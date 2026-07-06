# How to Check the Data Yourself — No Code Needed

This guide is for someone with **no programming experience**. It shows you how to go to the official websites, download the numbers, open them in an ordinary spreadsheet, read off the figures for any town, and even work out the "convergence" check by hand. If you can use a web browser and type into a spreadsheet cell, you can verify everything in this project without trusting anyone else's summary.

**You do not need Microsoft Excel.** Any of these free tools open the files:
- **Google Sheets** (free, in a browser — sheets.google.com)
- **LibreOffice Calc** (free download — libreoffice.org)
- Microsoft Excel if you have it.

Files you'll meet: **.csv** and **.xlsx** open in all of the above; **.ods** opens in Google Sheets and LibreOffice (and modern Excel).

**A note on finding pages:** website links change over time. If a link below doesn't work, go to **google.com** and paste the phrase in **bold** next to it — the official GOV.UK or ONS page is almost always the first result. Only trust pages ending in **gov.uk** or **ons.gov.uk** for the official figures.

---

## The four things you're checking

For any town you can look up four "rent levels" for 1-, 2- and 3-bedroom homes:

1. **Market rent** – what private landlords actually charge (from ONS).
2. **LHA** – the maximum housing benefit will pay (from the government/VOA).
3. **Affordable Rent** – you work this out yourself: **80% of the market rent**.
4. **Social rent** – the low, formula-based rent charged by councils/housing associations (from RSH).

"Convergence" just means these four numbers sit **close together**. That's the whole idea.

---

## STEP 1 — Market rent (ONS)

**What it is:** the middle ("median") monthly private rent, split by number of bedrooms, for each local council area.

1. In your browser search: **Private rental market summary statistics in England ONS**.
   Direct link: https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/privaterentalmarketsummarystatisticsinengland
2. On that page find the newest release and click the **download** button (it will be an **.xlsx** or **.ods** file). Save it, then open it in your spreadsheet program.
3. The workbook has several **tabs** (little labelled sheets along the bottom). You want the one broken down **by number of bedrooms** — the column headings will say things like **"One bedroom", "Two bedrooms", "Three bedrooms"**, and there will be a **"Median"** figure. Tab numbers change with each release, so pick the tab by those headings, not by a tab number.
4. Find your town in the list of **local authorities** (e.g. "Kingston upon Hull", "Stoke-on-Trent"). Read across to the **median** for 1, 2 and 3 bedrooms. **Ignore** any "Room", "Studio" or "Four or more" columns.
5. Write down the three numbers. Note the **period** shown at the top of the sheet (e.g. "12 months to September 2024") — you'll want it later.

> **Quick informal cross-check (optional):** on Rightmove or Zoopla you can search rentals in the town and eyeball whether asking prices are in the same ballpark. This is *not* the official figure (asking rents run higher than medians), just a sanity check.

---

## STEP 2 — LHA, the housing-benefit ceiling (easiest of all — no download)

**What it is:** the most that Housing Benefit / Universal Credit will pay towards rent in an area, by number of bedrooms.

**The no-download way (recommended):**
1. Go to **https://lha-direct.voa.gov.uk/** (search: **LHA Direct VOA** if the link moves).
2. Type in a **postcode** for the town (any real postcode there — a quick web search gives you one), or pick the area.
3. The page shows the weekly rates for **1 bedroom, 2 bedrooms, 3 bedrooms** (plus "shared" and "4 bedroom", which you ignore). Write down the three numbers.

**Important:** LHA is shown **per week**. Market rent (Step 1) is **per month**. To compare them, turn weekly into monthly: **multiply the weekly figure by 52, then divide by 12.**
Example: £101.92 per week × 52 ÷ 12 = **£441.65 per month** (about £442).

**The download way (if you want the whole country in one file):**
1. Search: **Local Housing Allowance rates GOV.UK collection**, or use https://www.gov.uk/government/collections/local-housing-allowance-lha-rates
2. Download the England rates file (a **.csv**) for the year you want. Open it in your spreadsheet.
3. Each row is a **"BRMA"** (Broad Rental Market Area) with monthly rates in columns by bedroom size. Find the BRMA covering your town.

> **Watch out:** LHA areas ("BRMAs") are **not** the same shape as council areas. One council can sit in a BRMA with a different name (e.g. Hull sits in the "Hull & East Riding" BRMA). LHA-Direct handles this for you when you type a postcode — that's why it's the easy route.
>
> **Also:** these LHA rates were set from rents collected up to **September 2023 and then frozen**. So if market rents have risen since, the LHA will look lower than today's market rent — that's expected, not an error.

---

## STEP 3 — Social rent (RSH)

**What it is:** the average low, formula-based rent for council/housing-association homes.

1. Search: **Registered provider social housing stock and rents in England GOV.UK** (latest year).
   Link: https://www.gov.uk/government/statistics/registered-provider-social-housing-stock-and-rents-in-england-2024-to-2025
2. On that page download the **"local authority" look-up tool** (an Excel file). Open it.
3. It usually has a **drop-down box**: click the cell, choose your council area, and the sheet shows that area's **average weekly general-needs (social) rent**. If there's no drop-down, find your council in the list.
4. This is also **per week** — turn it into monthly the same way (× 52 ÷ 12).
5. If your exact town isn't listed, use the **regional average** on the same page and note that you did. For reference, in 2024/25 the England average was **£113.69/week**, lowest in the **North East (£95.16)** and highest in **London (£140.70)**.

---

## STEP 4 — Demand and supply (MHCLG) — the "is anyone actually queuing?" check

Cheap, well-aligned rents only matter if people need the homes. These pages give you that picture (all searchable on GOV.UK):

- **Waiting lists:** search **Social housing lettings in England GOV.UK** → look for households on the local authority housing register.
- **Homelessness / temporary accommodation:** search **Statutory homelessness in England GOV.UK**.
- **How many new homes are being built:** search **Housing supply net additional dwellings England GOV.UK**.

You're just looking for whether the town has **a long waiting list / rising homelessness** (strong demand) and **low housebuilding** (tight supply). You don't need to calculate anything here — read the tables for your area and note "high / medium / low".

---

## STEP 5 — Do the convergence check by hand in a spreadsheet

Now put your numbers together. Open a blank spreadsheet and copy this simple layout. **You only type the numbers you looked up (the white cells); the formulas do the rest.**

Type these labels and your looked-up **monthly** figures:

|   | A | B | C | D |
|---|---|---|---|---|
| **1** | (leave blank) | 1 bed | 2 bed | 3 bed |
| **2** | Market rent (Step 1) | *type it* | *type it* | *type it* |
| **3** | LHA monthly (Step 2) | *type it* | *type it* | *type it* |
| **4** | Affordable rent | `=B2*0.8` | `=C2*0.8` | `=D2*0.8` |
| **5** | LHA ÷ Market | `=B3/B2` | `=C3/C2` | `=D3/D2` |

**How to type a formula:** click the cell, type the text exactly as shown starting with the **=** sign (e.g. `=B2*0.8`), then press **Enter**. The cell shows the answer, not the text.

Now read the results:

- **Row 4 (Affordable rent)** should be **at or below** the LHA in Row 3. If Affordable Rent ≤ LHA, a benefit tenant can cover it — a strong convergence sign.
- **Row 5 (LHA ÷ Market)** tells you how close LHA is to market rent. **0.80 or higher = well aligned** (converged). Around 0.60 or lower = a big gap (not converged). To get a single number, in an empty cell type `=AVERAGE(B5:D5)`.
- **Social rent close to market?** In an empty cell type `=SocialMonthly/AVERAGE(B2:D2)` (replace "SocialMonthly" with the number from Step 3). The **higher** this is, the less detached social rent is. In cheap northern/midlands areas it's often ~0.5–0.6; in London it can be ~0.25.
- **Are the 1/2/3-bed rents tightly bunched?** In an empty cell type `=STDEV(B2:D2)/AVERAGE(B2:D2)`. A **smaller** number means the rents are more consistent (more converged).

That's the entire method. An area scores well if: Affordable Rent sits near/under LHA, LHA÷Market is high, social rent is a decent share of market, and the three bed sizes are bunched together — **and** Step 4 showed real demand.

---

## Worked example you can copy (Hull LHA is real; market rent is a placeholder to show the mechanics)

Hull & East Riding **LHA** (weekly, from LHA-Direct): 1 bed £101.92, 2 bed £126.92, 3 bed £150.00.
Turn into monthly: **£442, £550, £650**.

Put those in Row 3. Then look up Hull's **market** medians from Step 1 and put the real numbers in Row 2 (the figures below are only an illustration of the arithmetic — **replace them with what you find**):

|   | 1 bed | 2 bed | 3 bed |
|---|---|---|---|
| Market rent (look this up!) | *e.g.* 500 | *e.g.* 575 | *e.g.* 675 |
| LHA monthly (real) | 442 | 550 | 650 |
| Affordable (=Market×0.8) | 400 | 460 | 540 |
| LHA ÷ Market | 0.88 | 0.96 | 0.96 |

In this illustration Affordable Rent (400/460/540) is **below** LHA (442/550/650) — fully coverable — and LHA÷Market averages ~0.93, i.e. very close. That's what a **converged** market looks like. Do the same with the real ONS numbers to confirm.

---

## Keeping yourself honest (a short checklist)

- ✅ **Only trust gov.uk / ons.gov.uk** for the four rent/demand figures.
- ✅ **Match the weeks and months** — LHA and social rent are weekly; convert before comparing.
- ✅ **Note the dates** — market rent is a recent 12-month period; LHA is frozen from Sept 2023. They won't line up perfectly, and that's the point (the gap grows as market rents rise).
- ✅ **Remember LHA areas ≠ council areas** — if in doubt, use LHA-Direct with a postcode.
- ✅ **Write down every source and date** next to each number, so anyone can retrace your steps.
- ⚠️ If a figure looks odd (e.g. a 1-bed dearer than a 3-bed), it's usually a small-sample quirk in that town — note it rather than relying on it.

---

### Optional: checking a housing provider (if you go that far)
To verify a housing association's health, search **Regulator of Social Housing regulatory judgements GOV.UK**, find the provider, and read its **Governance (G)**, **Viability (V)** and **Consumer (C)** grades — **1 is best**. Councils' own housing arms (ALMOs) and very small providers may not have these grades; that's normal.
