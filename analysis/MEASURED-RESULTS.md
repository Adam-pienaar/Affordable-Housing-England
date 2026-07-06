# Measured Convergence Ranking — Results

This is the **measured** version of the analysis, computed from the three official datasets supplied (in `analysis/data/`), not the earlier pattern-based read. Reproduce it with `python analysis/run_measured_ranking.py` → `analysis/measured_convergence_ranking.csv`.

## Data used
- **Market rent:** ONS/VOA Private Rental Market Statistics, **median monthly rent by bedroom, by local authority**, for **Oct 2022 – Sep 2023** (Tables 2.3/2.4/2.5).
- **LHA:** DWP/VOA LHA Table 1 — **April-2024 rates, weekly**, carried forward (frozen) to 2026/27; categories B/C/D = 1/2/3-bed. Converted to monthly ×52/12.
- **Social rent:** RSH 2024/25 — England general-needs average **£113.69/wk** used as a **national benchmark** (per-LA social rents are in a separate RSH file that was not supplied).
- **Affordable Rent:** derived = 80% × market.

**Why this pairing is clean:** the ONS rent window (Oct 2022–Sep 2023) is the *same* 12 months the frozen LHA is derived from, so this measures **structural convergence at the LHA reference point** — it removes the "freeze erosion" that widens today's live gap. It is not today's live market-vs-LHA gap (that is wider, because market rents have risen since Sep 2023).

**Coverage:** 97 local authorities scored — those with a reliable ONS median for all of 1/2/3-bed **and** a defensible LA→BRMA match (exact-name matches plus a curated map for the candidate areas). A full national run needs the official LA→BRMA lookup (not supplied); multi-BRMA LAs use their dominant BRMA and are flagged `geo=curated`.

---

## Headline: the thesis holds, the order changes

**Every one of the top 25 is a low-cost North / Midlands market; the least-converged are all high-rent South** (Cambridge, Brighton, Oxford, Bristol, Guildford, Reading). The regional prediction from the mechanism is confirmed by the data.

### Top 20 (measured)

| Rank | Area | BRMA | Market 2-bed | LHA 2-bed | Score |
|---|---|---|---|---|---|
| 1 | Burnley | East Lancs | £475 | £474 | 0.966 |
| 2 | Hartlepool | Teesside | £500 | £474 | 0.956 |
| 3 | Hyndburn | East Lancs | £495 | £474 | 0.942 |
| 4 | South Tyneside | Tyneside | £500 | £549 | 0.940 |
| 5 | **Kingston upon Hull** | Hull & East Riding | £495 | £474 | 0.933 |
| 6 | Pendle | East Lancs | £520 | £474 | 0.929 |
| 7 | North East Lincs (Grimsby) | Grimsby | £525 | £479 | 0.927 |
| 8 | Rotherham | Rotherham | £550 | £499 | 0.924 |
| 9 | Redcar & Cleveland | Teesside | £510 | £474 | 0.922 |
| 10 | County Durham | Durham | £450 | £399 | 0.921 |
| 11 | North Lincolnshire (Scunthorpe) | Scunthorpe | £525 | £494 | 0.920 |
| 12 | Gateshead | Tyneside | £580 | £549 | 0.914 |
| 13 | Blackburn with Darwen | East Lancs | £524 | £474 | 0.913 |
| 14 | Middlesbrough | Teesside | £525 | £474 | 0.913 |
| 15 | Blackpool | Fylde Coast | £550 | £540 | 0.909 |
| 16 | **Stoke-on-Trent** | Staffordshire North | £515 | £479 | 0.908 |
| 17 | **Doncaster** | Doncaster | £550 | £499 | 0.906 |
| 18 | Darlington | Darlington | £500 | £449 | 0.900 |
| 19 | Barnsley | Barnsley | £500 | £449 | 0.893 |
| 20 | Sunderland | Sunderland | £550 | £474 | 0.891 |

Least converged (bottom 5 of 97): Cambridge 0.662, Brighton & Hove 0.682, Oxford 0.691, Bristol 0.697, Exeter 0.719.

---

## The real mechanism (a subtlety the data exposes)

You might expect "LHA close to market" to be the northern signature. **It isn't** — LHA-to-market **alignment is high almost everywhere**, because LHA is set at the 30th percentile of each area's own distribution. Even **Guildford** scores 0.94 on alignment.

What actually separates converged from non-converged areas is **social-rent attachment** — social rent (near-uniform nationally) sits close to market rent **only where market rent is low**:

| | Alignment (LHA vs market) | Social attachment (social ÷ market) | Overall |
|---|---|---|---|
| Hull (North) | 0.93 | **0.99** | converged |
| Guildford (South) | 0.94 | **0.37** | not converged |

So **four-layer convergence requires social rent to be near market, which only happens in low-rent areas.** That is the genuine insight, and it's exactly the structural argument the pattern-based report made — now demonstrated with numbers.

> **Honest caveat on this component:** because per-LA social rents weren't supplied, social attachment here uses the England-average social rent as a fixed benchmark. That makes it partly a "how cheap is this market" proxy. Supply the RSH per-LA social-rent file and the script will use true local social rents, sharpening this component. The *alignment* and *compression* components already use fully local data.

---

## How the measured order revises the pattern-based list

| My earlier read | Measured | Verdict |
|---|---|---|
| Hull #2 | **#5** | ✅ Confirmed top-tier |
| Doncaster #5 | **#17** | ✅ Close, confirmed |
| Stoke-on-Trent #1 | **#16** | ➖ Strong (0.908) but not the single best; its rents are a touch higher/wider than the cheapest East-Lancs/Teesside towns |
| Teesside (Middlesbrough) #3 | Hartlepool **#2**, Redcar **#9**, Middlesbrough **#14** | ✅ Teesside cluster confirmed strong |
| Wolverhampton / Black Country #6 | **#38–60** | ❌ Over-ranked. West-Midlands rents & LHA are higher and social attachment lower, so pure convergence is weaker than I claimed (the *demand* case stays valid, but that's a different axis) |
| Burnley / East Lancs #15 | **#1, #3, #6, #13** | ⬆️ Under-ranked. East Lancashire is the standout convergence cluster |
| Hartlepool #18, Rotherham #17 | **#2, #8** | ⬆️ Under-ranked |
| Blackpool (demoted) | **#15 on the metric** | ⚠️ Confirms the point: high convergence *score*, but I demoted it for weak demand / poor stock — the metric measures rent alignment, not demand or asset quality |

**Net:** the *pattern* (low-cost North/Midlands) was right; my specific *ordering* leaned too heavily on regeneration narratives (Black Country, Stoke) and under-weighted the genuinely cheapest, tightest markets (East Lancashire, Hartlepool, Rotherham).

---

## A defensible revised Top 5 (convergence **plus** demand)

Convergence score alone would crown East Lancashire — but investment needs demand too. Balancing the measured score against demand/regeneration and stock-quality risk:

1. **Kingston upon Hull (#5, 0.933)** — top-tier convergence *and* a real demand engine (Humber energy cluster, port, university). Best all-round.
2. **Teesside — Hartlepool #2 / Middlesbrough #14 / Redcar #9** — elite convergence with the clearest new-demand story (Teesworks/Freeport).
3. **Doncaster (#17, 0.906)** — strong convergence with genuine logistics/rail employment and Sheffield city-region pull.
4. **Rotherham (#8, 0.924) / Barnsley (#19, 0.893)** — very tight convergence inside the Sheffield city-region labour market.
5. **Stoke-on-Trent (#16, 0.908)** — strong convergence plus regeneration and affordability-led in-migration.

**Highest pure convergence, watch the demand:** **Burnley / Hyndburn / Pendle / Blackburn (East Lancs)** top the metric and offer very high yields, but demand is Manchester-fringe and stock is old — excellent for benefit-aligned rent risk, thinner on capital growth. **Blackpool (#15)** scores well but stays a *watch* for weak demand and poor older stock.

---

## Caveats (read before quoting these numbers)
- **Time base:** rents are Oct 2022–Sep 2023 (matched to the LHA base). Today's live market-vs-LHA gap is wider.
- **Geography:** LA→BRMA is exact-match + a curated candidate map; multi-BRMA LAs (e.g. County Durham, East Riding) use the dominant BRMA and are flagged. An official lookup would refine this.
- **Social rent:** national benchmark, not per-LA (see caveat above).
- **Sample sizes:** ONS suppresses thin samples; `sample_min` is in the CSV — treat small-sample areas cautiously.
- **What this is:** a structural convergence screen. It is not a demand, yield or asset-quality model — pair it with Phase 7 of `METHODOLOGY.md`.
