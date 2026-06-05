"""
app.py — World Wide Beer Reviews Dashboard
Vibrant glassmorphism design with shimmer accents.
"""

import streamlit as st
import gc
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from filters import load_data, setup_sidebar_filters, get_kpi_data, get_full_counts
from charts import (
    plot_pie_chart, plot_histogram, plot_line_chart, plot_bar_chart,
    plot_scatter, plot_box, plot_heatmap, plot_area_chart, plot_count,
    plot_violin, plot_stacked_bar, plot_donut,
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

    /* ============ ALL BABY-PINK THEME ============ */
    :root {
        --pink-50:  #FFF5FA;
        --pink-100: #FFE6F2;
        --pink-200: #FFD1E5;
        --pink-300: #FFB6D4;
        --pink-400: #FF8FBC;
        --pink-500: #FF6FA8;
        --pink-600: #F25C97;
        --pink-700: #D84B82;
        --ink:      #6B3A52;
        --ink-soft: #A56B86;
    }

    /* ── Soft baby-pink background (no gradient color shift, just pink) ── */
    .stApp {
        background: #FFF0F7;
        font-family: 'Poppins', sans-serif;
    }

    /* ── Sidebar — soft pink frosted ── */
    section[data-testid="stSidebar"] {
        background: rgba(255, 230, 242, 0.92) !important;
        backdrop-filter: blur(18px);
        border-right: 1px solid rgba(255, 143, 188, 0.25);
    }
    section[data-testid="stSidebar"] label {
        color: var(--ink) !important;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] h2 { color: var(--pink-600) !important; }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--ink) !important;
    }
    .stMarkdown { color: var(--ink); }

    /* ── KPI Cards — soft pink, glossy, premium ── */
    .kpi-card {
        background: linear-gradient(160deg, #FFFFFF 0%, #FFEAF4 100%);
        border-radius: 22px;
        padding: 22px 14px;
        text-align: center;
        border: 1px solid rgba(255, 143, 188, 0.30);
        box-shadow: 0 10px 30px rgba(242, 92, 151, 0.12),
                    inset 0 1px 0 rgba(255,255,255,0.9);
        transition: all 0.35s cubic-bezier(.4,0,.2,1);
        min-height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        position: relative; overflow: hidden;
    }
    .kpi-card::after {
        content: '';
        position: absolute; inset: 0 0 auto 0; height: 4px;
        background: linear-gradient(90deg, var(--pink-300), var(--pink-500), var(--pink-300));
    }
    .kpi-card::before {
        content: '';
        position: absolute; top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: linear-gradient(45deg, transparent 42%, rgba(255,255,255,0.45) 50%, transparent 58%);
        animation: shimmer 5s ease-in-out infinite;
    }
    @keyframes shimmer {
        0%, 100% { transform: translateX(-100%) rotate(45deg); }
        50% { transform: translateX(100%) rotate(45deg); }
    }
    .kpi-card:hover {
        transform: translateY(-7px) scale(1.025);
        box-shadow: 0 18px 44px rgba(242, 92, 151, 0.22), inset 0 1px 0 rgba(255,255,255,1);
    }
    .kpi-number {
        font-family: 'Playfair Display', serif;
        font-size: 1.9rem; font-weight: 900;
        background: linear-gradient(135deg, var(--pink-500), var(--pink-700));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 6px 0 2px 0; line-height: 1.2; white-space: nowrap;
        position: relative; z-index: 1;
    }
    .kpi-label {
        font-family: 'Poppins', sans-serif;
        font-size: 0.7rem; color: var(--ink-soft);
        font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px;
        position: relative; z-index: 1;
    }
    .kpi-icon {
        font-size: 1.7rem; margin-bottom: 2px;
        position: relative; z-index: 1;
    }

    /* ── KPI Variants — ALL pink shades (cohesive) ── */
    div.kpi-number.kpi-cyan,
    div.kpi-number.kpi-gold,
    div.kpi-number.kpi-emerald,
    div.kpi-number.kpi-purple {
        background: linear-gradient(135deg, var(--pink-400), var(--pink-600)) !important;
        -webkit-background-clip: text !important; background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    div.kpi-number.kpi-gold {
        background: linear-gradient(135deg, var(--pink-500), var(--pink-700)) !important;
        -webkit-background-clip: text !important; background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }

    /* ── Chart Containers — clean white-pink panels ── */
    .chart-container {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 22px;
        padding: 22px;
        margin: 10px 0;
        border: 1px solid rgba(255, 143, 188, 0.22);
        box-shadow: 0 6px 26px rgba(242, 92, 151, 0.10);
        transition: box-shadow 0.3s ease, transform 0.3s ease;
    }
    .chart-container:hover {
        box-shadow: 0 12px 42px rgba(242, 92, 151, 0.18);
        transform: translateY(-2px);
    }

    /* ── Section Headers — pink pill with left accent ── */
    .section-header {
        background: linear-gradient(135deg, var(--pink-500) 0%, var(--pink-700) 100%);
        color: white !important;
        padding: 14px 28px;
        border-radius: 16px;
        font-family: 'Playfair Display', serif;
        font-size: 1.35rem; font-weight: 700;
        margin: 38px 0 20px 0;
        box-shadow: 0 8px 22px rgba(216, 75, 130, 0.30);
        letter-spacing: 0.5px;
        border-left: 6px solid #FFD1E5;
    }

    /* ── Title ── */
    .dash-title { text-align: center; padding: 30px 20px 12px 20px; }
    .dash-title h1 {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.9rem !important; font-weight: 900 !important;
        background: linear-gradient(135deg, var(--pink-400), var(--pink-600), var(--pink-700)) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 5px !important;
    }
    .dash-title p {
        font-family: 'Poppins', sans-serif; color: var(--ink-soft);
        font-size: 1rem; margin-top: 0;
    }

    .pink-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--pink-300), var(--pink-500), var(--pink-300), transparent);
        border: none; margin: 12px 0 28px 0; border-radius: 2px;
    }

    .footer {
        text-align: center; padding: 30px; color: var(--ink-soft);
        font-size: 0.85rem; font-family: 'Poppins', sans-serif;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in { animation: fadeInUp 0.6s ease-out forwards; }

    .stButton > button {
        background: linear-gradient(135deg, var(--pink-500), var(--pink-700)) !important;
        color: white !important; border: none !important;
        border-radius: 14px !important; font-weight: 600 !important;
        padding: 9px 22px !important;
        box-shadow: 0 5px 16px rgba(216, 75, 130, 0.30) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        box-shadow: 0 8px 26px rgba(216, 75, 130, 0.45) !important;
        transform: translateY(-2px);
    }

    /* Sidebar widget accents -> pink */
    section[data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] { background: var(--pink-600) !important; }
    section[data-testid="stSidebar"] [data-baseweb="tag"] {
        background: var(--pink-500) !important; color: #fff !important;
    }

    .insight-box {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(8px);
        border-left: 5px solid var(--pink-500);
        border-radius: 0 14px 14px 0;
        padding: 14px 20px; margin: 14px 0;
        font-size: 0.92rem; color: var(--ink);
        box-shadow: 0 3px 14px rgba(242, 92, 151, 0.08);
    }

    /* ── Data Sheet — pink table ── */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 143, 188, 0.28) !important;
        border-radius: 16px !important;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(242, 92, 151, 0.08);
    }
    div[data-testid="stDataFrame"] th,
    div[data-testid="stDataFrame"] [role="columnheader"] {
        background: linear-gradient(135deg, var(--pink-100), var(--pink-200)) !important;
        color: var(--pink-700) !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
    }
    div[data-testid="stDataFrame"] td,
    div[data-testid="stDataFrame"] [role="gridcell"] {
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.8rem !important;
        color: var(--ink) !important;
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

# ── Empty / too-small data guard ──────────────────────────────────
# When filters narrow results to (near) zero, charts get NaN axis limits
# and crash the page. Stop early with a friendly message instead.
if len(filtered_df) < 5:
    st.warning(
        "🔍 **No reviews match these filters** (or too few to chart). "
        "Try widening your filters or click **🔄 Reset All Filters** in the sidebar."
    )
    st.stop()


def safe_chart(plot_fn, data):
    """Render a chart, but never let one broken chart crash the whole page."""
    try:
        fig = plot_fn(data)
        fig.set_dpi(150)  # crisp, high-resolution rendering
        st.pyplot(fig, width="stretch", dpi=150)
        plt.close(fig)
    except Exception:
        st.info("Not enough data to render this chart for the current filters.")


# ══════════════════════════════════════════════════════════════════
# SECTION 1: DISTRIBUTION & COMPOSITION
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📊 Distribution & Composition</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    safe_chart(plot_pie_chart, filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    safe_chart(plot_donut, filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
    IPAs and Pale Ales dominate the beer world. Most craft beers land in the 5–8% ABV sweet spot.
</div>
""", unsafe_allow_html=True)

col_c, col_d = st.columns(2)
with col_c:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    safe_chart(plot_histogram, filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)

with col_d:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    safe_chart(plot_count, filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 2: TRENDS OVER TIME
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📈 Trends Over Time</div>', unsafe_allow_html=True)

col_e, col_f = st.columns(2)
with col_e:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    safe_chart(plot_line_chart, filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)

with col_f:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    safe_chart(plot_area_chart, filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
    Beer reviewing took off around 2004 and peaked in 2008–2011. The craft beer boom is clearly visible, especially for IPAs.
</div>
""", unsafe_allow_html=True)


gc.collect()
# ══════════════════════════════════════════════════════════════════
# SECTION 3: RATINGS & COMPARISONS
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">⭐ Ratings & Comparisons</div>', unsafe_allow_html=True)

col_g, col_h = st.columns(2)
with col_g:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    safe_chart(plot_bar_chart, filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)

with col_h:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    safe_chart(plot_stacked_bar, filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)


gc.collect()
# ══════════════════════════════════════════════════════════════════
# SECTION 4: RELATIONSHIPS & DEEP DIVE
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">🔬 Relationships & Deep Dive</div>', unsafe_allow_html=True)

col_i, col_j = st.columns(2)
with col_i:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    safe_chart(plot_scatter, filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)

with col_j:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    safe_chart(plot_heatmap, filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
    Taste has the strongest link to overall rating (0.90 correlation). ABV barely affects how people rate a beer.
</div>
""", unsafe_allow_html=True)

col_k, col_l = st.columns(2)
with col_k:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    safe_chart(plot_box, filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)

with col_l:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    safe_chart(plot_violin, filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)

gc.collect()


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
data_display = filtered_df[avail].rename(columns={c: _col_map[c] for c in avail}).head(200).reset_index(drop=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown(
    f'<p style="font-family:Poppins,sans-serif;font-size:0.82rem;margin-bottom:6px;">'
    f'<span style="background:linear-gradient(135deg,#FF4D8D,#A855F7);-webkit-background-clip:text;'
    f'-webkit-text-fill-color:transparent;font-weight:700;">{len(filtered_df):,}</span>'
    f' <span style="color:#8B7AA0;">total reviews &middot; showing first 200 rows</span></p>',
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
    🍺 World Wide Beer Reviews Dashboard &nbsp;|&nbsp; Built with Python, Streamlit, Matplotlib & Seaborn<br>
    Data Source: BeerAdvocate (1.5M Reviews)
</div>
""", unsafe_allow_html=True)
