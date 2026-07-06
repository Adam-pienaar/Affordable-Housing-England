# Affordable Housing England — Rent Convergence Analysis

Identifies areas in England where **1–3 bedroom** rents (studios and shared
accommodation excluded) show **convergence** across the four rent layers —
**market rent, Local Housing Allowance (LHA), Affordable Rent (80% of market),
and social rent** — making rent risk lower and housing-benefit alignment
stronger for affordable-housing development or investment.

## Contents

| File | What it is |
|---|---|
| [`analysis/uk-rent-convergence-analysis.md`](analysis/uk-rent-convergence-analysis.md) | The report: mechanism, convergence metric, ranked areas (top 15–25), top-5 opportunities, risks, sources. |
| [`analysis/HOW-TO-CHECK-THE-DATA.md`](analysis/HOW-TO-CHECK-THE-DATA.md) | **No-code, plain-English guide** for a non-technical person to find, download, open and read the official data, and do the convergence check by hand in a free spreadsheet. Start here to verify the numbers yourself. |
| [`analysis/convergence_analysis.py`](analysis/convergence_analysis.py) | Reproducible scorer that computes exact per-area convergence scores from the live gov.uk / ONS datasets. |
| [`analysis/METHODOLOGY.md`](analysis/METHODOLOGY.md) | Technical step-by-step runbook (uses the script) to conduct the whole study: data sources, formulas, geography reconciliation, demand overlay, provider due diligence, refresh cadence. |
| [`analysis/top5-area-providers.md`](analysis/top5-area-providers.md) | Operators active in the social/affordable rent stream in each top-5 area, with homes owned + RSH grades. |

## Key finding (one line)

Rent convergence is **structurally concentrated in the low-cost North and
Midlands** — because LHA is the 30th percentile of local rents, and social rent
is nationally near-uniform while market rent varies hugely, all four rent layers
sit closest together exactly where market rents are lowest and most compressed.

## How the ranking is derived

For each area, using **1/2/3-bed only** (monthly £):

- **LHA–market alignment** — `mean(min(LHA_b / Market_b, 1))`
- **Affordable-vs-LHA cover** — Affordable = `0.80 × Market`; is LHA ≥ Affordable?
- **Social-rent attachment** — `Social_monthly / mean(Market_1,2,3)`
- **Rent compression** — `1 − CV(Market_1, Market_2, Market_3)`

Composite: `0.40·alignment + 0.30·social_attachment + 0.30·compression`, with a
demand/shortage overlay to prioritise *investable* convergence.

## Reproduce the exact per-area numbers

```bash
pip install pandas openpyxl odfpy requests

# sanity-check the scoring logic (no network needed)
python analysis/convergence_analysis.py --selftest

# compute the full ranking from local copies of the published datasets
python analysis/convergence_analysis.py \
    --lha england-rates-2024-to-2025.csv \
    --market prms_median_rents.ods \
    --social rsh_la_lookup.xlsx \
    --out convergence_ranking.csv
```

Download the source files from:

- **LHA (England, monthly, by BRMA):** DWP/VOA *Local Housing Allowance rates* collection.
- **Market rent (median monthly by bedroom/LA):** ONS *Private Rental Market Summary Statistics in England*.
- **Social rent (by LA, weekly):** Regulator of Social Housing *social housing stock and rents 2024/25* look-up tool.

Exact URLs and citations are in the report's **Sources** section.

## Data-integrity note

Figures are taken from official published sources (ONS, DWP/VOA, Regulator of
Social Housing, MHCLG) and cited in the report. Where the full per-area datasets
could not be machine-downloaded in the environment that drafted the report
(gov.uk/ONS were blocked by network policy), **no numbers were invented** — the
area ranking is an evidence-based *pattern* read grounded in verified
national/regional data, and the script recomputes exact scores against the live
data. See the report's **Data provenance & limitations** section.
