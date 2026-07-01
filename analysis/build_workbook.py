#!/usr/bin/env python3
"""Build the rent-convergence Excel workbook from the analysis content.

Keeps structured/tabular data (rankings, metric definitions, verified anchors,
sources) and omits long-form prose. Run: python analysis/build_workbook.py
"""
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
     "Sourced LHA close to market (1b GBP101.92 / 2b GBP126.92 / 3b GBP150.00 pw); tight 1-3 bed spread",
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
    ["Hull & East Riding LHA - 1 bed", "GBP 101.92 / wk (approx GBP 442/mo)", "2024/25", "VOA/council (6)"],
    ["Hull & East Riding LHA - 2 bed", "GBP 126.92 / wk (approx GBP 550/mo)", "2024/25", "VOA/council (6)"],
    ["Hull & East Riding LHA - 3 bed", "GBP 150.00 / wk (approx GBP 650/mo)", "2024/25", "VOA/council (6)"],
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

h6 = ["Area", "Organisation", "Type", "Relevance to this revenue stream"]
r6 = [
    # Stoke-on-Trent
    ["Stoke-on-Trent", "Aspire Housing", "RP (housing association)",
     "North Staffs/Stoke & Newcastle-under-Lyme RP developing new affordable homes; in merger talks with whg (would create ~32,000-home Midlands group)."],
    ["Stoke-on-Trent", "Honeycomb Group (incl. Staffs Housing)", "RP / charity",
     "Provides affordable housing and specialist support across Staffordshire, Cheshire and Derbyshire; Stoke-based."],
    ["Stoke-on-Trent", "Stoke-on-Trent Housing Society", "RP (charitable HA)",
     "621 homes across the city; actively builds new homes to meet local housing need."],
    ["Stoke-on-Trent", "EPIC Housing", "RP (community HA)",
     "~1,400 homes at affordable rents across Stoke, Newcastle-under-Lyme and Staffordshire Moorlands."],
    # Hull & East Riding
    ["Kingston upon Hull & East Riding", "Riverside", "RP (large national HA)",
     "Dedicated Hull operations delivering social/affordable rent plus care & support."],
    ["Kingston upon Hull & East Riding", "Pickering & Ferens Homes (PFH)", "RP (housing association)",
     "~1,400 homes across Hull & East Riding (predominantly older-persons affordable housing)."],
    ["Kingston upon Hull & East Riding", "Hull Churches Housing Association", "RP (independent HA)",
     "~500 homes for social rent & shared ownership in Hull and adjoining East Riding."],
    ["Kingston upon Hull & East Riding", "Sanctuary", "RP (large national HA)",
     "National RP with a Hull office/presence providing affordable rented homes."],
    # Teesside
    ["Teesside (Middlesbrough/Stockton/Redcar)", "Thirteen Group", "RP (housing association)",
     "Teesside-based; ~34,000 homes mostly in Teesside - the largest local social landlord and an active developer."],
    ["Teesside (Middlesbrough/Stockton/Redcar)", "Beyond Housing", "RP (housing association)",
     "Major RP across Redcar & Cleveland / Tees Valley; core partner in Tees Valley Homefinder."],
    ["Teesside (Middlesbrough/Stockton/Redcar)", "North Star Housing Group", "RP (housing association)",
     "Stockton-based RP; core partner in Tees Valley Homefinder and the Tees Valley Housing Partnership."],
    ["Teesside (Middlesbrough/Stockton/Redcar)", "The PRS REIT", "For-profit build-to-rent",
     "For-profit single-family BTR active in Teesside - example of the commercial side of the same rented-housing stream."],
    # Wolverhampton / Black Country
    ["Wolverhampton / Black Country", "whg (Walsall Housing Group)", "RP (large HA)",
     "Large Midlands RP (Walsall HQ) delivering new affordable/social homes (e.g. Royal Hospital site: 154 homes for affordable rent & shared ownership)."],
    ["Wolverhampton / Black Country", "Bromford", "RP (large HA / developer)",
     "Wolverhampton-HQ RP; major West Midlands developer via the 'Homes for the West Midlands' partnership (100% affordable Black Country scheme)."],
    ["Wolverhampton / Black Country", "Black Country Housing Group (BCHG)", "RP (housing association)",
     "Black Country RP providing affordable rented homes and support."],
    ["Wolverhampton / Black Country", "Wolverhampton Homes", "Council ALMO",
     "Arm's-length organisation managing the City of Wolverhampton Council's social rented stock."],
    # Doncaster
    ["Doncaster", "St Leger Homes of Doncaster", "Council ALMO",
     "Manages ~20,000 homes for City of Doncaster Council - the dominant social landlord; runs the Choice Based Lettings scheme."],
    ["Doncaster", "Together Housing", "RP (large HA)",
     "Delivering new affordable homes in Doncaster (2024 scheme with Housing 21 as part of a diverse development)."],
    ["Doncaster", "Housing 21", "RP (older-persons HA)",
     "Retirement/older-persons RP partnering on affordable-homes delivery in Doncaster."],
]
nr6 = write_table(ws6, 4, h6, r6, widths=[34, 34, 26, 66], wrap_cols=(1, 2, 3, 4))
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
        for c in range(1, 5):
            ws6.cell(row=5 + i, column=c).fill = PatternFill("solid", fgColor="F2F2F2")
ws6.freeze_panes = "A5"
ws6.cell(row=nr6 + 1, column=1,
         value="Note: this maps who is active in the stream, not an endorsement or a claim of "
               "current tenders. RP = Registered Provider; ALMO = Arm's Length Management "
               "Organisation. Verify current pipeline/JV appetite directly before acting.").font = NOTE_FONT
ws6.merge_cells(start_row=nr6 + 1, start_column=1, end_row=nr6 + 1, end_column=4)
ws6.row_dimensions[nr6 + 1].height = 40

wb.save(OUT)
print("wrote", OUT)
