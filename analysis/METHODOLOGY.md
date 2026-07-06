# How to Conduct This Research — Step-by-Step Runbook

A repeatable process for finding England areas where **1–3 bed** market rent, LHA, Affordable Rent (80% market) and social rent **converge**, then shortlisting investable locations and the operators active there. Follow the phases in order. Skipping the data-provenance rules (Phase 0) is how these studies go wrong.

> **Not technical?** Read [`HOW-TO-CHECK-THE-DATA.md`](HOW-TO-CHECK-THE-DATA.md) first — it's a no-code, plain-English version that shows how to find, download and read the same data and do the convergence check by hand in a free spreadsheet. This document is the fuller technical runbook that also uses the Python script.

**Estimated effort:** ~2–4 days for a first full run; ~half a day to refresh once the pipeline exists.

---

## Phase 0 — Set up and ground rules (do this first)

1. **Tools.** Install Python + `pandas`, `openpyxl`, `odfpy`, `requests`. Everything below can be done in a spreadsheet, but the datasets are large enough that a script pays off (this repo's `convergence_analysis.py` already implements the scoring).
2. **Golden rule — don't fabricate.** Every rent figure must trace to a named published source. Calculations (80% of market, ratios, coefficient of variation) are fine; *inventing* an input is not. Mark anything unverified as `n/v`, never as a number.
3. **Fix your reference dates.** Rents move; LHA is frozen at a point in time. Record the exact release/period of every dataset so the comparison is like-for-like (e.g. "ONS PRMS 12 months to Sept 2024", "LHA 2024/25 = 30th percentile of rents to Sept 2023").
4. **Decide the geography you will report in.** LHA is published by **BRMA**; market and social rent by **local authority (LA)**. These do not coincide. Pick LA as the reporting unit and map each LA to its dominant BRMA (Phase 5), or report at BRMA and accept LA approximations. Document the choice.

---

## Phase 1 — Define scope and the convergence metric

1. **Scope:** England, **1/2/3 bed self-contained only**. Exclude studios, rooms and shared accommodation at the point of data extraction, not later.
2. **The four layers per area (monthly £):** market rent `M_b`, LHA `L_b`, Affordable Rent `A_b = 0.80 × M_b`, social rent `S`.
3. **Metric (fix the formulas before you look at data, so results aren't reverse-engineered):**
   - LHA–market alignment = `mean_b( min(L_b / M_b, 1) )` → 1.0 = converged
   - Affordable-vs-LHA cover (diagnostic) = `mean_b( min(L_b / (0.80·M_b), 1) )` → 1.0 when LHA ≥ Affordable
   - Social attachment = `S_monthly / mean(M_1,M_2,M_3)` → higher = less detached
   - Compression = `1 − CV(M_1,M_2,M_3)`, CV = st.dev/mean → higher = tighter spread
   - **Composite = 0.40·alignment + 0.30·social_attachment + 0.30·compression** (weights are a choice — write them down and test sensitivity later).

---

## Phase 2 — Gather MARKET rents (ONS Private Rental Market Statistics)

1. **Source:** ONS *Private rental market summary statistics in England* (median monthly rent by **bedroom category**, region and administrative area). This replaced the old VOA PRMS series.
   `https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/privaterentalmarketsummarystatisticsinengland`
2. Download the latest dataset (published ~every 6 months; ODS/Excel). Note the 12-month period it covers.
3. Extract, per LA: **median monthly rent for 1-bed, 2-bed, 3-bed**. Discard room/studio/4+ columns.
4. Sanity check: 3-bed ≥ 2-bed ≥ 1-bed in almost all areas; flag reversals as data quirks (thin samples).

## Phase 3 — Gather LHA rates (DWP / VOA)

1. **Source:** GOV.UK *Local Housing Allowance rates* collection; the machine-readable England file is the cleanest input.
   Collection: `https://www.gov.uk/government/collections/local-housing-allowance-lha-rates`
   England monthly CSV (2024/25 example): `england-rates-2024-to-2025.csv` (already **monthly**, by BRMA, all 5 categories).
2. Extract, per BRMA: **1-bed, 2-bed, 3-bed** monthly rates. Discard shared-accommodation and 4-bed.
3. **Record the LHA basis and freeze status.** 2024/25 rates = 30th percentile of market rents to **30 Sep 2023**; frozen into 2025/26. This is central: the LHA–market gap *widens* as market rents rise above that frozen base, so convergence decays over time. Always know how stale the LHA base is versus your market-rent period.

## Phase 4 — Gather SOCIAL rents (Regulator of Social Housing)

1. **Source:** RSH *Registered provider social housing stock and rents in England* (latest year), plus the *Local authority* equivalent. Use the **dynamic LA look-up tool** for area-level average weekly general-needs rent.
   `https://www.gov.uk/government/statistics/registered-provider-social-housing-stock-and-rents-in-england-2024-to-2025`
2. Extract per LA: **average weekly general-needs social rent.** Convert to monthly: `× 52 / 12`.
3. If an LA figure is missing, fall back to the **regional average** (e.g. England £113.69/wk; North East £95.16; London £140.70 in 2024/25) and label it an estimate — do not leave it blank or invent a bespoke number.

## Phase 5 — Reconcile geography (BRMA ↔ LA)

1. Build a lookup mapping each LA to its dominant BRMA. Sources: the VOA BRMA definitions / LHA-Direct (`https://lha-direct.voa.gov.uk/`), or ONS geography lookups.
2. Where an LA spans multiple BRMAs (or a BRMA covers several LAs), pick the dominant one and **flag the approximation**. This is the single biggest source of noise — note it wherever it bites.

---

## Phase 6 — Compute Affordable Rent and the convergence score

1. Affordable Rent `A_b = 0.80 × M_b` for each bed size (this is the only rent you *derive*; the rest are observed).
2. Join the three datasets on your reporting unit (Phase 5) and compute the four metric components and the composite from Phase 1.
3. **Shortcut:** use this repo's script —
   ```bash
   pip install pandas openpyxl odfpy requests
   python analysis/convergence_analysis.py --selftest        # verify the logic
   python analysis/convergence_analysis.py \
       --lha england-rates-2024-to-2025.csv \
       --market prms_median_rents.ods \
       --social rsh_la_lookup.xlsx \
       --out convergence_ranking.csv
   ```
   It parses the files tolerantly, computes the metric, and writes a ranked CSV.

---

## Phase 7 — Overlay DEMAND and SUPPLY (convergence alone isn't enough)

A converged market with no demand is a value trap. Pull these per area and rank them alongside the score:

| Signal | Source |
|---|---|
| Households on the housing register (waiting list) | MHCLG *Social housing lettings* / live tables |
| Temporary-accommodation & homelessness acceptances | MHCLG *Statutory homelessness in England* |
| Net additional dwellings / housing delivery | MHCLG *Housing supply: net additional dwellings* & *Housing Delivery Test* |
| Planning activity / land supply pressure | MHCLG *Planning applications statistics*; local plan status |
| Population & household growth | ONS population projections; census |
| Local employment / regeneration | Combined-authority & council economic plans; Freeport/levelling-up announcements |

Rule of thumb: prioritise areas that are **converged (Phase 6) AND demand-tight (waiting-list pressure, rising TA) AND supply-constrained or regenerating.**

---

## Phase 8 — Rank, shortlist and pressure-test

1. Sort by composite score; overlay the demand signals to produce an **investable** ranking (not just a "cheapest rents" list).
2. **Demote traps:** very cheap + weak demand + poor stock (e.g. some coastal markets) — aligned on paper, high real-world risk.
3. **Sensitivity test:** re-run with different weights and with 2-bed-only. If the top of the list is stable, it's robust; if it lurches, say so.
4. Pick a top 5 on the *combination* of tight convergence, durable demand, regeneration momentum and manageable risk.

---

## Phase 9 — Identify operators active in the stream + due diligence

For each shortlisted area, find who already delivers social/affordable rent there and screen them:

1. **Who's active:** council "registered providers"/"housing associations" directory pages; the council's ALMO; choice-based-lettings partners; for-profit BTR operators for the commercial angle.
2. **Scale & health, per provider:**
   - Homes owned/managed — provider website / annual report / RSH statistical data.
   - **RSH regulatory judgement — governance (G), viability (V), consumer (C):** `https://www.gov.uk/government/publications/regulatory-judgements-and-regulatory-notices` (1 = strongest; V2 is normal for big developers).
   - Financial strength — audited accounts / Statement of Comprehensive Income; credit ratings (Moody's/S&P) for the largest.
   - Development pipeline — annual report + Homes England Strategic Partnership allocations.
3. **Correctly classify:** ALMOs aren't separately G/V-graded (the council holds the registration); sub-1,000-home RPs aren't individually graded; for-profit providers sit outside the standard G/V regime. Don't force a grade where none exists — mark `—`.

---

## Phase 10 — Validate and document

1. **Cross-check** a handful of areas against a second source (e.g. an agent index like Rightmove/Zoopla rental data, or a council housing-needs assessment) to confirm the market-rent picture isn't a sample artefact.
2. **Cite everything:** dataset name, publisher, release period, URL, for every figure. Keep a sources sheet.
3. **State limitations plainly:** BRMA↔LA approximation, LHA freeze/staleness, any regional fallbacks used for social rent, thin-sample LAs.

## Phase 11 — Refresh cadence

- **ONS PRMS:** ~every 6 months → recompute market layer and the score.
- **LHA:** annually each April (and whenever re-pegged to the 30th percentile) → the alignment component can move sharply on a re-peg.
- **RSH rents & grades:** annually → refresh social layer and provider due diligence.
- Re-run the whole pipeline on each release; convergence is a moving target because LHA is frozen while market rents drift.

---

### One-paragraph summary
Fix your metric and reference dates first. Pull **market rent** (ONS PRMS, 1–3 bed medians by LA), **LHA** (DWP/VOA, 1–3 bed by BRMA — note the frozen 30th-percentile base), and **social rent** (RSH, weekly by LA → monthly). Reconcile BRMA↔LA. Derive Affordable Rent as 80% of market, compute alignment + social-attachment + compression into a composite score, then overlay waiting-list/homelessness/supply data to turn "converged" into "investable." Shortlist, pressure-test the weights, then profile the RPs/ALMOs/BTR operators active in each area using RSH grades and accounts. Cite every number; refresh when ONS/LHA/RSH update.
