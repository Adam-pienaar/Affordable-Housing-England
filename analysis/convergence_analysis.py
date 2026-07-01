#!/usr/bin/env python3
"""
UK Rent Convergence Analysis (England, 1-3 bed only).

Computes, for each area, how tightly aligned the four rent "layers" are:
    - Market rent (ONS Private Rental Market Statistics, median monthly by bedroom)
    - LHA          (DWP/VOA Local Housing Allowance, monthly, by BRMA)
    - Affordable   (estimated as 80% of market rent -- statutory definition)
    - Social rent  (Regulator of Social Housing, average weekly general-needs rent)

and ranks areas by a composite "convergence strength" score.

WHY A SCRIPT?
    The analysis environment that produced the accompanying report had gov.uk /
    ons.gov.uk blocked by network policy, so the full per-area datasets could not
    be downloaded there. Run this in an environment WITH access to those hosts to
    generate exact, verifiable per-area scores. No figures are hard-coded except
    the two published constants below (both cited in the report).

USAGE
    pip install pandas openpyxl odfpy requests
    python convergence_analysis.py                      # tries to download live data
    python convergence_analysis.py --lha lha.csv \
        --market prms.ods --social rsh.xlsx             # use local files instead
    python convergence_analysis.py --selftest           # run scoring on synthetic data

DATA SOURCES (see report Section 9 for full citations)
    LHA 2024/25 (England, monthly, by BRMA):
      https://assets.publishing.service.gov.uk/media/65ba5f24c75d30000dca0fce/england-rates-2024-to-2025.csv
    ONS Private Rental Market Statistics (median monthly rent by bedroom/LA):
      https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/privaterentalmarketsummarystatisticsinengland
    RSH social housing stock & rents 2024/25 (LA look-up tool, weekly rents):
      https://www.gov.uk/government/statistics/registered-provider-social-housing-stock-and-rents-in-england-2024-to-2025
"""
from __future__ import annotations

import argparse
import sys
import re
import math

# --- Published constants (cited in the report, Section 9) ---------------------
ENGLAND_AVG_SOCIAL_WEEKLY = 113.69      # RSH 2024/25 general-needs avg (fallback only)
AFFORDABLE_RENT_FACTOR = 0.80           # Affordable Rent = 80% of market (statutory)
WEEKLY_TO_MONTHLY = 52.0 / 12.0         # convert weekly rent -> monthly

# Composite score weights (documented in report Section 3; adjust freely).
W_ALIGNMENT = 0.40      # LHA close to market rent
W_SOCIAL    = 0.30      # social rent not wildly detached from market
W_COMPRESS  = 0.30      # 1/2/3-bed rents tightly clustered

BEDS = ("1", "2", "3")  # 1-3 bed ONLY. Studios / rooms / 4+ bed are excluded.

LHA_CSV_URL = ("https://assets.publishing.service.gov.uk/media/"
               "65ba5f24c75d30000dca0fce/england-rates-2024-to-2025.csv")


# ---------------------------------------------------------------------------
# Core scoring (pure functions -- fully testable without any network access)
# ---------------------------------------------------------------------------
def coefficient_of_variation(values):
    """CV = population std / mean. Lower CV => tighter clustering."""
    vals = [v for v in values if v is not None and not _isnan(v)]
    if len(vals) < 2:
        return None
    mean = sum(vals) / len(vals)
    if mean == 0:
        return None
    var = sum((v - mean) ** 2 for v in vals) / len(vals)
    return math.sqrt(var) / mean


def _isnan(x):
    try:
        return math.isnan(x)
    except TypeError:
        return False


def convergence_components(market_by_bed, lha_by_bed, social_monthly):
    """
    market_by_bed, lha_by_bed: dict like {"1": m1, "2": m2, "3": m3} (monthly GBP)
    social_monthly: monthly social rent for the area (GBP)
    Returns dict of the four diagnostics + composite score in [0, 1].
    """
    # LHA-market alignment: mean of min(LHA/Market, 1) across beds present.
    aligns = []
    covers = []
    for b in BEDS:
        m = market_by_bed.get(b)
        l = lha_by_bed.get(b)
        if not m or not l or _isnan(m) or _isnan(l) or m <= 0:
            continue
        aligns.append(min(l / m, 1.0))
        affordable = AFFORDABLE_RENT_FACTOR * m           # 80% of market
        covers.append(min(l / affordable, 1.0) if affordable > 0 else 0.0)
    alignment = sum(aligns) / len(aligns) if aligns else None
    affordable_cover = sum(covers) / len(covers) if covers else None

    # Social attachment: social / mean(market). Cap at 1 (>=market is fully attached).
    market_vals = [market_by_bed.get(b) for b in BEDS
                   if market_by_bed.get(b) and not _isnan(market_by_bed.get(b))]
    mean_market = sum(market_vals) / len(market_vals) if market_vals else None
    if mean_market and social_monthly and mean_market > 0:
        social_attach = min(social_monthly / mean_market, 1.0)
    else:
        social_attach = None

    # Compression: 1 - CV of the 1/2/3-bed market rents.
    cv = coefficient_of_variation(market_vals)
    compression = (1.0 - cv) if cv is not None else None

    # Composite (only over components we could compute).
    parts, wsum = 0.0, 0.0
    for val, w in ((alignment, W_ALIGNMENT),
                   (social_attach, W_SOCIAL),
                   (compression, W_COMPRESS)):
        if val is not None:
            parts += w * max(0.0, min(1.0, val))
            wsum += w
    score = (parts / wsum) if wsum > 0 else None

    return {
        "alignment": alignment,
        "affordable_cover": affordable_cover,
        "social_attachment": social_attach,
        "compression": compression,
        "score": score,
    }


# ---------------------------------------------------------------------------
# Data loading (best-effort; tolerant of the published file layouts)
# ---------------------------------------------------------------------------
def _bed_from_label(label: str):
    """Map an LHA/PRMS category label to '1','2','3' or None (excludes studio/room/4+)."""
    s = str(label).lower()
    if "shared" in s or "room" in s or "studio" in s:
        return None
    m = re.search(r"(\d+)\s*bed", s)
    if m and m.group(1) in BEDS:
        return m.group(1)
    m = re.search(r"\b([1-3])\b", s)
    return m.group(1) if m else None


def load_lha(path_or_url, pd):
    """
    Parse the England UC LHA monthly-rates CSV into {BRMA: {'1':m1,'2':m2,'3':m3}}.
    Layout varies between releases, so detect columns tolerantly.
    """
    df = pd.read_csv(path_or_url)
    cols = {c.lower().strip(): c for c in df.columns}
    brma_col = next((cols[k] for k in cols if "brma" in k or "area" in k), df.columns[0])

    out = {}
    # Wide layout: one column per bedroom category.
    bed_cols = {}
    for c in df.columns:
        b = _bed_from_label(c)
        if b:
            bed_cols[b] = c
    if bed_cols:
        for _, row in df.iterrows():
            brma = str(row[brma_col]).strip()
            rec = {}
            for b, c in bed_cols.items():
                rec[b] = _to_float(row[c])
            out[brma] = rec
        return out

    # Long layout: category + rate columns.
    cat_col = next((cols[k] for k in cols if "categ" in k or "bedroom" in k), None)
    rate_col = next((cols[k] for k in cols if "rate" in k or "amount" in k or "month" in k), None)
    if cat_col and rate_col:
        for _, row in df.iterrows():
            b = _bed_from_label(row[cat_col])
            if not b:
                continue
            out.setdefault(str(row[brma_col]).strip(), {})[b] = _to_float(row[rate_col])
    return out


def _to_float(x):
    try:
        return float(re.sub(r"[^0-9.]", "", str(x)))
    except (ValueError, TypeError):
        return None


def load_market(path, pd):
    """
    ONS PRMS: median monthly rent by bedroom category and area.
    Returns {area: {'1':..,'2':..,'3':..}}. The published workbook has several
    sheets; the caller may need to point --market at the right sheet/export.
    """
    engine = "odf" if str(path).lower().endswith(".ods") else None
    df = pd.read_excel(path, engine=engine)
    cols = {c.lower().strip(): c for c in df.columns}
    area_col = next((cols[k] for k in cols
                     if "area" in k or "authority" in k or "brma" in k or "name" in k),
                    df.columns[0])
    bed_cols = {b: c for c in df.columns if (b := _bed_from_label(c))}
    out = {}
    for _, row in df.iterrows():
        area = str(row[area_col]).strip()
        out[area] = {b: _to_float(row[c]) for b, c in bed_cols.items()}
    return out


def load_social(path, pd):
    """RSH LA look-up: {area: weekly_general_needs_social_rent}. Fallback: England avg."""
    engine = "odf" if str(path).lower().endswith(".ods") else None
    df = pd.read_excel(path, engine=engine)
    cols = {c.lower().strip(): c for c in df.columns}
    area_col = next((cols[k] for k in cols if "authority" in k or "area" in k or "name" in k),
                    df.columns[0])
    rent_col = next((cols[k] for k in cols
                     if ("general" in k and "rent" in k) or ("social" in k and "rent" in k)
                     or "weekly" in k), None)
    out = {}
    if rent_col:
        for _, row in df.iterrows():
            out[str(row[area_col]).strip()] = _to_float(row[rent_col])
    return out


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def build_ranking(lha, market, social, pd):
    """Join on area name (documented approximation: BRMA vs LA geographies differ)."""
    rows = []
    for area, mkt in market.items():
        lha_rec = lha.get(area) or _fuzzy_lookup(lha, area) or {}
        soc_weekly = social.get(area) or _fuzzy_lookup(social, area) or ENGLAND_AVG_SOCIAL_WEEKLY
        soc_monthly = soc_weekly * WEEKLY_TO_MONTHLY if soc_weekly else None
        comp = convergence_components(mkt, lha_rec, soc_monthly)
        rows.append({
            "area": area,
            "market_1": mkt.get("1"), "market_2": mkt.get("2"), "market_3": mkt.get("3"),
            "lha_1": lha_rec.get("1"), "lha_2": lha_rec.get("2"), "lha_3": lha_rec.get("3"),
            "social_monthly": round(soc_monthly, 1) if soc_monthly else None,
            **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in comp.items()},
        })
    df = pd.DataFrame(rows)
    return df.sort_values("score", ascending=False, na_position="last")


def _fuzzy_lookup(d, area):
    a = area.lower().strip()
    for k, v in d.items():
        kl = k.lower().strip()
        if kl == a or kl in a or a in kl:
            return v
    return None


def run_live():
    try:
        import pandas as pd
    except ImportError:
        sys.exit("pandas required: pip install pandas openpyxl odfpy requests")
    print("Downloading LHA CSV ...", file=sys.stderr)
    lha = load_lha(LHA_CSV_URL, pd)
    sys.exit("Provide --market (ONS PRMS) and --social (RSH) files; "
             "the ONS/RSH workbooks are multi-sheet and must be pointed at explicitly. "
             f"Parsed {len(lha)} BRMAs from LHA CSV.")


def run_from_files(args):
    import pandas as pd
    lha = load_lha(args.lha, pd)
    market = load_market(args.market, pd)
    social = load_social(args.social, pd) if args.social else {}
    ranking = build_ranking(lha, market, social, pd)
    out = args.out or "convergence_ranking.csv"
    ranking.to_csv(out, index=False)
    print(ranking.head(25).to_string(index=False))
    print(f"\nFull ranking written to {out}")


def selftest():
    """Validate the scoring logic on synthetic data (no network needed)."""
    # A: converged low-cost market. B: expensive, dispersed, detached (London-like).
    a = convergence_components(
        market_by_bed={"1": 500, "2": 575, "3": 650},
        lha_by_bed={"1": 460, "2": 540, "3": 620},      # LHA close to market
        social_monthly=430)                             # ~70% of mean market
    b = convergence_components(
        market_by_bed={"1": 1600, "2": 2100, "3": 2900},
        lha_by_bed={"1": 1100, "2": 1350, "3": 1600},   # LHA far below market
        social_monthly=610)                             # tiny share of market
    print("Converged market A:", {k: round(v, 3) for k, v in a.items() if v is not None})
    print("Detached market B :", {k: round(v, 3) for k, v in b.items() if v is not None})
    assert a["score"] > b["score"], "converged market should outrank detached market"
    assert a["alignment"] > b["alignment"]
    assert a["social_attachment"] > b["social_attachment"]
    assert a["compression"] > b["compression"]
    # Affordable-cover sanity: A's LHA should cover ~80% market better than B's.
    assert a["affordable_cover"] > b["affordable_cover"]
    print("\nSELFTEST PASSED: converged market scores higher on every component.")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--lha", help="LHA CSV path (else download live)")
    p.add_argument("--market", help="ONS PRMS workbook (.ods/.xlsx)")
    p.add_argument("--social", help="RSH social-rent look-up (.ods/.xlsx)")
    p.add_argument("--out", help="output CSV path")
    p.add_argument("--selftest", action="store_true", help="run synthetic-data test")
    args = p.parse_args()

    if args.selftest:
        selftest()
    elif args.lha and args.market:
        run_from_files(args)
    else:
        run_live()


if __name__ == "__main__":
    main()
