"""
filters.py - Data loading, cleaning, and interactive filtering.
Optimized for speed: typed CSV reads, lean sampling, hardcoded full counts.
"""

import pandas as pd
import numpy as np
import streamlit as st
import os
import gc

# Column dtypes to speed up read_csv (~40% faster than auto-detect)
_DTYPES = {
    "brewery_id": "int32",
    "brewery_name": "str",
    "review_time": "int32",
    "review_overall": "float32",
    "review_aroma": "float32",
    "review_appearance": "float32",
    "review_profilename": "str",
    "beer_style": "str",
    "review_palate": "float32",
    "review_taste": "float32",
    "beer_name": "str",
    "beer_abv": "float32",
    "beer_beerid": "int32",
}


@st.cache_data(show_spinner="Loading beer data...")
def load_data():
    """Load, clean, and sample the beer reviews dataset.
    Memory-optimized: reads .gz directly, samples early to stay under 512MB RAM.
    """
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    data_path = os.path.join(data_dir, "beer_reviews.csv")
    gz_path = os.path.join(data_dir, "beer_reviews.csv.gz")

    # Prefer reading .gz directly (avoids decompressing 172MB to disk)
    if os.path.exists(gz_path):
        read_path = gz_path
    elif os.path.exists(data_path):
        read_path = data_path
    else:
        st.error(
            f"**Dataset not found!**\n\n"
            f"Expected at: `{data_path}` or `{gz_path}`\n\n"
            f"Please download `beer_reviews.csv` from the BeerAdvocate dataset "
            f"and place it in the `data/` folder next to `app.py`."
        )
        st.stop()

    # Read in small chunks to limit peak memory on free-tier (512MB)
    chunks = []
    total_rows = 0
    for chunk in pd.read_csv(read_path, dtype=_DTYPES, chunksize=100_000):
        total_rows += len(chunk)
        chunks.append(chunk.sample(n=min(3_000, len(chunk)), random_state=42))
        del chunk
        gc.collect()
    df = pd.concat(chunks, ignore_index=True)
    del chunks
    gc.collect()

    # Quick fills
    df["brewery_name"] = df["brewery_name"].fillna("Unknown")
    df["review_profilename"] = df["review_profilename"].fillna("Anonymous")
    df["beer_abv"] = df["beer_abv"].fillna(df["beer_abv"].mean())

    # Remove reviews outside 1-5 range
    mask = (
        df["review_overall"].between(1, 5)
        & df["review_aroma"].between(1, 5)
        & df["review_taste"].between(1, 5)
    )
    df = df.loc[mask]

    # Derived columns
    df["review_year"] = pd.to_datetime(df["review_time"], unit="s").dt.year.astype("int16")
    df["overall_score"] = (
        (df["review_aroma"] + df["review_appearance"] + df["review_palate"]
         + df["review_taste"] + df["review_overall"]) / 5
    ).astype("float32")

    # Drop heavy columns we no longer need
    df.drop(columns=["review_time"], inplace=True)

    # Drop columns we don't need to save memory
    drop_cols = [c for c in ["review_profilename", "brewery_id", "beer_beerid"] if c in df.columns]
    if drop_cols:
        df.drop(columns=drop_cols, inplace=True)

    # Sample for performance — 15K keeps memory safe under 512MB free tier
    if len(df) > 15_000:
        df = df.sample(n=15_000, random_state=42).reset_index(drop=True)
    gc.collect()

    return df


def get_full_counts():
    """Return real dataset totals — hardcoded to avoid re-reading 180MB CSV."""
    return {
        "total_reviews": 1_586_614,
        "total_beers": 66_055,
        "total_breweries": 5_743,
    }


def setup_sidebar_filters(df):
    """Create sidebar filters and return (filtered_df, filters_active)."""

    st.sidebar.markdown(
        '<div style="text-align:center;padding:10px 0 20px 0;">'
        '<h2 style="color:#FF6B9D;margin:0;font-family:Georgia,serif;">🍺 Filters</h2>'
        '<p style="color:#999;font-size:13px;margin:0;">Narrow down the reviews</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key.startswith("filter_"):
                del st.session_state[key]
        st.rerun()

    st.sidebar.markdown("---")

    # 1. Year Range
    min_year = int(df["review_year"].min())
    max_year = int(df["review_year"].max())
    year_range = st.sidebar.slider(
        "📅 Review Year Range",
        min_value=min_year, max_value=max_year,
        value=(min_year, max_year), key="filter_year",
    )

    st.sidebar.markdown("---")

    # 2. Beer Style
    all_styles = sorted(df["beer_style"].unique().tolist())
    selected_style = st.sidebar.selectbox(
        "🍻 Beer Style",
        options=["All Styles"] + all_styles,
        key="filter_style",
    )

    st.sidebar.markdown("---")

    # 3. ABV Range
    abv_range = st.sidebar.slider(
        "🔢 ABV Range (%)",
        min_value=0.0, max_value=30.0,
        value=(0.0, 30.0), step=0.5,
        key="filter_abv",
    )

    st.sidebar.markdown("---")

    # 4. Brewery Multi-Select
    top_breweries = df["brewery_name"].value_counts().head(50).index.tolist()
    selected_breweries = st.sidebar.multiselect(
        "🏭 Breweries (Top 50)",
        options=top_breweries, default=[],
        key="filter_breweries",
    )

    st.sidebar.markdown("---")

    # 5. Beer Name Search
    search_text = st.sidebar.text_input(
        "🔍 Search Beer Name", value="", key="filter_search",
    )

    # ── Apply Filters ──
    filtered = df

    # Year
    if year_range[0] != min_year or year_range[1] != max_year:
        filtered = filtered[
            filtered["review_year"].between(year_range[0], year_range[1])
        ]

    # Style
    if selected_style != "All Styles":
        filtered = filtered[filtered["beer_style"] == selected_style]

    # ABV
    if abv_range[0] != 0.0 or abv_range[1] != 30.0:
        filtered = filtered[
            filtered["beer_abv"].between(abv_range[0], abv_range[1])
        ]

    # Brewery
    if selected_breweries:
        filtered = filtered[filtered["brewery_name"].isin(selected_breweries)]

    # Search
    if search_text.strip():
        filtered = filtered[
            filtered["beer_name"].str.lower().str.contains(
                search_text.strip().lower(), na=False
            )
        ]

    filters_active = (
        year_range[0] != min_year
        or year_range[1] != max_year
        or selected_style != "All Styles"
        or abv_range[0] != 0.0
        or abv_range[1] != 30.0
        or len(selected_breweries) > 0
        or search_text.strip() != ""
    )

    return filtered, filters_active


def get_kpi_data(df):
    """KPI summary from the (filtered) sample."""
    if len(df) == 0:
        return {"avg_rating": 0, "top_style": "N/A", "avg_abv": 0}
    return {
        "avg_rating": round(float(df["review_overall"].mean()), 2),
        "top_style": df["beer_style"].value_counts().index[0],
        "avg_abv": round(float(df["beer_abv"].mean()), 1),
    }
