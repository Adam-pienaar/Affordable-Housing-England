# Measured Convergence Ranking — Results

This is the **measured** analysis, computed from official datasets (in `analysis/data/`). Reproduce with `python analysis/run_measured_ranking.py` → `analysis/measured_convergence_ranking.csv`.

**All three rent layers are now real and local.** Only the geography (LA→BRMA) still uses a curated map.

## Data used
- **Market rent:** ONS/VOA Private Rental Market Statistics — median monthly rent by bedroom, by local authority, **Oct 2022 – Sep 2023** (Tables 2.3/2.4/2.5).
- **LHA:** DWP/VOA Table 1 — April-2024 weekly rates, frozen/carried to 2026/27; CAT B/C/D = 1/2/3-bed → monthly.
- **Social rent:** RSH 2024/25 combined tool (`Flat_File`) — **per-LA, per-bedsize general-needs (social rent) net rent**, weighted across PRP and council stock, joined to market on the ONS area E-code. **92 of 97 areas use local social rent**; 5 use the England fallback (Barrow-in-Furness, Scarborough, Northampton, Harrogate, Mendip — old ONS area codes that don't match the 2024/25 RSH file after local-government reorganisation).
- **Affordable Rent:** derived = 80% × market.

**Why this pairing is clean:** the ONS rent window (Oct 2022–Sep 2023) is the same 12 months the frozen LHA is derived from, so this measures **structural convergence at the LHA reference point** — not today's live gap (which is wider, as market rents have risen since).

**Coverage:** 97 local authorities — those with a reliable ONS median for all of 1/2/3-bed and a defensible LA→BRMA match. Multi-BRMA LAs use their dominant BRMA (`geo=curated`). Full national coverage needs the official LA→BRMA lookup.

---

## Headline: the thesis holds; local social rents refine the order

Every top-25 area is a low-cost North / Midlands market; the least-converged are all high-rent South (Cambridge, Brighton, Bristol, Exeter, Oxford). Using **real local social rents** (instead of a national average) pulled **Teesside up** and eased **Hull down**, because Teesside's social rents are a higher share of its market rent than Hull's unusually low social rents are of theirs.

### Top 20 (measured, fully local)

| Rank | Area | BRMA | Mkt 2-bed | LHA 2-bed | Social 2-bed | Score |
|---|---|---|---|---|---|---|
| 1 | Burnley | East Lancs | £475 | £474 | £425 | 0.928 |
| 2 | Hartlepool | Teesside | £500 | £474 | £441 | 0.921 |
| 3 | Redcar & Cleveland | Teesside | £510 | £474 | £461 | 0.906 |
| 4 | Hyndburn | East Lancs | £495 | £474 | £403 | 0.889 |
| 5 | Middlesbrough | Teesside | £525 | £474 | £450 | 0.888 |
| 6 | Barrow-in-Furness † | Barrow-in-Furness | £550 | £499 | £493* | 0.886 |
| 7 | South Tyneside | Tyneside | £500 | £549 | £396 | 0.883 |
| 8 | North East Lincs (Grimsby) | Grimsby | £525 | £479 | £426 | 0.883 |
| 9 | North Lincolnshire (Scunthorpe) | Scunthorpe | £525 | £494 | £421 | 0.879 |
| 10 | Pendle | East Lancs | £520 | £474 | £404 | 0.879 |
| 11 | County Durham | Durham | £450 | £399 | £390 | 0.875 |
| 12 | **Kingston upon Hull** | Hull & East Riding | £495 | £474 | £407 | 0.875 |
| 13 | Rotherham | Rotherham | £550 | £499 | £401 | 0.872 |
| 14 | Scarborough † | Scarborough | £600 | £549 | £493* | 0.871 |
| 15 | Gateshead | Tyneside | £580 | £549 | £406 | 0.869 |
| 16 | Blackburn with Darwen | East Lancs | £524 | £474 | £412 | 0.867 |
| 17 | Blackpool | Fylde Coast | £550 | £540 | £404 | 0.858 |
| 18 | Preston | Central Lancs | £600 | £573 | £422 | 0.850 |
| 19 | Sunderland | Sunderland | £550 | £474 | £418 | 0.850 |
| 20 | **Stoke-on-Trent** | Staffordshire North | £515 | £479 | £380 | 0.846 |

† social rent = national fallback (`*`), so score is slightly indicative. Least converged (bottom 5 of 97): Cambridge 0.674, Brighton & Hove 0.680, Bristol 0.688, Exeter 0.702, Oxford 0.708.

---

## The real mechanism (confirmed with local social rents)

"LHA close to market" is **not** the northern signature — LHA-to-market **alignment is high almost everywhere** (LHA is the 30th percentile by construction; even Cambridge 0.72, Guildford 0.94). What separates converged from non-converged areas is **social-rent attachment** — social rent sits close to market rent **only where market rent is low**:

| | Market 2-bed | Social 2-bed | Social attachment | Overall |
|---|---|---|---|---|
| Hartlepool (Teesside) | £500 | £441 | **0.88** | converged |
| Hull | £495 | £407 | **0.80** | converged (social a touch lower) |
| Bristol (South) | £1,325 | £442 | **0.34** | not converged |

Social rent barely varies nationally (~£380–£490/mo here), but market rent ranges from ~£475 to ~£1,400 — so **four-layer convergence requires a low-rent market**. That is the structural argument, now shown with fully local numbers.

---

## How the measured order revises the pattern-based list

| Earlier pattern read | Measured (local social) | Verdict |
|---|---|---|
| Teesside #3 | Hartlepool **#2**, Redcar **#3**, Middlesbrough **#5** | ⬆️ Now the standout cluster — strongest convergence *and* best demand story |
| Hull #2 | **#12** | ✅ Still top-tier, but its social rents are among the lowest nationally, so slightly more detached than Teesside |
| Stoke #1 | **#20** | ➖ Strong (0.846); rents a touch higher/wider than the cheapest towns |
| Doncaster #5 | **#22** | ✅ Confirmed; very low social rent (£384) trims its attachment |
| Wolverhampton / Black Country #6 | **#37+** | ❌ Over-ranked on pure convergence (higher WM rents; demand case is separate) |
| Burnley / East Lancs #15 | **#1, #4, #10, #16** | ⬆️ Under-ranked — the tightest convergence cluster |
| Hartlepool #18, Rotherham #17 | **#2, #13** | ⬆️ Under-ranked |
| Blackpool (demoted) | **#17 on the metric** | ⚠️ High score, but demoted for weak demand / poor stock — the metric measures rent alignment, not demand |

**Net:** the *pattern* (low-cost North/Midlands) was right; my *ordering* over-weighted regeneration narratives (Black Country, Stoke) and under-weighted the genuinely cheapest, tightest markets (Teesside, East Lancashire, Humber).

---

## A defensible revised Top 5 (convergence **plus** demand)

Convergence alone would crown East Lancashire; investment needs demand too. Balancing the measured score against demand/regeneration and stock-quality risk:

1. **Teesside — Hartlepool #2 / Redcar #3 / Middlesbrough #5.** Elite convergence on all four layers *and* the clearest new-demand story (Teesworks/Freeport, energy investment). Now the standout.
2. **Kingston upon Hull (#12, 0.875).** Top-tier convergence, a large deep market, and a real demand engine (Humber energy cluster, port, university).
3. **Doncaster (#22, 0.844).** Strong convergence with a genuine logistics/rail employment base and Sheffield city-region pull.
4. **Sunderland (#19, 0.850).** Strong convergence plus Riverside regeneration and automotive employment.
5. **Stoke-on-Trent (#20, 0.846).** Strong convergence with regeneration and affordability-led in-migration.

**Highest pure convergence, watch the demand:** **Burnley / Hyndburn / Pendle / Blackburn (East Lancs)** top the metric with very high yields but Manchester-fringe demand and old stock; **Grimsby / Scunthorpe / Rotherham / Barnsley** are close behind. **Blackpool (#17)** scores well but stays a *watch* for weak demand and poor older stock.

---

## Caveats (read before quoting)
- **Time base:** rents are Oct 2022–Sep 2023 (matched to the LHA base). Today's live market-vs-LHA gap is wider.
- **Geography:** LA→BRMA is exact-match + a curated candidate map; multi-BRMA LAs use the dominant BRMA (`geo=curated`). An official lookup would refine this and extend beyond 97 areas.
- **Social rent:** now **local per-bed** for 92/97 areas; 5 use the England fallback (flagged `soc_src=national`) — treat those (incl. Barrow #6, Scarborough #14) as slightly indicative.
- **Sample sizes:** ONS suppresses thin samples; `sample_min` is in the CSV — treat small-sample areas cautiously.
- **What this is:** a structural convergence screen, not a demand, yield or asset-quality model — pair it with Phase 7 of `METHODOLOGY.md`.
