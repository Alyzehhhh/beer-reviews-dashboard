"""
app.py — World Wide Beer Reviews Dashboard
Vibrant glassmorphism design with shimmer accents.
"""

import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from filters import load_data, setup_sidebar_filters, get_kpi_data, get_full_counts
from charts import (
    plot_pie_chart, plot_histogram, plot_line_chart, plot_bar_chart,
    plot_scatter, plot_box, plot_heatmap, plot_area_chart, plot_count,
    plot_violin, plot_pair, plot_bubble, plot_stacked_bar, plot_donut,
)

st.set_page_config(
    page_title="World Wide Beer Reviews",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS — Glassmorphism + Shimmer ─────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Poppins:wght@300;400;500;600&display=swap');

    /* ── Animated gradient background ── */
    .stApp {
        background: linear-gradient(135deg, #FDF2F8 0%, #FAF5FF 25%, #EFF6FF 50%, #FDF2F8 75%, #FCE7F3 100%);
        background-size: 400% 400%;
        animation: bgShift 20s ease infinite;
        font-family: 'Poppins', sans-serif;
    }
    @keyframes bgShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ── Sidebar — frosted glass ── */
    section[data-testid="stSidebar"] {
        background: rgba(255, 240, 250, 0.85) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 77, 141, 0.15);
    }
    section[data-testid="stSidebar"] label {
        color: #4A3060 !important;
        font-weight: 500;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #2D2040 !important;
    }

    /* ── KPI Cards — glassmorphism ── */
    .kpi-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 20px 14px;
        text-align: center;
        border: 1px solid rgba(255, 77, 141, 0.15);
        box-shadow: 0 8px 32px rgba(167, 85, 247, 0.08), inset 0 1px 0 rgba(255,255,255,0.8);
        transition: all 0.4s cubic-bezier(.4,0,.2,1);
        min-height: 120px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.3) 50%, transparent 60%);
        animation: shimmer 4s ease-in-out infinite;
    }
    @keyframes shimmer {
        0%, 100% { transform: translateX(-100%) rotate(45deg); }
        50% { transform: translateX(100%) rotate(45deg); }
    }
    .kpi-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 16px 48px rgba(167, 85, 247, 0.15), inset 0 1px 0 rgba(255,255,255,0.9);
    }
    .kpi-number {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem; font-weight: 900;
        background: linear-gradient(135deg, #FF4D8D, #A855F7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 4px 0 2px 0; line-height: 1.2; white-space: nowrap;
        position: relative; z-index: 1;
    }
    .kpi-label {
        font-family: 'Poppins', sans-serif;
        font-size: 0.7rem; color: #8B7AA0;
        font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px;
        position: relative; z-index: 1;
    }
    .kpi-icon {
        font-size: 1.6rem; margin-bottom: 4px;
        position: relative; z-index: 1;
    }

    /* ── KPI Variants ── */
    div.kpi-number.kpi-cyan {
        background: linear-gradient(135deg, #36D1DC, #5B86E5) !important;
        -webkit-background-clip: text !important; background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    div.kpi-number.kpi-gold {
        background: linear-gradient(135deg, #F7971E, #FFD200) !important;
        -webkit-background-clip: text !important; background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    div.kpi-number.kpi-emerald {
        background: linear-gradient(135deg, #34D399, #059669) !important;
        -webkit-background-clip: text !important; background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    div.kpi-number.kpi-purple {
        background: linear-gradient(135deg, #A855F7, #7C3AED) !important;
        -webkit-background-clip: text !important; background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }

    /* ── Chart Containers — glass cards ── */
    .chart-container {
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 22px;
        margin: 10px 0;
        border: 1px solid rgba(255, 77, 141, 0.1);
        box-shadow: 0 4px 24px rgba(167, 85, 247, 0.06);
        transition: box-shadow 0.3s ease;
    }
    .chart-container:hover {
        box-shadow: 0 8px 40px rgba(167, 85, 247, 0.12);
    }

    /* ── Section Headers — gradient pill ── */
    .section-header {
        background: linear-gradient(135deg, #FF4D8D 0%, #A855F7 50%, #5B86E5 100%);
        color: white !important;
        padding: 14px 28px;
        border-radius: 16px;
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem; font-weight: 700;
        margin: 35px 0 20px 0;
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.3);
        letter-spacing: 0.5px;
    }

    /* ── Title ── */
    .dash-title { text-align: center; padding: 28px 20px 12px 20px; }
    .dash-title h1 {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.8rem !important; font-weight: 900 !important;
        background: linear-gradient(135deg, #FF4D8D, #A855F7, #36D1DC) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 5px !important;
    }
    .dash-title p {
        font-family: 'Poppins', sans-serif; color: #8B7AA0;
        font-size: 1rem; margin-top: 0;
    }

    .pink-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #FF4D8D, #A855F7, #36D1DC, transparent);
        border: none; margin: 12px 0 28px 0; border-radius: 2px;
    }

    .footer {
        text-align: center; padding: 30px; color: #bbb;
        font-size: 0.85rem; font-family: 'Poppins', sans-serif;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in { animation: fadeInUp 0.6s ease-out forwards; }

    .stMarkdown { color: #2D2040; }
    .stButton > button {
        background: linear-gradient(135deg, #FF4D8D, #A855F7) !important;
        color: white !important; border: none !important;
        border-radius: 14px !important; font-weight: 600 !important;
        padding: 8px 22px !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3) !important;
    }
    .stButton > button:hover {
        box-shadow: 0 6px 25px rgba(168, 85, 247, 0.5) !important;
        transform: translateY(-1px);
    }

    .insight-box {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-left: 4px solid;
        border-image: linear-gradient(180deg, #FF4D8D, #A855F7) 1;
        border-radius: 0 14px 14px 0;
        padding: 14px 20px; margin: 14px 0;
        font-size: 0.9rem; color: #4A3060;
    }

    /* ── Data Sheet — glass table ── */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(168, 85, 247, 0.15) !important;
        border-radius: 16px !important;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.06);
    }
    div[data-testid="stDataFrame"] th,
    div[data-testid="stDataFrame"] [role="columnheader"] {
        background: linear-gradient(135deg, #FCE7F3, #FAF5FF) !important;
        color: #7C3AED !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
    }
    div[data-testid="stDataFrame"] td,
    div[data-testid="stDataFrame"] [role="gridcell"] {
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.8rem !important;
        color: #2D2040 !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Load Data ─────────────────────────────────────────────────────
df = load_data()
filtered_df, filters_active = setup_sidebar_filters(df)

# ── Header ────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-title animate-in">
    <h1>🍺 World Wide Beer Reviews</h1>
    <p>Exploring 1.5 million reviews from BeerAdvocate — aroma, appearance, palate, taste & beyond</p>
</div>
<div class="pink-divider"></div>
""", unsafe_allow_html=True)


# ── KPI Cards ─────────────────────────────────────────────────────
kpi = get_kpi_data(filtered_df)
full = get_full_counts()


def fmt(n):
    if n >= 1_000_000: return f"{n/1_000_000:.2f}M"
    elif n >= 1_000: return f"{n/1_000:.1f}K"
    return str(n)


col1, col2, col3 = st.columns(3)

with col1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="kpi-card animate-in">
            <div class="kpi-icon">📝</div>
            <div class="kpi-number">{fmt(full["total_reviews"])}</div>
            <div class="kpi-label">Total Reviews</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card animate-in">
            <div class="kpi-icon">🍺</div>
            <div class="kpi-number kpi-cyan">{fmt(full["total_beers"])}</div>
            <div class="kpi-label">Unique Beers</div>
        </div>""", unsafe_allow_html=True)

with col2:
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"""
        <div class="kpi-card animate-in">
            <div class="kpi-icon">🏭</div>
            <div class="kpi-number kpi-purple">{fmt(full["total_breweries"])}</div>
            <div class="kpi-label">Breweries</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card animate-in">
            <div class="kpi-icon">⭐</div>
            <div class="kpi-number kpi-gold">{kpi['avg_rating']}</div>
            <div class="kpi-label">Avg Rating</div>
        </div>""", unsafe_allow_html=True)

with col3:
    c5, c6 = st.columns(2)
    with c5:
        st.markdown(f"""
        <div class="kpi-card animate-in">
            <div class="kpi-icon">🏆</div>
            <div class="kpi-number kpi-emerald" style="font-size:0.9rem;">{kpi['top_style']}</div>
            <div class="kpi-label">Top Style</div>
        </div>""", unsafe_allow_html=True)
    with c6:
        st.markdown(f"""
        <div class="kpi-card animate-in">
            <div class="kpi-icon">🔥</div>
            <div class="kpi-number kpi-gold">{kpi['avg_abv']}%</div>
            <div class="kpi-label">Avg ABV</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if filters_active:
    st.markdown(
        f'<div class="insight-box">Showing <b>{len(filtered_df):,}</b> of <b>{len(df):,}</b> sampled reviews based on your filters.</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════
# SECTION 1: DISTRIBUTION & COMPOSITION
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📊 Distribution & Composition</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = plot_pie_chart(filtered_df)
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = plot_donut(filtered_df)
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
    IPAs and Pale Ales dominate the beer world. Most craft beers land in the 5–8% ABV sweet spot.
</div>
""", unsafe_allow_html=True)

col_c, col_d = st.columns(2)
with col_c:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = plot_histogram(filtered_df)
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col_d:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = plot_count(filtered_df)
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 2: TRENDS OVER TIME
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📈 Trends Over Time</div>', unsafe_allow_html=True)

col_e, col_f = st.columns(2)
with col_e:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = plot_line_chart(filtered_df)
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col_f:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = plot_area_chart(filtered_df)
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
    Beer reviewing took off around 2004 and peaked in 2008–2011. The craft beer boom is clearly visible, especially for IPAs.
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 3: RATINGS & COMPARISONS
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">⭐ Ratings & Comparisons</div>', unsafe_allow_html=True)

col_g, col_h = st.columns(2)
with col_g:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = plot_bar_chart(filtered_df)
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col_h:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = plot_stacked_bar(filtered_df)
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 4: RELATIONSHIPS & DEEP DIVE
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">🔬 Relationships & Deep Dive</div>', unsafe_allow_html=True)

col_i, col_j = st.columns(2)
with col_i:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = plot_scatter(filtered_df)
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col_j:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = plot_heatmap(filtered_df)
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
    Taste has the strongest link to overall rating (0.90 correlation). ABV barely affects how people rate a beer.
</div>
""", unsafe_allow_html=True)

col_k, col_l = st.columns(2)
with col_k:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = plot_box(filtered_df)
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col_l:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = plot_violin(filtered_df)
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# Bubble chart (Plotly)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig = plot_bubble(filtered_df)
st.plotly_chart(fig, width="stretch")
st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 5: MULTI-DIMENSION ANALYSIS
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">🎯 Multi-Dimension Analysis</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
    This pair plot reveals how all five rating dimensions relate. Notice the tight clusters — most reviewers rate all dimensions similarly.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig = plot_pair(filtered_df)
st.pyplot(fig, width="stretch")
plt.close(fig)
st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 6: DATA SHEET (compact)
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📋 Data Sheet</div>', unsafe_allow_html=True)

_col_map = {
    "beer_name": "Beer",
    "brewery_name": "Brewery",
    "beer_style": "Style",
    "beer_abv": "ABV %",
    "review_overall": "Overall",
    "review_taste": "Taste",
    "review_aroma": "Aroma",
}
avail = [c for c in _col_map if c in filtered_df.columns]
data_display = filtered_df[avail].rename(columns={c: _col_map[c] for c in avail}).head(500).reset_index(drop=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown(
    f'<p style="font-family:Poppins,sans-serif;font-size:0.82rem;margin-bottom:6px;">'
    f'<span style="background:linear-gradient(135deg,#FF4D8D,#A855F7);-webkit-background-clip:text;'
    f'-webkit-text-fill-color:transparent;font-weight:700;">{len(filtered_df):,}</span>'
    f' <span style="color:#8B7AA0;">total reviews &middot; showing first 500 rows</span></p>',
    unsafe_allow_html=True,
)

st.dataframe(
    data_display,
    height=350,
    width="stretch",
    column_config={
        "ABV %": st.column_config.NumberColumn(format="%.1f"),
        "Overall": st.column_config.NumberColumn(format="%.1f"),
        "Taste": st.column_config.NumberColumn(format="%.1f"),
        "Aroma": st.column_config.NumberColumn(format="%.1f"),
    },
)
st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────
st.markdown('<div class="pink-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    🍺 World Wide Beer Reviews Dashboard &nbsp;|&nbsp; Built with Python, Streamlit, Matplotlib, Seaborn & Plotly<br>
    Data Source: BeerAdvocate (1.5M Reviews)
</div>
""", unsafe_allow_html=True)
