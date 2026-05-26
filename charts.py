"""
charts.py — Vibrant, glossy chart functions with shimmer gradients.
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import matplotlib.colors as mcolors
import seaborn as sns
import numpy as np
import pandas as pd
# plotly removed to save ~100MB RAM on free tier

# ── Glossy Vibrant Palette ──
C1 = "#FF4D8D"   # hot pink
C2 = "#FF85A2"   # rose
C3 = "#36D1DC"   # cyan shimmer
C4 = "#5B86E5"   # electric blue
C5 = "#F7971E"   # golden amber
C6 = "#A855F7"   # vivid purple
C7 = "#34D399"   # emerald
C8 = "#FB7185"   # coral
C9 = "#FBBF24"   # gold
C10 = "#6EE7B7"  # mint

COLORS = [C1, C3, C6, C5, C7, C4, C8, C9, C10, C2]
BG = "#FEFAFF"
TEXT = "#2D2040"
GRID = "#F0E4F4"

# Gradient helper for bar fills
def _gradient_bars(ax, bars, color_start, color_end):
    """Apply a subtle gradient to bar patches via alpha trick."""
    pass  # matplotlib doesn't do per-bar gradients easily; we use rich solid colors instead

def _s(fig, ax, title):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_title(title, fontsize=14, fontweight="bold", color=TEXT, pad=14,
                 fontfamily="serif", fontstyle="italic")
    ax.tick_params(colors=TEXT, labelsize=9)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(True, alpha=0.25, color=GRID, linestyle="--")
    return fig


# ── 1. PIE ──
def plot_pie_chart(df):
    top = df["beer_style"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor(BG)
    explode = [0.04] * len(top)
    wedges, texts, auto = ax.pie(
        top.values, labels=top.index, autopct="%1.1f%%", explode=explode,
        colors=COLORS, startangle=140, pctdistance=0.80,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2.5),
        textprops=dict(fontsize=8, color=TEXT), shadow=False,
    )
    for t in auto:
        t.set_fontsize(7); t.set_color(TEXT); t.set_fontweight("bold")
    ax.set_title("Top 10 Beer Styles", fontsize=15, fontweight="bold",
                 color=C1, fontfamily="serif", fontstyle="italic")
    plt.tight_layout()
    return fig


# ── 2. HISTOGRAM ──
def plot_histogram(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    n, bins, patches = ax.hist(df["review_overall"].dropna(), bins=20,
                                edgecolor="white", linewidth=1.2, alpha=0.9)
    # Gradient coloring across bins
    cm = plt.cm.get_cmap("PuRd")
    for i, p in enumerate(patches):
        p.set_facecolor(cm(0.3 + 0.6 * i / len(patches)))
    ax.set_xlabel("Overall Rating", fontsize=11, color=TEXT)
    ax.set_ylabel("Number of Reviews", fontsize=11, color=TEXT)
    _s(fig, ax, "Distribution of Overall Ratings")
    plt.tight_layout()
    return fig


# ── 3. LINE ──
def plot_line_chart(df):
    yearly = df.groupby("review_year").size().reset_index(name="count")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.fill_between(yearly["review_year"], yearly["count"], alpha=0.12, color=C3)
    ax.plot(yearly["review_year"], yearly["count"], color=C3, linewidth=3,
            marker="o", markersize=7, markerfacecolor=C1,
            markeredgecolor="white", markeredgewidth=2, zorder=5)
    # Glow effect
    ax.plot(yearly["review_year"], yearly["count"], color=C3, linewidth=8, alpha=0.15)
    ax.set_xlabel("Year", fontsize=11, color=TEXT)
    ax.set_ylabel("Number of Reviews", fontsize=11, color=TEXT)
    _s(fig, ax, "Review Trends Over the Years")
    plt.tight_layout()
    return fig


# ── 4. BAR ──
def plot_bar_chart(df):
    brew = df.groupby("brewery_name").agg(
        avg=("review_overall", "mean"), cnt=("review_overall", "count"),
    ).reset_index()
    brew = brew[brew["cnt"] >= 30].nlargest(15, "avg")
    fig, ax = plt.subplots(figsize=(8, 7))
    colors = [COLORS[i % len(COLORS)] for i in range(len(brew))]
    bars = ax.barh(brew["brewery_name"], brew["avg"], color=colors,
                   edgecolor="white", linewidth=1.2, height=0.7)
    # Value labels
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.02, bar.get_y() + bar.get_height()/2,
                f"{w:.2f}", va="center", fontsize=8, color=TEXT, fontweight="bold")
    ax.set_xlabel("Average Overall Rating", fontsize=11, color=TEXT)
    ax.invert_yaxis()
    ax.set_xlim(right=brew["avg"].max() + 0.2)
    _s(fig, ax, "Top 15 Breweries by Rating")
    plt.tight_layout()
    return fig


# ── 5. SCATTER ──
def plot_scatter(df):
    s = df.sample(n=min(800, len(df)), random_state=42)
    fig, ax = plt.subplots(figsize=(8, 5))
    sc = ax.scatter(s["beer_abv"], s["review_overall"], c=s["review_taste"],
                    cmap="cool", alpha=0.55, s=18, edgecolors="white", linewidths=0.3)
    cbar = plt.colorbar(sc, ax=ax, pad=0.02)
    cbar.set_label("Taste Rating", color=TEXT, fontsize=10)
    ax.set_xlabel("ABV (%)", fontsize=11, color=TEXT)
    ax.set_ylabel("Overall Rating", fontsize=11, color=TEXT)
    ax.set_xlim(0, 30)
    _s(fig, ax, "ABV vs Overall Rating (colored by Taste)")
    plt.tight_layout()
    return fig


# ── 6. BOX ──
def plot_box(df):
    top = df["beer_style"].value_counts().head(8).index.tolist()
    sub = df[df["beer_style"].isin(top)]
    fig, ax = plt.subplots(figsize=(10, 5))
    pal = {s: COLORS[i % len(COLORS)] for i, s in enumerate(top)}
    bp = sns.boxplot(data=sub, x="beer_style", y="review_overall",
                hue="beer_style", palette=pal, ax=ax, linewidth=1.2, legend=False,
                flierprops=dict(marker="o", markersize=2, alpha=0.3),
                boxprops=dict(alpha=0.85))
    ax.set_xlabel("")
    ax.set_ylabel("Overall Rating", fontsize=11, color=TEXT)
    ax.set_xticks(range(len(top)))
    ax.set_xticklabels(top, rotation=30, ha="right", fontsize=8)
    _s(fig, ax, "Rating Spread by Beer Style")
    plt.tight_layout()
    return fig


# ── 7. HEATMAP ──
def plot_heatmap(df):
    cols = ["review_overall", "review_aroma", "review_appearance", "review_palate", "review_taste", "beer_abv"]
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(7, 6))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="PuRd", mask=mask,
                linewidths=2.5, linecolor="white", ax=ax,
                annot_kws={"size": 11, "color": TEXT, "fontweight": "bold"},
                cbar_kws={"shrink": 0.8})
    labels = ["Overall", "Aroma", "Appearance", "Palate", "Taste", "ABV"]
    ax.set_xticklabels(labels, fontsize=9, color=TEXT)
    ax.set_yticklabels(labels, fontsize=9, color=TEXT, rotation=0)
    _s(fig, ax, "Correlation Between Ratings")
    ax.grid(False)
    plt.tight_layout()
    return fig


# ── 8. AREA ──
def plot_area_chart(df):
    top5 = df["beer_style"].value_counts().head(5).index
    sub = df[df["beer_style"].isin(top5)]
    pivot = sub.groupby(["review_year", "beer_style"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(8, 5))
    pivot.plot.area(ax=ax, color=COLORS[:5], alpha=0.75, linewidth=1.5)
    ax.set_xlabel("Year", fontsize=11, color=TEXT)
    ax.set_ylabel("Number of Reviews", fontsize=11, color=TEXT)
    ax.legend(fontsize=7, loc="upper left", framealpha=0.9)
    _s(fig, ax, "Top 5 Styles Over Time")
    plt.tight_layout()
    return fig


# ── 9. COUNT ──
def plot_count(df):
    top15 = df["beer_style"].value_counts().head(15)
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = [COLORS[i % len(COLORS)] for i in range(len(top15))]
    bars = ax.barh(top15.index, top15.values, color=colors,
                   edgecolor="white", linewidth=1.2, height=0.7)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 50, bar.get_y() + bar.get_height()/2,
                f"{w:,.0f}", va="center", fontsize=7, color=TEXT, fontweight="bold")
    ax.invert_yaxis()
    ax.set_xlabel("Number of Reviews", fontsize=11, color=TEXT)
    _s(fig, ax, "Most Reviewed Beer Styles")
    plt.tight_layout()
    return fig


# ── 10. VIOLIN ──
def plot_violin(df):
    top = df["beer_style"].value_counts().head(8).index.tolist()
    sub = df[df["beer_style"].isin(top)]
    fig, ax = plt.subplots(figsize=(10, 5))
    pal = {s: COLORS[i % len(COLORS)] for i, s in enumerate(top)}
    sns.violinplot(data=sub, x="beer_style", y="review_taste",
                   hue="beer_style", palette=pal, ax=ax, inner="box",
                   linewidth=0.8, legend=False, alpha=0.8)
    ax.set_xlabel("")
    ax.set_ylabel("Taste Rating", fontsize=11, color=TEXT)
    ax.set_xticks(range(len(top)))
    ax.set_xticklabels(top, rotation=30, ha="right", fontsize=8)
    _s(fig, ax, "Taste Distribution by Style")
    plt.tight_layout()
    return fig


# ── BONUS 1: PAIR PLOT ──
def plot_pair(df):
    s = df.sample(n=min(300, len(df)), random_state=42)
    cols = ["review_overall", "review_aroma", "review_taste"]
    g = sns.pairplot(
        s[cols], diag_kind="kde",
        plot_kws=dict(alpha=0.3, s=8, color=C6, edgecolor="white", linewidth=0.1),
        diag_kws=dict(color=C1, alpha=0.7),
    )
    g.figure.patch.set_facecolor(BG)
    g.figure.suptitle("Rating Dimensions — Pair Plot", y=1.01,
                      fontsize=14, fontweight="bold", color=TEXT, fontfamily="serif")
    return g.figure


# ── BONUS 2: BUBBLE (Plotly) ──
def plot_bubble(df):
    brew = df.groupby("brewery_name").agg(
        avg=("review_overall", "mean"), cnt=("review_overall", "count"),
        beers=("beer_beerid", "nunique"),
    ).reset_index()
    brew = brew[brew["cnt"] >= 30].nlargest(40, "cnt")
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    sizes = (brew["beers"] / brew["beers"].max() * 400).clip(lower=20)
    scatter = ax.scatter(
        brew["avg"], brew["cnt"], s=sizes, c=brew["avg"],
        cmap=mcolors.LinearSegmentedColormap.from_list("", ["#36D1DC", "#FF4D8D", "#A855F7"]),
        alpha=0.75, edgecolors="white", linewidth=0.8,
    )
    ax.set_xlabel("Average Rating", color=TEXT, fontfamily="serif")
    ax.set_ylabel("Total Reviews", color=TEXT, fontfamily="serif")
    ax.set_title("Breweries — Rating vs Popularity", fontsize=14, fontweight="bold",
                 color=TEXT, fontfamily="serif")
    ax.tick_params(colors=GRID)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(True, alpha=0.15, color=GRID)
    cb = fig.colorbar(scatter, ax=ax, pad=0.02)
    cb.set_label("Avg Rating", color=TEXT)
    cb.ax.tick_params(colors=GRID)
    fig.tight_layout()
    return fig


# ── BONUS 3: STACKED BAR ──
def plot_stacked_bar(df):
    top10 = df["beer_style"].value_counts().head(10).index
    sub = df[df["beer_style"].isin(top10)]
    rcols = ["review_aroma", "review_appearance", "review_palate", "review_taste"]
    means = sub.groupby("beer_style")[rcols].mean().loc[top10]
    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = np.zeros(len(means))
    labels = ["Aroma", "Appearance", "Palate", "Taste"]
    bar_colors = [C1, C3, C6, C5]
    for i, col in enumerate(rcols):
        ax.bar(range(len(means)), means[col], bottom=bottom,
               color=bar_colors[i], label=labels[i], edgecolor="white",
               linewidth=1, alpha=0.88)
        bottom += means[col].values
    ax.set_xticks(range(len(means)))
    ax.set_xticklabels(means.index, rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("Cumulative Avg Rating", fontsize=11, color=TEXT)
    ax.legend(fontsize=9, loc="upper right")
    _s(fig, ax, "Rating Breakdown by Style")
    plt.tight_layout()
    return fig


# ── BONUS 4: DONUT ──
def plot_donut(df):
    bins = [0, 4, 6, 8, 12, 60]
    labels = ["Light (0-4%)", "Medium (4-6%)", "Strong (6-8%)", "V.Strong (8-12%)", "Extreme (12%+)"]
    tmp = df.copy()
    tmp["abv_cat"] = pd.cut(tmp["beer_abv"], bins=bins, labels=labels, right=False)
    counts = tmp["abv_cat"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor(BG)
    explode = [0.03] * len(counts)
    wedges, texts, auto = ax.pie(
        counts.values, labels=counts.index, autopct="%1.1f%%", explode=explode,
        colors=[C1, C3, C6, C5, C8], startangle=90, pctdistance=0.78,
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2.5),
        textprops=dict(fontsize=9, color=TEXT),
    )
    for t in auto:
        t.set_fontsize(8); t.set_fontweight("bold"); t.set_color(TEXT)
    ax.set_title("ABV Category Distribution", fontsize=15, fontweight="bold",
                 color=C6, fontfamily="serif", fontstyle="italic")
    plt.tight_layout()
    return fig
