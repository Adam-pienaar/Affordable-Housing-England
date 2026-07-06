#!/usr/bin/env python3
"""Generate clean, neutral charts for the investor briefing from the measured
ranking CSV. Outputs PNGs into analysis/figures/."""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "measured_convergence_ranking.csv")
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)

# --- clean neutral styling ---
NAVY = "#1F3B57"       # North/Midlands
STEEL = "#2C6E9E"
SOUTH = "#B98A56"      # muted ochre for South
GREY = "#9AA5AD"
INK = "#2B2B2B"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "text.color": INK,
    "axes.edgecolor": "#C9CED2", "axes.labelcolor": INK, "axes.titlecolor": NAVY,
    "xtick.color": INK, "ytick.color": INK, "axes.linewidth": 0.8,
    "figure.dpi": 150, "savefig.dpi": 150, "savefig.bbox": "tight",
})

NORTH_MID = {"North East", "North West", "Yorkshire and the Humber",
             "East Midlands", "West Midlands"}
# fill regions for the 5 national-fallback rows (codes didn't join)
REGION_FIX = {"Barrow-in-Furness": "North West", "Scarborough": "Yorkshire and the Humber",
              "Northampton": "East Midlands", "Harrogate": "Yorkshire and the Humber",
              "Mendip": "South West"}

df = pd.read_csv(CSV)
df["region"] = df["region"].fillna("")
for a, r in REGION_FIX.items():
    df.loc[df.area == a, "region"] = r
df["grp"] = df["region"].apply(lambda r: "North & Midlands" if r in NORTH_MID else "South")


def tidy(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def clean_name(s):
    return (s.replace(" UA", "").replace(", City of", "")
             .replace("North East Lincolnshire", "NE Lincs (Grimsby)")
             .replace("North Lincolnshire", "N Lincs (Scunthorpe)")
             .replace("Kingston upon Hull", "Kingston upon Hull"))


# ---- Fig 1: Top 18 areas by score (horizontal bars) --------------------------
top = df.head(18).iloc[::-1]
colors = [STEEL if g == "North & Midlands" else SOUTH for g in top["grp"]]
fig, ax = plt.subplots(figsize=(7.2, 5.4))
ax.barh(range(len(top)), top["score"], color=colors, edgecolor="white", height=0.72)
ax.set_yticks(range(len(top)))
ax.set_yticklabels([clean_name(a) for a in top["area"]], fontsize=8.5)
ax.set_xlim(0.78, 0.96)
ax.set_xlabel("Convergence score (1.0 = perfect alignment of all four rent layers)")
ax.set_title("Top 18 areas by rent-convergence score", fontweight="bold", loc="left", pad=10)
for i, v in enumerate(top["score"]):
    ax.text(v + 0.002, i, f"{v:.3f}", va="center", fontsize=7.5, color=INK)
tidy(ax)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=STEEL, label="North & Midlands"),
                   Patch(color=SOUTH, label="South")],
          loc="lower right", frameon=False, fontsize=8.5)
fig.savefig(os.path.join(FIG, "fig1_top_areas.png"))
plt.close(fig)

# ---- Fig 2: Mechanism scatter (alignment vs social attachment) ---------------
fig, ax = plt.subplots(figsize=(7.2, 5.2))
for grp, col in [("North & Midlands", STEEL), ("South", SOUTH)]:
    sub = df[df.grp == grp]
    ax.scatter(sub["alignment"], sub["social_attach"], s=34, c=col, alpha=0.8,
               edgecolor="white", linewidth=0.5, label=grp)
for name, dx, dy in [("Hartlepool UA", 5, 5), ("Kingston upon Hull, City of UA", 5, -12),
                     ("Bristol, City of UA", -8, 8), ("Cambridge", 5, 6),
                     ("Burnley", 5, 6)]:
    r = df[df.area == name]
    if len(r):
        x, y = r.iloc[0]["alignment"], r.iloc[0]["social_attach"]
        ax.annotate(clean_name(name), (x, y), textcoords="offset points",
                    xytext=(dx, dy), fontsize=8, color=INK)
ax.set_xlabel("LHA-to-market alignment  (high almost everywhere)")
ax.set_ylabel("Social-rent attachment  (social ÷ market)")
ax.set_title("Why the North converges: alignment is universal, social attachment is not",
             fontweight="bold", loc="left", fontsize=11, pad=10)
ax.legend(loc="lower left", frameon=False, fontsize=9)
tidy(ax)
fig.text(0.62, 0.16, "Converged = top-right\n(all four layers close)",
         fontsize=8.5, color=GREY, style="italic")
fig.savefig(os.path.join(FIG, "fig2_mechanism.png"))
plt.close(fig)

# ---- Fig 3: Four rent layers for the Top 5 investment picks (2-bed) -----------
picks = ["Hartlepool UA", "Kingston upon Hull, City of UA", "Doncaster",
         "Sunderland", "Stoke-on-Trent UA"]
labels = ["Teesside\n(Hartlepool)", "Kingston\nupon Hull", "Doncaster",
          "Sunderland", "Stoke-\non-Trent"]
sub = df.set_index("area").loc[picks]
layers = [("Market", sub["mkt_2"], NAVY), ("LHA", sub["lha_2"], STEEL),
          ("Affordable (80%)", sub["affordable_2"], "#8FB8D6"),
          ("Social", sub["soc_2"], SOUTH)]
import numpy as np
x = np.arange(len(picks)); w = 0.2
fig, ax = plt.subplots(figsize=(7.6, 4.6))
for i, (lab, vals, col) in enumerate(layers):
    ax.bar(x + (i - 1.5) * w, vals.values, w, label=lab, color=col, edgecolor="white")
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8.5)
ax.set_ylabel("Monthly rent, 2-bed (£)")
ax.set_title("The four rent layers sit close together — Top 5 picks (2-bed)",
             fontweight="bold", loc="left", pad=10)
ax.legend(loc="upper right", frameon=False, fontsize=8.5, ncol=2)
tidy(ax)
fig.savefig(os.path.join(FIG, "fig3_four_layers.png"))
plt.close(fig)

# ---- Fig 4: Regional average convergence (map substitute) --------------------
reg = (df.groupby("region")["score"].mean().drop(labels=[""], errors="ignore")
         .sort_values())
colors = [STEEL if r in NORTH_MID else SOUTH for r in reg.index]
fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.barh(range(len(reg)), reg.values, color=colors, edgecolor="white", height=0.7)
ax.set_yticks(range(len(reg))); ax.set_yticklabels(reg.index, fontsize=9)
ax.set_xlim(0.70, 0.90)
ax.set_xlabel("Average convergence score (scored areas)")
ax.set_title("Convergence by region — North & Midlands lead, South trails",
             fontweight="bold", loc="left", pad=10)
for i, v in enumerate(reg.values):
    ax.text(v + 0.002, i, f"{v:.3f}", va="center", fontsize=8, color=INK)
tidy(ax)
fig.text(0.5, -0.03, "Regional average of scored local authorities. A true LA-boundary "
         "map needs GIS data (egress-blocked here).", ha="center", fontsize=7.5, color=GREY)
fig.savefig(os.path.join(FIG, "fig4_regional.png"))
plt.close(fig)

print("wrote 4 figures to", FIG)
