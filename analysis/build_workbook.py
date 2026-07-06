#!/usr/bin/env python3
"""Build the rent-convergence Excel workbook from the analysis content.

Keeps structured/tabular data (rankings, metric definitions, verified anchors,
sources) and omits long-form prose. Run: python analysis/build_workbook.py
"""
import os
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

OUT = "analysis/uk-rent-convergence-analysis.xlsx"

# --- styling helpers ---------------------------------------------------------
HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
TITLE_FONT = Font(bold=True, size=14, color="1F4E78")
NOTE_FONT = Font(italic=True, size=9, color="595959")
TOP_FILL = PatternFill("solid", fgColor="E2EFDA")
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="top")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def _num(v):
    """Convert a CSV string to int/float where possible, else pass through."""
    try:
        f = float(v)
        return int(f) if f == int(f) else f
    except (ValueError, TypeError):
        return v


def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        cell.border = BORDER


def write_table(ws, start_row, headers, rows, widths, wrap_cols=(), highlight_top=0):
    style_header(ws, start_row, len(headers))
    for j, h in enumerate(headers, 1):
        ws.cell(row=start_row, column=j, value=h)
    for i, row in enumerate(rows, 1):
        r = start_row + i
        for j, val in enumerate(row, 1):
            cell = ws.cell(row=r, column=j, value=val)
            cell.border = BORDER
            cell.alignment = WRAP if j in wrap_cols else Alignment(vertical="top")
            if highlight_top and i <= highlight_top:
                cell.fill = TOP_FILL
    for j, w in enumerate(widths, 1):
        ws.column_letter = get_column_letter(j)
        ws.column_dimensions[get_column_letter(j)].width = w
    return start_row + len(rows) + 1


def title(ws, text, row=1, span=1):
    ws.cell(row=row, column=1, value=text).font = TITLE_FONT
    if span > 1:
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span)


wb = Workbook()

# ============================ Sheet 1: Ranked areas ==========================
ws = wb.active
ws.title = "Ranked Convergence Areas"
title(ws, "England 1-3 Bed Rent Convergence - Ranked Areas (pattern-based)", 1, 6)
ws.cell(row=2, column=1,
        value="Ranked by convergence strength combined with demand/shortage. "
              "Studios and shared accommodation excluded. Ordering is directional; "
              "run convergence_analysis.py for exact per-area scores.").font = NOTE_FONT
ws.merge_cells("A2:F2")
ws.row_dimensions[2].height = 30

headers = ["Rank", "Area (BRMA / LA)", "Region", "Why rents converge",
           "Demand drivers", "Key risks"]
rows = [
    [1, "Stoke-on-Trent", "W Mids",
     "Very low, tightly-clustered rents; LHA sits close to market; Affordable Rent (80%) approx LHA",
     "Affordable-city in-migration, ceramics/logistics jobs, city-centre regeneration",
     "Pockets of low-demand terraced stock; deprivation; benefit-tenant reliance"],
    [2, "Kingston upon Hull & East Riding", "Yorks & Humber",
     "Measured #5 of 97. LHA close to market (2-bed 474 vs 495/mo; align 0.96); tight 1-3 bed spread",
     "Humber offshore-wind/energy cluster, port, university, regeneration",
     "Localised low demand in older stock; flood-zone constraints"],
    [3, "Teesside (Middlesbrough/Stockton/Redcar)", "North East",
     "Among lowest rents in England; LHA approx market; social rent a high share",
     "Teesworks / Teesside Freeport, energy & process-industry investment",
     "Deprivation pockets; demand concentrated near regeneration sites"],
    [4, "Sunderland", "North East",
     "Low, compressed rents; strong social/market ratio",
     "Riverside Sunderland regeneration, automotive supply chain, jobs growth",
     "Peripheral estates weak-demand; single-employer exposure"],
    [5, "Doncaster", "Yorks & Humber",
     "Low rents; LHA well-aligned; modest dispersion",
     "Rail/logistics (Gateway), airport-site redevelopment, Sheffield city-region",
     "Post-industrial low-demand pockets"],
    [6, "Wolverhampton / Black Country (Sandwell, Walsall, Dudley)", "W Mids",
     "Low-to-moderate rents, compressed; large benefit-backed demand",
     "Very large waiting lists, WM conurbation jobs, HS2/interchange regeneration",
     "Stock-condition & management-intensity; deprivation"],
    [7, "Wigan", "North West",
     "Low rents; Greater Manchester overspill keeps demand firm",
     "GM commuter demand, employment growth, town-centre regen",
     "Rising rents narrowing the LHA gap over time"],
    [8, "Grimsby / North-East Lincolnshire", "Yorks & Humber",
     "Very low rents; LHA close to market",
     "Humber renewables/port jobs, town-deal regeneration",
     "Thin market; concentrated deprivation"],
    [9, "Mansfield / Ashfield (North Notts)", "E Mids",
     "Low, compressed rents; strong LHA alignment",
     "Nottingham/Derby commuter demand, logistics corridor",
     "Smaller market depth"],
    [10, "Barnsley", "Yorks & Humber",
     "Low rents; tight spread; high social/market share",
     "Sheffield city-region jobs, town-centre regeneration",
     "Low-demand older terraces in places"],
    [11, "County Durham (Durham BRMA)", "North East",
     "Low rents outside the small student core; social rent high share",
     "Large stock, university & public-sector employment",
     "Durham City student core distorts sub-areas"],
    [12, "Darlington", "North East",
     "Low rents; well-aligned LHA",
     "Darlington Economic Campus (Treasury North) civil-service jobs",
     "Small market; single policy-led demand driver"],
    [13, "Wakefield", "Yorks & Humber",
     "Low-moderate rents; compressed",
     "Leeds city-region commuter demand, logistics",
     "Rent growth eroding LHA gap"],
    [14, "Bradford", "Yorks & Humber",
     "Low rents; large benefit-backed demand",
     "Young/growing population, City of Culture legacy, Leeds proximity",
     "Deprivation; stock condition"],
    [15, "Burnley / Pennine Lancashire (East Lancs)", "North West",
     "Among the lowest rents nationally; LHA approx market",
     "Manchester-fringe demand, manufacturing",
     "Very low capital values; weak-demand micro-markets"],
    [16, "Blackburn with Darwen", "North West",
     "Very low, compressed rents",
     "Young population growth, M65 corridor jobs",
     "Deprivation; demand localised"],
    [17, "Rotherham", "Yorks & Humber",
     "Low rents; high social/market ratio",
     "Sheffield city-region, advanced-manufacturing park",
     "Post-industrial low-demand pockets"],
    [18, "Hartlepool", "North East",
     "Very low rents; LHA close to market",
     "Freeport/energy spillover, port",
     "Thin, deprivation-heavy market; demand risk"],
    [19, "Leicester", "E Mids",
     "Moderate rents but very strong benefit demand; reasonable alignment",
     "Large diverse population, universities, big waiting list",
     "Higher dispersion than northern peers; supply pressure raising rents"],
    [20, "Derby", "E Mids",
     "Moderate, fairly compressed rents",
     "Rolls-Royce/Alstom/rail & nuclear-supply jobs, strong employment",
     "Rent growth narrowing gap; higher entry prices"],
    [21, "Liverpool", "North West",
     "Moderate rents; strong demand; decent social/market share",
     "Universities, health/knowledge economy, large-scale regeneration",
     "City-centre new-build oversupply in some segments"],
    [22, "Preston (Central Lancs)", "North West",
     "Low-moderate, compressed rents",
     "University, Preston City Deal infrastructure/jobs",
     "Student-segment distortion"],
]
next_row = write_table(ws, 4, headers, rows,
                       widths=[6, 34, 16, 44, 40, 38],
                       wrap_cols=(2, 4, 5, 6), highlight_top=5)
ws.cell(row=next_row + 1, column=1,
        value="Top 5 rows shaded. Excluded from top ranking despite affordability: "
              "Blackpool (aligned but chronic low demand / rent-risk) and "
              "Birmingham (high demand but higher, more dispersed rents).").font = NOTE_FONT
ws.merge_cells(start_row=next_row + 1, start_column=1, end_row=next_row + 1, end_column=6)
ws.row_dimensions[next_row + 1].height = 30
ws.freeze_panes = "A5"

# ============================ Sheet 2: Top 5 =================================
ws2 = wb.create_sheet("Top 5 Opportunities")
title(ws2, "Top 5 Strongest Investment Opportunities", 1, 4)
h2 = ["Rank", "Area", "Convergence rationale", "Watch"]
r2 = [
    [1, "Stoke-on-Trent",
     "Very low, tightly-clustered 1-3 bed rents; LHA close to market and Affordable Rent (80%) near LHA, so benefit-backed tenancies are reliably coverable; regeneration + affordability-led in-migration.",
     "Concentration of weak-demand terraced stock - buy in sound sub-markets."],
    [2, "Kingston upon Hull & East Riding",
     "Only fully-sourced anchor: LHA approx market across 1-3 beds; social rent a high share of market; Humber energy/port cluster + university underpin demand.",
     "Flood-zone and older-stock demand pockets."],
    [3, "Teesside (Middlesbrough/Stockton/Redcar)",
     "England's lowest-rent tier so alignment on all four layers is strong; clearest new-demand story via Teesworks/Freeport and energy investment.",
     "Keep close to regeneration footprint; avoid deprived peripheral estates."],
    [4, "Wolverhampton / Black Country",
     "Low-to-moderate, compressed rents with some of the largest benefit-backed demand/waiting lists in England inside a major conurbation labour market; depth of demand lowers void risk.",
     "Stock condition and higher management intensity."],
    [5, "Doncaster",
     "Low, well-aligned rents with a genuine logistics/rail employment engine and Sheffield city-region spillover - convergence plus a growth driver.",
     "Post-industrial low-demand micro-markets."],
]
write_table(ws2, 3, h2, r2, widths=[6, 30, 70, 40], wrap_cols=(2, 3, 4), highlight_top=5)
ws2.cell(row=3 + len(r2) + 2, column=1,
         value="Honourable mentions: Sunderland (Riverside regeneration) and Wigan "
               "(Greater Manchester overspill) - interchangeable with #4-#5 depending "
               "on exact per-area scores.").font = NOTE_FONT
ws2.merge_cells(start_row=3 + len(r2) + 2, start_column=1, end_row=3 + len(r2) + 2, end_column=4)
ws2.row_dimensions[3 + len(r2) + 2].height = 28

# ============================ Sheet 3: Metric ================================
ws3 = wb.create_sheet("Convergence Metric")
title(ws3, "Convergence Metric (1-3 bed only, monthly GBP)", 1, 4)
h3 = ["Component", "Definition", "Converged when", "Weight"]
r3 = [
    ["LHA-market alignment", "mean over b in {1,2,3} of min(LHA_b / Market_b, 1)",
     "-> 1.0 (LHA close to market)", 0.40],
    ["Social-rent attachment", "Social_monthly / mean(Market_1, Market_2, Market_3)",
     "higher = less detached", 0.30],
    ["Rent compression", "1 - CV(Market_1, Market_2, Market_3); CV = stdev/mean",
     "higher = tighter spread", 0.30],
    ["Affordable-vs-LHA cover (diagnostic)",
     "Affordable_b = 0.80 x Market_b; mean of min(LHA_b / Affordable_b, 1)",
     "-> 1.0 (LHA >= 80% market). High iff alignment >= 0.80.", "n/a"],
]
nr = write_table(ws3, 3, h3, r3, widths=[34, 52, 40, 10], wrap_cols=(1, 2, 3))
ws3.cell(row=nr + 1, column=1,
         value="Composite score = 0.40*alignment + 0.30*social_attachment + 0.30*compression. "
               "Constants: Affordable Rent = 80% of market (statutory); weekly->monthly = x52/12. "
               "A demand/shortage overlay prioritises investable convergence.").font = NOTE_FONT
ws3.merge_cells(start_row=nr + 1, start_column=1, end_row=nr + 1, end_column=4)
ws3.row_dimensions[nr + 1].height = 42

# Worked selftest illustration (from convergence_analysis.py --selftest)
nr += 3
ws3.cell(row=nr, column=1, value="Worked illustration (synthetic, from script selftest):").font = Font(bold=True)
hx = ["Market type", "align", "afford_cover", "social_attach", "compression", "score"]
rx = [
    ["Converged low-cost market", 0.938, 1.000, 0.748, 0.894, 0.867],
    ["Detached expensive market (London-like)", 0.627, 0.784, 0.277, 0.757, 0.561],
]
write_table(ws3, nr + 1, hx, rx, widths=[38, 10, 14, 14, 14, 10])

# ============================ Sheet 4: Verified anchors ======================
ws4 = wb.create_sheet("Verified Data Anchors")
title(ws4, "Verified Data Anchors (published figures used in the analysis)", 1, 4)
h4 = ["Metric", "Value", "Period", "Source (see Sources sheet)"]
r4 = [
    ["Avg weekly general-needs social rent, England", "GBP 113.69", "2024/25", "RSH (3)"],
    ["Social rent - lowest region (North East)", "GBP 95.16 / wk", "2024/25", "RSH (3)"],
    ["Social rent - highest region (London)", "GBP 140.70 / wk", "2024/25", "RSH (3)"],
    ["Social rent annual increase", "+8%", "2023/24 -> 2024/25", "RSH (3)"],
    ["Lowest-rent region (market), England", "North East approx GBP 641/mo (FYE24); GBP 694 (Oct24)", "2024", "ONS (4)(5)"],
    ["Next most affordable regions", "East Midlands, then Yorkshire & The Humber", "2024", "ONS (5)"],
    ["Highest-rent region (market)", "London approx GBP 2,172/mo", "Oct 2024", "ONS (4)"],
    ["LHA basis", "30th percentile of local market rents to 30 Sep 2023", "2024/25", "DWP/VOA (1)"],
    ["LHA status 2025/26", "Frozen at 2024/25 levels", "2025/26", "GOV.UK (2)"],
    ["Hull & East Riding LHA - 1 bed", "GBP 87.45 / wk (approx GBP 379/mo)", "Apr-2024 base", "DWP/VOA LHA file (6)"],
    ["Hull & East Riding LHA - 2 bed", "GBP 109.32 / wk (approx GBP 474/mo)", "Apr-2024 base", "DWP/VOA LHA file (6)"],
    ["Hull & East Riding LHA - 3 bed", "GBP 126.58 / wk (approx GBP 549/mo)", "Apr-2024 base", "DWP/VOA LHA file (6)"],
    ["Hull market median (1/2/3 bed)", "GBP 425 / 495 / 575 per month", "Oct22-Sep23", "ONS PRMS (supplied)"],
    ["Households on LA housing registers", "1.33 million (highest since 2014)", "31 Mar 2024", "MHCLG (7)"],
    ["London share of national register", "approx 25%", "2024", "MHCLG (7)"],
    ["Households in temporary accommodation", "130,890 (+11.5% YoY)", "31 Mar 2025", "MHCLG (8)"],
]
write_table(ws4, 3, h4, r4, widths=[46, 52, 22, 28], wrap_cols=(1, 2, 4))

# ============================ Sheet 5: Sources ===============================
ws5 = wb.create_sheet("Sources")
title(ws5, "Sources", 1, 3)
h5 = ["Ref", "Publication", "URL"]
r5 = [
    ["1", "GOV.UK / DWP - Indicative LHA rates for 2024 to 2025 (30th-percentile basis)",
     "https://www.gov.uk/government/statistics/local-housing-allowance-indicative-rates-for-2024-to-2025/indicative-local-housing-allowance-rates-for-2024-to-2025"],
    ["2", "GOV.UK - LHA rates applicable from April 2025 to March 2026 (frozen)",
     "https://www.gov.uk/government/publications/local-housing-allowance-lha-rates-applicable-from-april-2025-to-march-2026"],
    ["3", "RSH - Registered provider social housing stock and rents in England 2024 to 2025",
     "https://www.gov.uk/government/statistics/registered-provider-social-housing-stock-and-rents-in-england-2024-to-2025"],
    ["4", "ONS - Private rent and house prices, UK: October 2024",
     "https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/privaterentandhousepricesuk/october2024"],
    ["5", "ONS - Private rental affordability, England, Wales and Northern Ireland: 2024",
     "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/bulletins/privaterentalaffordabilityengland/2024"],
    ["6", "GOV.UK / VOA - Local Housing Allowance rates collection (Hull & East Riding BRMA)",
     "https://www.gov.uk/government/collections/local-housing-allowance-lha-rates"],
    ["7", "GOV.UK - Social housing lettings in England, tenants: April 2023 to March 2024",
     "https://www.gov.uk/government/statistics/social-housing-lettings-in-england-april-2023-to-march-2024/social-housing-lettings-in-england-tenants-april-2023-to-march-2024"],
    ["8", "GOV.UK - Statutory homelessness in England: financial year 2024-25",
     "https://www.gov.uk/government/statistics/statutory-homelessness-in-england-financial-year-2024-25/statutory-homelessness-in-england-financial-year-2024-25"],
    ["Primary market dataset", "ONS - Private Rental Market Summary Statistics in England (median monthly rent by bedroom/LA)",
     "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/privaterentalmarketsummarystatisticsinengland"],
]
write_table(ws5, 3, h5, r5, widths=[14, 60, 70], wrap_cols=(2, 3))
nr5 = 3 + len(r5) + 2
ws5.cell(row=nr5, column=1,
         value="Note: per-area rankings are pattern-based, grounded in the verified regional "
               "mechanism; no per-area rents were fabricated. Full per-BRMA LHA and per-LA ONS "
               "medians could not be machine-downloaded in the drafting environment "
               "(gov.uk/ONS blocked); convergence_analysis.py recomputes exact scores on the live data.").font = NOTE_FONT
ws5.merge_cells(start_row=nr5, start_column=1, end_row=nr5, end_column=3)
ws5.row_dimensions[nr5].height = 56

# ============================ Sheet 6: Area providers ========================
ws6 = wb.create_sheet("Top 5 Area Providers")
title(ws6, "Operators active in this revenue stream - Top 5 areas", 1, 5)
ws6.cell(row=2, column=1,
         value="Registered providers (RPs), council ALMOs and for-profit build-to-rent (BTR) "
               "operators currently delivering social & affordable rent (incl. Affordable Rent "
               "at 80% of market) in each area. Most are not-for-profit RPs - the dominant "
               "operators of this stream. Verified via public/council sources (Sept 2024-2026).").font = NOTE_FONT
ws6.merge_cells("A2:E2")
ws6.row_dimensions[2].height = 42

h6 = ["Area", "Organisation", "Type", "Homes (approx)", "G", "V", "C",
      "Notes (relevance / RSH judgement / development)"]
r6 = [
    # Stoke-on-Trent
    ["Stoke-on-Trent", "Aspire Housing", "RP", "~9,300", "G1", "V2", "C1",
     "North Staffs/Stoke & Cheshire; developing new affordable homes; in merger talks with whg (~32,000-home group). RJ Nov 2025."],
    ["Stoke-on-Trent", "Honeycomb Group (incl. Staffs Housing)", "RP / charity", "~3,118", "n/v", "n/v", "n/v",
     "Affordable housing & support across Staffs, Cheshire, Derbyshire. RSH judgement Oct 2025 (grades not captured this pass)."],
    ["Stoke-on-Trent", "Stoke-on-Trent Housing Society", "RP (charitable)", "621", "—", "—", "—",
     "Under 1,000 homes: not individually graded by RSH. Actively builds new homes in the city."],
    ["Stoke-on-Trent", "EPIC Housing", "RP (community)", "~1,400", "n/v", "n/v", "n/v",
     "Affordable rents across Stoke, Newcastle-under-Lyme and Staffordshire Moorlands."],
    # Hull & East Riding
    ["Kingston upon Hull & East Riding", "Riverside", "RP (large national)", "~75,000*", "G1", "V2", "n/v",
     "Dedicated Hull operations (rent + care). RJ Mar 2024: G1 upgrade, V2 retained. *widely-reported total, confirm."],
    ["Kingston upon Hull & East Riding", "Pickering & Ferens Homes (PFH)", "RP", "~1,400", "n/v", "n/v", "n/v",
     "Older-persons affordable housing across Hull & East Riding."],
    ["Kingston upon Hull & East Riding", "Hull Churches Housing Association", "RP (independent)", "~500", "—", "—", "—",
     "Under 1,000 homes: not individually graded. Social rent & shared ownership in Hull and adjoining East Riding."],
    ["Kingston upon Hull & East Riding", "Sanctuary", "RP (large national)", "~120,000*", "G1", "V2", "C2",
     "Hull office/presence. C2 from planned inspection Jan 2025. *widely-reported total, confirm."],
    # Teesside
    ["Teesside (Middlesbrough/Stockton/Redcar)", "Thirteen Group", "RP", "~34,000", "G1", "V1", "C1",
     "Teesside's largest social landlord and an active developer. C1 from inspection Mar 2025."],
    ["Teesside (Middlesbrough/Stockton/Redcar)", "Beyond Housing", "RP", "~15,350", "G1", "V1", "n/v",
     "Redcar/Tees Valley; core Tees Valley Homefinder partner. G1 upgrade Mar 2024."],
    ["Teesside (Middlesbrough/Stockton/Redcar)", "North Star Housing Group", "RP", "~4,000", "G1", "V1", "n/v",
     "Stockton-based; Tees Valley partnership. RJ Dec 2024."],
    ["Teesside (Middlesbrough/Stockton/Redcar)", "The PRS REIT", "For-profit BTR", "~5,000+ (n/v)", "—", "—", "—",
     "For-profit provider outside the standard G/V regime; single-family build-to-rent active in Teesside."],
    # Wolverhampton / Black Country
    ["Wolverhampton / Black Country", "whg (Walsall Housing Group)", "RP (large)", "~21,000", "G1", "V1", "n/v",
     "Walsall HQ. Royal Hospital scheme = 154 affordable-rent/shared-ownership homes; reports top grade after inspection."],
    ["Wolverhampton / Black Country", "Bromford", "RP (large / developer)", "~47,000", "G1", "V1", "n/v",
     "Wolverhampton HQ; major developer ('Homes for the West Midlands'). LiveWest merger reported early 2026 - combined scale to confirm."],
    ["Wolverhampton / Black Country", "Black Country Housing Group (BCHG)", "RP", ">2,000", "G1", "V1", "n/v",
     "Black Country RP providing affordable rented homes and support."],
    ["Wolverhampton / Black Country", "Wolverhampton Homes", "Council ALMO", "~21,000 (managed)", "—", "—", "n/v",
     "Manages City of Wolverhampton Council stock; council holds the provider registration (not separately G/V graded); subject to consumer standards."],
    # Doncaster
    ["Doncaster", "St Leger Homes of Doncaster", "Council ALMO", "~20,000 (managed)", "—", "—", "n/v",
     "ALMO for City of Doncaster Council (council holds registration; subject to consumer standards). Runs Choice Based Lettings."],
    ["Doncaster", "Together Housing", "RP (large)", "~36,000", "G1", "V2", "n/v",
     "Delivering new affordable homes in Doncaster (2024 scheme with Housing 21). Viability regraded V1->V2."],
    ["Doncaster", "Housing 21", "RP (older-persons)", "~23,300", "G1", "V1", "C1",
     "Retirement/ExtraCare across ~240 LAs; partnering on affordable-homes delivery in Doncaster."],
]
nr6 = write_table(ws6, 4, h6, r6, widths=[30, 32, 20, 15, 5, 5, 5, 60],
                  wrap_cols=(1, 2, 3, 8))
for c in (5, 6, 7):  # centre the grade columns
    for rr in range(5, 5 + len(r6)):
        ws6.cell(row=rr, column=c).alignment = CENTER
# legend
leg = ("Legend: G=governance, V=viability, C=consumer (RSH grades; 1=strongest). "
       "n/v = not verified in this pass. — = not applicable (ALMO: the council holds "
       "the provider registration; or under-1,000-home RP not individually graded; or "
       "for-profit outside the G/V regime). * = widely-reported round figure, confirm. "
       "Grades change - re-check current RSH regulatory judgements before relying on them.")
ws6.cell(row=nr6, column=1, value=leg).font = NOTE_FONT
ws6.merge_cells(start_row=nr6, start_column=1, end_row=nr6, end_column=8)
ws6.row_dimensions[nr6].height = 56
nr6 += 1
# shade alternating area blocks for readability
block_starts = {}
for i, row in enumerate(r6):
    block_starts.setdefault(row[0], []).append(i)
shade = False
seen = set()
for i, row in enumerate(r6):
    if row[0] not in seen:
        seen.add(row[0]); shade = not shade
    if shade:
        for c in range(1, 9):
            ws6.cell(row=5 + i, column=c).fill = PatternFill("solid", fgColor="F2F2F2")
ws6.freeze_panes = "A5"
ws6.cell(row=nr6 + 1, column=1,
         value="Note: this maps who is active in the stream, not an endorsement or a claim of "
               "current tenders. RP = Registered Provider; ALMO = Arm's Length Management "
               "Organisation. Verify current pipeline/JV appetite directly before acting.").font = NOTE_FONT
ws6.merge_cells(start_row=nr6 + 1, start_column=1, end_row=nr6 + 1, end_column=8)
ws6.row_dimensions[nr6 + 1].height = 40

# ============================ Sheet 7: Measured ranking ======================
CSVP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "measured_convergence_ranking.csv")
if os.path.exists(CSVP):
    ws7 = wb.create_sheet("Measured Ranking")
    title(ws7, "MEASURED convergence ranking (from supplied ONS + LHA + RSH data)", 1, 9)
    ws7.cell(row=2, column=1,
             value="Computed by run_measured_ranking.py. Market = ONS PRMS median by LA "
                   "(Oct 2022-Sep 2023); LHA = DWP/VOA Apr-2024 base (monthly); social = RSH "
                   "2024/25 LOCAL per-bed general-needs rent (92/97 areas; 5 national fallback). "
                   "Rents matched to the LHA base window = structural convergence, not today's "
                   "live gap. geo: exact = name match, curated = our LA->BRMA map. 97 areas; top 30 shown.").font = NOTE_FONT
    ws7.merge_cells("A2:I2")
    ws7.row_dimensions[2].height = 56
    with open(CSVP, newline="") as fh:
        rd = list(csv.DictReader(fh))
    cols = [("rank", "Rank", 6), ("area", "Area (LA)", 30), ("brma", "BRMA", 20),
            ("geo", "Geo", 9), ("soc_src", "Soc src", 8), ("sample_min", "Sample", 8),
            ("mkt_2", "Mkt 2b", 8), ("lha_2", "LHA 2b", 8), ("soc_2", "Soc 2b", 8),
            ("alignment", "Align", 8), ("social_attach", "SocAtt", 8),
            ("compression", "Compr", 8), ("score", "Score", 8)]
    headers = [c[1] for c in cols]
    rows = [[(_num(r[c[0]])) for c in cols] for r in rd[:30]]
    nr7 = write_table(ws7, 4, headers, rows,
                      widths=[c[2] for c in cols], wrap_cols=(2, 3), highlight_top=5)
    for rr in range(5, 5 + len(rows)):          # centre numeric columns
        for cc in list(range(4, len(cols) + 1)):
            ws7.cell(row=rr, column=cc).alignment = CENTER
    ws7.freeze_panes = "A5"
    ws7.cell(row=nr7, column=1,
             value="Full 97-area table: analysis/measured_convergence_ranking.csv. "
                   "See MEASURED-RESULTS.md for interpretation, the social-rent caveat, and how "
                   "this revises the pattern-based ranking (e.g. East Lancs promoted, Black Country "
                   "lowered on pure convergence).").font = NOTE_FONT
    ws7.merge_cells(start_row=nr7, start_column=1, end_row=nr7, end_column=13)
    ws7.row_dimensions[nr7].height = 42

wb.save(OUT)
print("wrote", OUT)
