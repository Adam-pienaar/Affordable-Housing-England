#!/usr/bin/env python3
"""Build the investor briefing as a polished PDF (reportlab) from the measured
data + figures. Mirrors the Word briefing. Run: python analysis/build_pdf.py"""
import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, ListFlowable, ListItem)
from reportlab.lib.enums import TA_CENTER

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
CSV = os.path.join(HERE, "measured_convergence_ranking.csv")
OUT = os.path.join(HERE, "UK-Rent-Convergence-Briefing.pdf")

NAVY = colors.HexColor("#1F3B57")
STEEL = colors.HexColor("#2C6E9E")
GREY = colors.HexColor("#606060")
ZEBRA = colors.HexColor("#EEF3F7")
WHITE = colors.white

df = pd.read_csv(CSV)
REGION_ABBR = {"Yorkshire and the Humber": "Yorks & Humber"}
REGION_FIX = {"Barrow-in-Furness": "North West", "Scarborough": "Yorks & Humber",
              "Northampton": "East Midlands", "Harrogate": "Yorks & Humber",
              "Mendip": "South West"}


def clean(s):
    return (s.replace(" UA", "").replace(", City of", "")
             .replace("North East Lincolnshire", "NE Lincs (Grimsby)")
             .replace("North Lincolnshire", "N Lincs (Scunthorpe)"))


ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], textColor=NAVY, fontSize=16,
                    spaceBefore=6, spaceAfter=6, borderPad=0)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=STEEL, fontSize=12,
                    spaceBefore=8, spaceAfter=3)
BODY = ParagraphStyle("Body", parent=ss["BodyText"], fontSize=10.5, leading=14)
BULLET = ParagraphStyle("Bul", parent=BODY, fontSize=10.5, leading=13.5)
CAP = ParagraphStyle("Cap", parent=BODY, fontSize=8.5, textColor=GREY, leading=11)
CTR = ParagraphStyle("Ctr", parent=BODY, alignment=TA_CENTER)

USABLE = A4[0] - 34 * mm  # margins 17mm each side


def bullets(items):
    li = []
    for it in items:
        if isinstance(it, tuple):
            txt = f"<b>{it[0]}</b> {it[1]}"
        else:
            txt = it
        li.append(ListItem(Paragraph(txt, BULLET), leftIndent=10, value="•"))
    return ListFlowable(li, bulletType="bullet", start="•", leftIndent=12,
                        bulletColor=STEEL, spaceAfter=6)


def image(name, width=USABLE):
    path = os.path.join(FIG, name)
    iw, ih = ImageReader(path).getSize()
    return Image(path, width=width, height=width * ih / iw)


def make_table(headers, rows, widths, fs=8.5):
    data = [headers] + rows
    t = Table(data, colWidths=[w * mm for w in widths], hAlign="CENTER")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), fs),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9CED2")),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ZEBRA))
    t.setStyle(TableStyle(style))
    return t


story = []

# ---- COVER ----
story += [Spacer(1, 60 * mm)]
story.append(Paragraph('<font color="#1F3B57"><b>Rent Convergence in England</b></font>',
                       ParagraphStyle("T", parent=CTR, fontSize=28, leading=32)))
story.append(Spacer(1, 6 * mm))
story.append(Paragraph('<font color="#2C6E9E">A 1–3 Bed Affordable-Housing Investment Screen</font>',
                       ParagraphStyle("S", parent=CTR, fontSize=15)))
story.append(Spacer(1, 3 * mm))
story.append(Paragraph('<i><font color="#606060">Where market rent, LHA, Affordable Rent and social rent line up</font></i>',
                       ParagraphStyle("S2", parent=CTR, fontSize=12)))
story.append(Spacer(1, 40 * mm))
for txt, sz, col in [("Measured from official open data — 97 local authorities scored", 11, NAVY),
                     ("ONS Private Rental Market Statistics · DWP/VOA LHA · Regulator of Social Housing", 9.5, GREY),
                     ("July 2026", 10, GREY)]:
    story.append(Paragraph(txt, ParagraphStyle("cv", parent=CTR, fontSize=sz, textColor=col)))
    story.append(Spacer(1, 3 * mm))
story.append(PageBreak())

# ---- EXEC SUMMARY ----
story.append(Paragraph("Executive summary", H1))
story.append(Paragraph("What this is", H2))
story.append(bullets([
    "A screen for English areas where all four rent levels for 1–3 bed homes sit close together — lower rent risk, stronger housing-benefit alignment.",
    "Four layers compared: market rent, LHA (benefit cap), Affordable Rent (80% of market), and social rent.",
    "97 local authorities scored from official open data; studios and shared housing excluded.",
]))
story.append(Paragraph("Headline finding", H2))
story.append(bullets([
    ("Geography:", "convergence is concentrated in the low-cost North &amp; Midlands; the least-converged areas are all high-rent South."),
    "Every one of the top 25 areas is northern or Midlands; the bottom five are Cambridge, Brighton, Bristol, Exeter, Oxford.",
    ("Why:", "the driver is social-rent attachment — near-uniform social rent only sits close to market rent where market rent is low."),
]))
story.append(Paragraph("Top 5 investment picks (convergence + demand)", H2))
story.append(bullets(["Teesside (Hartlepool / Redcar / Middlesbrough) · Kingston upon Hull · Doncaster · Sunderland · Stoke-on-Trent."]))
story.append(Spacer(1, 3 * mm))
story.append(image("fig1_top_areas.png", USABLE * 0.92))
story.append(PageBreak())

# ---- THE IDEA ----
story.append(Paragraph("The convergence idea", H1))
story.append(bullets([
    ("Aligned when:", "LHA is close to market rent — benefit-backed demand is well supported."),
    "Affordable Rent (80% of market) sits near or below LHA — coverable by a benefit tenant.",
    "Social rent not wildly detached from market rent.",
    "1/2/3-bed rents relatively compressed (low variation).",
]))
story.append(Paragraph('<i>Score = 0.40 × LHA-alignment + 0.30 × social-attachment + 0.30 × rent-compression '
                       '(0–1; higher = tighter).</i>', CAP))
story.append(Paragraph("The mechanism the data exposes", H2))
story.append(bullets([
    "LHA-to-market alignment is high almost everywhere — LHA is the 30th percentile by design (even Cambridge, Guildford score well).",
    "Social rent barely varies nationally (~£380–£490/mo here) but market rent ranges ~£475–£1,400.",
    ("Result:", "four-layer convergence needs a low-rent market — the northern signature."),
]))
story.append(Spacer(1, 2 * mm))
story.append(image("fig2_mechanism.png", USABLE * 0.92))
story.append(PageBreak())

# ---- TOP 20 ----
story.append(Paragraph("Measured results — Top 20 areas", H1))
headers = ["#", "Area", "Region", "Mkt 2-bed", "LHA 2-bed", "Social 2-bed", "Score"]
rows = []
for _, r in df.head(20).iterrows():
    rraw = r["region"] if pd.notna(r["region"]) else ""
    region = REGION_ABBR.get(rraw, rraw) if rraw else REGION_FIX.get(r["area"], "—")
    rows.append([str(int(r["rank"])), clean(r["area"]), region,
                 f"£{int(r['mkt_2'])}", f"£{int(r['lha_2'])}", f"£{int(r['soc_2'])}", f"{r['score']:.3f}"])
story.append(make_table(headers, rows, widths=[8, 42, 32, 20, 20, 22, 16]))
story.append(Spacer(1, 2 * mm))
story.append(Paragraph("Rents matched to the LHA reference window (Oct 2022–Sep 2023); measures structural "
                       "convergence, not today's live gap. Full 97-area table in the accompanying spreadsheet.", CAP))
story.append(Spacer(1, 4 * mm))
story.append(Paragraph("Regional pattern", H2))
story.append(image("fig4_regional.png", USABLE * 0.82))
story.append(PageBreak())

# ---- TOP 5 ----
story.append(Paragraph("Top 5 investment picks", H1))
story.append(image("fig3_four_layers.png", USABLE * 0.86))
story.append(Spacer(1, 3 * mm))
picks = [
    ("1 · Teesside — Hartlepool / Redcar / Middlesbrough",
     "elite convergence (#2/#3/#5) with the clearest new-demand story: Teesworks / Freeport and energy investment.",
     "keep to the regeneration footprint; avoid deprived peripheral estates."),
    ("2 · Kingston upon Hull  (#12)",
     "top-tier convergence, a large deep market, and a real demand engine — Humber energy cluster, port, university.",
     "flood-zone and older-stock pockets; social rents unusually low."),
    ("3 · Doncaster  (#22)",
     "strong convergence with a genuine logistics / rail base and Sheffield city-region pull.",
     "post-industrial low-demand micro-markets."),
    ("4 · Sunderland  (#19)",
     "strong convergence plus Riverside regeneration and automotive employment.",
     "peripheral estates weaker; single-employer exposure."),
    ("5 · Stoke-on-Trent  (#20)",
     "strong convergence with regeneration and affordability-led in-migration.",
     "pockets of low-demand terraced stock; buy in sound sub-markets."),
]
for title, why, risk in picks:
    story.append(Paragraph(title, H2))
    story.append(bullets([("Why:", why), ("Watch:", risk)]))
story.append(Paragraph("<i>Highest pure convergence but thinner demand: Burnley / Hyndburn / Pendle / Blackburn "
                       "(East Lancs), Grimsby, Scunthorpe, Rotherham. Blackpool scores well but stays a watch "
                       "(weak demand, poor stock).</i>", CAP))
story.append(PageBreak())

# ---- OPERATORS ----
story.append(Paragraph("Operators active in the stream", H1))
story.append(Paragraph("Registered providers (RP) and council ALMOs already delivering social &amp; affordable rent "
                       "in each pick. RSH grades: G=governance, V=viability, C=consumer (1 = strongest). "
                       "* = widely-reported figure.", CAP))
story.append(Spacer(1, 2 * mm))
op_headers = ["Area", "Organisation", "Type", "Homes", "RSH (G/V/C)"]
op_rows = [
    ["Teesside", "Thirteen Group", "RP", "~34,000", "G1 / V1 / C1"],
    ["Teesside", "Beyond Housing", "RP", "~15,350", "G1 / V1 / —"],
    ["Teesside", "North Star Housing", "RP", "~4,000", "G1 / V1 / —"],
    ["Hull", "Riverside", "RP", "~75,000*", "G1 / V2 / —"],
    ["Hull", "Sanctuary", "RP", "~120,000*", "G1 / V2 / C2"],
    ["Hull", "Pickering & Ferens Homes", "RP", "~1,400", "n/v"],
    ["Doncaster", "St Leger Homes of Doncaster", "ALMO", "~20,000", "— (council-held)"],
    ["Doncaster", "Together Housing", "RP", "~36,000", "G1 / V2 / —"],
    ["Doncaster", "Housing 21", "RP", "~23,300", "G1 / V1 / C1"],
    ["Sunderland", "Gentoo Group", "RP", "~29,000", "G1 / V2 / C1"],
    ["Stoke-on-Trent", "Aspire Housing", "RP", "~9,300", "G1 / V2 / C1"],
    ["Stoke-on-Trent", "Honeycomb Group (Staffs Housing)", "RP", "~3,118", "n/v"],
    ["Stoke-on-Trent", "EPIC Housing", "RP", "~1,400", "n/v"],
]
story.append(make_table(op_headers, op_rows, widths=[24, 55, 14, 22, 30], fs=9))
story.append(Spacer(1, 2 * mm))
story.append(Paragraph("Maps who is active — not an endorsement or a claim of current tenders. Verify current "
                       "pipeline / JV appetite and re-check RSH judgements before acting.", CAP))
story.append(PageBreak())

# ---- METHOD & CAVEATS ----
story.append(Paragraph("Method, data &amp; caveats", H1))
story.append(Paragraph("Data sources (official, open)", H2))
story.append(bullets([
    "Market rent — ONS/VOA Private Rental Market Statistics: median monthly rent by bedroom, by local authority (Oct 2022–Sep 2023).",
    "LHA — DWP/VOA April-2024 rates (frozen), 1/2/3-bed, by BRMA.",
    "Social rent — Regulator of Social Housing 2024/25: per-LA, per-bedsize general-needs rent.",
    "Affordable Rent — derived as 80% of market (statutory definition).",
]))
story.append(Paragraph("How it was built", H2))
story.append(bullets([
    "Three layers joined per area; convergence score computed and ranked.",
    "92 of 97 areas use local social rent; 5 use the England average as fallback.",
    "LA→BRMA geography: 56 exact matches + 37 web-verified + 4 genuinely multi-BRMA (flagged).",
]))
story.append(Paragraph("Caveats", H2))
story.append(bullets([
    "Structural, not live — rents matched to the frozen-LHA window; today's market-vs-LHA gap is wider.",
    "A convergence screen, not a demand / yield / asset-quality model — pair with local demand work.",
    "Small-sample areas flagged in the data; treat cautiously.",
    "97 areas scored (not all ~300) — full national coverage needs the official LA→BRMA lookup.",
]))
story.append(Paragraph("Sources", H2))
story.append(Paragraph("ONS Private Rental Market Statistics · DWP/VOA Local Housing Allowance rates · Regulator of "
                       "Social Housing, Registered provider social housing stock and rents 2024/25 · RSH regulatory "
                       "judgements. All Open Government Licence. Reproducible via run_measured_ranking.py.", CAP))


def footer(canvas, doc_):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GREY)
    if doc_.page > 1:
        canvas.drawRightString(A4[0] - 17 * mm, 10 * mm, f"{doc_.page}")
        canvas.drawString(17 * mm, 10 * mm, "Rent Convergence in England — investment screen")
    canvas.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=17 * mm, bottomMargin=16 * mm,
                        leftMargin=17 * mm, rightMargin=17 * mm,
                        title="Rent Convergence in England")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("wrote", OUT)
