#!/usr/bin/env python3
"""
MEASURED convergence ranking from the real supplied datasets.

Inputs (in analysis/data/, all Open Government Licence):
  - ONS_PRMS_Oct2022-Sep2023.xls   VOA/ONS Private Rental Market Statistics:
        median monthly rent by bedroom, by administrative area (LA).
        Tables 2.3 / 2.4 / 2.5 = One / Two / Three bedrooms.
  - LHA_TABLES_2026-27.xlsx        DWP/VOA LHA: Table 1 = LHA rates from Apr 2024
        (weekly), carried forward to 2026/27 (frozen). CAT B/C/D = 1/2/3 bed.
  - RSH_RP_combined_tool_2024-25.xlsx  Social rent: per-LA, per-bedsize average
        general-needs (GN = social rent) net weekly rent, from the 'Flat_File'
        sheet, weighted across PRP (SDR) and council (LADR) stock. Joined to
        market on the ONS area E-code. England avg £113.69/wk kept only as a
        fallback where an LA has no GN figure.

Time alignment: the ONS rents (Oct 2022-Sep 2023) are the SAME 12-month window
the frozen LHA is derived from, so this measures STRUCTURAL convergence at the
LHA reference point (it is not today's live gap, which is wider as market rents
have since risen).

Output: analysis/measured_convergence_ranking.csv
"""
from __future__ import annotations
import os, re, math
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
ONS = os.path.join(DATA, "ONS_PRMS_Oct2022-Sep2023.xls")
LHA = os.path.join(DATA, "LHA_TABLES_2026-27.xlsx")
SOCIAL = os.path.join(DATA, "RSH_RP_combined_tool_2024-25.xlsx")
OUT = os.path.join(HERE, "measured_convergence_ranking.csv")

ENGLAND_SOCIAL_WEEKLY = 113.69          # RSH 2024/25 general-needs avg (fallback only)
W2M = 52.0 / 12.0
AFFORDABLE = 0.80
W_ALIGN, W_SOCIAL, W_COMPRESS = 0.40, 0.30, 0.30

# Curated LA -> BRMA map for areas whose names don't match (BRMAs are broader /
# differently named than lower-tier districts). Only mappings we are confident of;
# every target BRMA is verified to exist in the LHA file at load time. Multi-BRMA
# LAs use their dominant BRMA and are flagged geo_approx=curated.
LA_TO_BRMA = {
    # North East
    "Middlesbrough UA": "Teesside", "Stockton-on-Tees UA": "Teesside",
    "Redcar and Cleveland UA": "Teesside", "Hartlepool UA": "Teesside",
    "County Durham UA": "Durham", "Darlington UA": "Darlington",
    "Gateshead": "Tyneside", "Newcastle upon Tyne": "Tyneside",
    "North Tyneside": "Tyneside", "South Tyneside": "Tyneside",
    "Sunderland": "Sunderland", "Northumberland UA": "Northumberland",
    # Yorkshire & Humber
    "Kingston upon Hull, City of UA": "Hull & East Riding",
    "East Riding of Yorkshire UA": "Hull & East Riding",
    "North East Lincolnshire UA": "Grimsby", "North Lincolnshire UA": "Scunthorpe",
    "Bradford": "Bradford & South Dales", "Calderdale": "Halifax",
    # North West
    "Blackburn with Darwen UA": "East Lancs", "Burnley": "East Lancs",
    "Pendle": "East Lancs", "Hyndburn": "East Lancs", "Rossendale": "East Lancs",
    "Preston": "Central Lancs", "South Ribble": "Central Lancs", "Chorley": "Central Lancs",
    "Bolton": "Bolton and Bury", "Bury": "Bolton and Bury",
    "Oldham": "Oldham & Rochdale", "Rochdale": "Oldham & Rochdale",
    "Liverpool": "Greater Liverpool", "Knowsley": "Greater Liverpool",
    "Blackpool UA": "Fylde Coast",
    # East Midlands
    "Mansfield": "North Nottingham", "Ashfield": "North Nottingham",
    # West Midlands
    "Stoke-on-Trent UA": "Staffordshire North", "Newcastle-under-Lyme": "Staffordshire North",
    "Wolverhampton": "Black Country", "Dudley": "Black Country",
    "Sandwell": "Black Country", "Walsall": "Black Country",
}

# Curated LAs that genuinely span several BRMAs (one dominant BRMA used) -> flagged
# 'curated-approx'. The rest of the curated map was web-verified (East Lancs, Central
# Lancs, Black Country, Teesside, Tyneside, Staffordshire North, etc.) -> 'curated'.
APPROX = {"County Durham UA", "East Riding of Yorkshire UA", "Mansfield", "Ashfield"}


def norm(s: str) -> str:
    s = str(s).lower()
    s = re.sub(r"\b(ua|md|london borough|borough|city of|the)\b", " ", s)
    s = re.sub(r"[^a-z ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def to_float(x):
    try:
        v = float(re.sub(r"[^0-9.]", "", str(x)))
        return v if v > 0 else None
    except (ValueError, TypeError):
        return None


def load_ons_bed(sheet):
    df = pd.read_excel(ONS, sheet_name=sheet, header=6)
    df = df[df["LA Code1"].notna()].copy()            # LA rows only (drop region/England)
    df["Area"] = df["Area"].astype(str).str.strip()
    df["code"] = df["Area Code1"].astype(str).str.strip()
    df["median"] = df["Median"].map(to_float)
    df["count"] = df["Count of rents"].map(to_float)
    return df.set_index("Area")[["code", "median", "count"]]


def load_social():
    """Per-LA GN (social rent) net weekly rent by bedsize, weighted PRP+LARP.
    Returns ({LA E-code: {'1':monthly,'2':..,'3':..}}, {LA E-code: region})."""
    df = pd.read_excel(SOCIAL, sheet_name="Flat_File")
    region = {str(r.LA_Code).strip(): str(r.Region).strip()
              for r in df.itertuples() if pd.notna(r.Region)}
    df = df[(df["Type"] == "GN") & (df["Bedsize"].isin(["1Bd", "2Bd", "3Bd"]))].copy()
    for c in ["SDR_Own", "SDR_AVRENT", "LADR_Own", "LADR_AVRENT"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    out = {}
    bedmap = {"1Bd": "1", "2Bd": "2", "3Bd": "3"}
    for r in df.itertuples():
        num = r.SDR_AVRENT * r.SDR_Own + r.LADR_AVRENT * r.LADR_Own
        den = r.SDR_Own + r.LADR_Own
        if den <= 0:
            continue
        wk = num / den
        if wk > 0:
            out.setdefault(str(r.LA_Code).strip(), {})[bedmap[r.Bedsize]] = wk * W2M
    return out, region


def load_lha():
    df = pd.read_excel(LHA, sheet_name="Table 1", header=1)
    df = df.rename(columns={df.columns[0]: "BRMA"})
    df["BRMA"] = df["BRMA"].astype(str).str.strip()
    df = df[df["BRMA"].str.lower() != "nan"]
    # CAT B/C/D = 1/2/3 bed, WEEKLY -> monthly
    out = {}
    for _, r in df.iterrows():
        out[r["BRMA"]] = {
            "1": to_float(r["CAT B"]) and to_float(r["CAT B"]) * W2M,
            "2": to_float(r["CAT C"]) and to_float(r["CAT C"]) * W2M,
            "3": to_float(r["CAT D"]) and to_float(r["CAT D"]) * W2M,
        }
    return out


def cv(vals):
    vals = [v for v in vals if v]
    if len(vals) < 2:
        return None
    m = sum(vals) / len(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / len(vals)) / m if m else None


def main():
    m1, m2, m3 = load_ons_bed("Table2.3"), load_ons_bed("Table2.4"), load_ons_bed("Table2.5")
    lha = load_lha()
    social, region_by_code = load_social()
    for b in set(LA_TO_BRMA.values()):
        assert b in lha, f"curated BRMA not found in LHA file: {b}"
    lha_norm = {norm(k): k for k in lha}
    nat_social = ENGLAND_SOCIAL_WEEKLY * W2M

    areas = sorted(set(m1.index) | set(m2.index) | set(m3.index))
    rows = []
    for area in areas:
        market = {"1": m1["median"].get(area) if area in m1.index else None,
                  "2": m2["median"].get(area) if area in m2.index else None,
                  "3": m3["median"].get(area) if area in m3.index else None}
        if not all(market.values()):
            continue
        code = (m2["code"].get(area) if area in m2.index else
                m1["code"].get(area) if area in m1.index else m3["code"].get(area))
        cnt = min(x for x in [m1["count"].get(area) if area in m1.index else 0,
                              m2["count"].get(area) if area in m2.index else 0,
                              m3["count"].get(area) if area in m3.index else 0] if x)
        # resolve BRMA
        if area in LA_TO_BRMA:
            brma = LA_TO_BRMA[area]
            how = "curated-approx" if area in APPROX else "curated"
        elif norm(area) in lha_norm:
            brma, how = lha_norm[norm(area)], "exact"
        else:
            continue
        L = lha[brma]
        if not all(L.values()):
            continue

        # local social rent per bed (fallback: national avg where an LA bed is missing)
        soc = social.get(code, {})
        soc_src = "local" if soc else "national"
        soc_b = {b: soc.get(b, nat_social) for b in ("1", "2", "3")}

        aligns = [min(L[b] / market[b], 1.0) for b in ("1", "2", "3")]
        covers = [min(L[b] / (AFFORDABLE * market[b]), 1.0) for b in ("1", "2", "3")]
        attach = [min(soc_b[b] / market[b], 1.0) for b in ("1", "2", "3")]
        alignment = sum(aligns) / 3
        social_attach = sum(attach) / 3
        compression = 1 - cv(list(market.values()))
        score = (W_ALIGN * alignment + W_SOCIAL * social_attach + W_COMPRESS * compression)

        rows.append({
            "area": area, "code": code, "region": region_by_code.get(code, ""),
            "brma": brma, "geo": how, "soc_src": soc_src, "sample_min": int(cnt),
            "mkt_1": round(market["1"]), "mkt_2": round(market["2"]), "mkt_3": round(market["3"]),
            "lha_1": round(L["1"]), "lha_2": round(L["2"]), "lha_3": round(L["3"]),
            "soc_1": round(soc_b["1"]), "soc_2": round(soc_b["2"]), "soc_3": round(soc_b["3"]),
            "affordable_2": round(AFFORDABLE * market["2"]),
            "alignment": round(alignment, 3),
            "afford_cover": round(sum(covers) / 3, 3),
            "social_attach": round(social_attach, 3),
            "compression": round(compression, 3),
            "score": round(score, 3),
        })

    df = pd.DataFrame(rows).sort_values("score", ascending=False).reset_index(drop=True)
    df.insert(0, "rank", df.index + 1)
    df.to_csv(OUT, index=False)
    pd.set_option("display.width", 200, "display.max_columns", 30)
    nloc = (df["soc_src"] == "local").sum()
    print(f"Scored {len(df)} areas (exact + curated LA->BRMA); "
          f"{nloc} use LOCAL per-bed social rent, {len(df)-nloc} national fallback.\n")
    print("TOP 25:")
    print(df.head(25)[["rank", "area", "brma", "geo", "sample_min",
                       "mkt_2", "lha_2", "soc_2", "alignment",
                       "social_attach", "compression", "score"]].to_string(index=False))
    print(f"\nFull table -> {OUT}")


if __name__ == "__main__":
    main()
