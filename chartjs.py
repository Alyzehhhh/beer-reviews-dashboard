"""
chartjs.py — Interactive Chart.js charts embedded inside Streamlit.

These cover the 6 "interactive" charts (Pie, Histogram, Line, Bar, Bubble, Funnel).
Each function returns an HTML string to render via st.components.v1.html.
The actual statistics are computed in Python (pandas); Chart.js only draws.

Baby-pink theme to match the rest of the dashboard.
"""

import json
import numpy as np
import pandas as pd

# ── Baby-pink palette (matches charts.py / app.py) ──
PINK = {
    "p50": "#FFF5FA", "p100": "#FFE6F2", "p200": "#FFD1E5", "p300": "#FFB6D4",
    "p400": "#FF8FBC", "p500": "#FF6FA8", "p600": "#F25C97", "p700": "#D84B82",
    "ink": "#6B3A52", "ink_soft": "#A56B86", "grid": "#FFE0EE",
}
PALETTE = ["#FF6FA8", "#F25C97", "#FF8FBC", "#D84B82", "#FFA6C9",
           "#E86FA0", "#FFB6D4", "#FF9DC0", "#FFD1E5", "#FFC2DD"]

_CHART_CDN = "https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"


def _shell(canvas_id, config_js, height=360, extra_js=""):
    """Wrap a Chart.js config in a full self-contained HTML doc."""
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<script src="{_CHART_CDN}"></script>
<style>
  html,body {{ margin:0; padding:0; background:transparent;
    font-family:'Poppins',-apple-system,Segoe UI,sans-serif; }}
  .wrap {{
    background:rgba(255,255,255,0.85);
    border:1px solid rgba(255,143,188,0.22);
    border-radius:22px; padding:18px 18px 10px 18px;
    box-shadow:0 6px 26px rgba(242,92,151,0.10);
  }}
  .ctitle {{
    font-family:'Playfair Display',Georgia,serif; font-style:italic;
    font-weight:700; font-size:1.05rem; color:{PINK['p600']};
    text-align:center; margin:2px 0 12px 0;
  }}
  .cbox {{ position:relative; height:{height}px; width:100%; animation:fade .7s ease; }}
  @keyframes fade {{ from {{opacity:0; transform:translateY(8px);}} to {{opacity:1;transform:none;}} }}
</style></head>
<body>
  <div class="wrap">
    <div class="ctitle">{{TITLE}}</div>
    <div class="cbox"><canvas id="{canvas_id}"></canvas></div>
  </div>
<script>
  const ink="{PINK['ink']}", inkSoft="{PINK['ink_soft']}", grid="{PINK['grid']}";
  Chart.defaults.font.family="'Poppins',sans-serif";
  Chart.defaults.color=inkSoft;
  const ctx=document.getElementById("{canvas_id}");
  const cfg={config_js};
  document.querySelector('.ctitle').textContent=cfg.__title||'';
  delete cfg.__title;

  // ── Click interactions: re-animate the whole chart + pulse/glow the clicked element ──
  cfg.options = cfg.options || {{}};
  const _userOnClick = cfg.options.onClick;
  cfg.options.onClick = function(evt, elements, chartInstance){{
    // 1) re-run the entry animation (redraw)
    chartInstance.reset();
    chartInstance.update();
    // 2) pulse + glow the clicked slice/bar/point
    if(elements && elements.length){{
      const el = elements[0];
      const ds = chartInstance.data.datasets[el.datasetIndex];
      const idx = el.index;
      const orig = Array.isArray(ds.backgroundColor) ? ds.backgroundColor[idx] : ds.backgroundColor;
      ctx.style.transition = "filter .18s ease, transform .18s ease";
      ctx.style.filter = "drop-shadow(0 0 16px #FF6FA8) brightness(1.12)";
      ctx.style.transform = "scale(1.015)";
      // glow the element itself by temporarily boosting it
      const setColor = (c)=>{{ if(Array.isArray(ds.backgroundColor)) ds.backgroundColor[idx]=c; else ds.backgroundColor=c; chartInstance.update('none'); }};
      setColor("#FF3D86");
      // little petal burst at the click point
      petalBurst(evt.native ? evt.native.clientX : evt.x, evt.native ? evt.native.clientY : evt.y);
      setTimeout(()=>{{
        ctx.style.filter=""; ctx.style.transform="";
        setColor(orig);
      }}, 650);
    }}
    if(typeof _userOnClick === 'function') _userOnClick(evt, elements, chartInstance);
  }};

  // sparkle/petal burst helper
  function petalBurst(x, y){{
    if(x==null||y==null) return;
    const flowers=["🌸","🌷","✨","💖","🌼"];
    for(let i=0;i<7;i++){{
      const s=document.createElement('div');
      s.textContent=flowers[Math.floor(Math.random()*flowers.length)];
      s.style.cssText="position:fixed;left:"+x+"px;top:"+y+"px;font-size:16px;pointer-events:none;z-index:9999;transition:all .8s cubic-bezier(.2,.8,.3,1);opacity:1;";
      document.body.appendChild(s);
      const ang=Math.random()*Math.PI*2, dist=40+Math.random()*55;
      requestAnimationFrame(()=>{{
        s.style.left=(x+Math.cos(ang)*dist)+"px";
        s.style.top=(y+Math.sin(ang)*dist)+"px";
        s.style.opacity="0";
        s.style.transform="rotate("+(Math.random()*360)+"deg) scale(0.6)";
      }});
      setTimeout(()=>s.remove(),850);
    }}
  }}

  const chart=new Chart(ctx,cfg);
  // gentle hover cursor cue
  ctx.style.cursor="pointer";
  {extra_js}
</script>
</body></html>"""


def _tooltip_pink():
    return {
        "backgroundColor": PINK["p700"],
        "titleColor": "#fff", "bodyColor": "#fff",
        "borderColor": PINK["p300"], "borderWidth": 1,
        "padding": 10, "cornerRadius": 10, "displayColors": True,
        "titleFont": {"weight": "600"},
    }


# ── 1. PIE — Top 10 styles ──
def pie_html(df, height=320):
    top = df["beer_style"].value_counts().head(10)
    cfg = {
        "type": "doughnut",
        "data": {
            "labels": top.index.tolist(),
            "datasets": [{
                "data": [int(v) for v in top.values],
                "backgroundColor": PALETTE,
                "borderColor": "#fff", "borderWidth": 3,
                "hoverOffset": 14, "hoverBorderWidth": 3,
            }],
        },
        "options": {
            "responsive": True, "maintainAspectRatio": False,
            "cutout": "52%",
            "animation": {"animateRotate": True, "animateScale": True, "duration": 1100},
            "plugins": {
                "legend": {"position": "right", "labels": {"boxWidth": 12, "font": {"size": 11}, "padding": 8}},
                "tooltip": {**_tooltip_pink(),
                            "callbacks": {}},
            },
        },
        "__title": "Top 10 Beer Styles",
    }
    return _shell("pieC", json.dumps(cfg), height)


# ── 2. HISTOGRAM — overall rating distribution (binned bar) ──
def histogram_html(df, height=320):
    vals = df["review_overall"].dropna().values
    counts, edges = np.histogram(vals, bins=20)
    labels = [f"{edges[i]:.1f}" for i in range(len(counts))]
    # gradient-ish: map each bar to palette ramp
    bg = []
    for i in range(len(counts)):
        t = i / max(1, len(counts) - 1)
        bg.append(PALETTE[int(t * (len(PALETTE) - 1))])
    cfg = {
        "type": "bar",
        "data": {"labels": labels, "datasets": [{
            "label": "Reviews", "data": [int(c) for c in counts],
            "backgroundColor": bg, "borderColor": "#fff", "borderWidth": 1,
            "borderRadius": 6, "hoverBackgroundColor": PINK["p700"],
        }]},
        "options": {
            "responsive": True, "maintainAspectRatio": False,
            "animation": {"duration": 1000, "easing": "easeOutQuart"},
            "plugins": {"legend": {"display": False}, "tooltip": _tooltip_pink()},
            "scales": {
                "x": {"title": {"display": True, "text": "Overall Rating"},
                      "grid": {"display": False}},
                "y": {"title": {"display": True, "text": "Number of Reviews"},
                      "grid": {"color": grid_color()}, "beginAtZero": True},
            },
        },
        "__title": "Distribution of Overall Ratings",
    }
    return _shell("histC", json.dumps(cfg), height)


def grid_color():
    return PINK["grid"]


# ── 3. LINE — reviews per year ──
def line_html(df, height=320):
    yearly = df.groupby("review_year").size().reset_index(name="count").sort_values("review_year")
    cfg = {
        "type": "line",
        "data": {"labels": [int(y) for y in yearly["review_year"]],
                 "datasets": [{
                     "label": "Reviews", "data": [int(c) for c in yearly["count"]],
                     "borderColor": PINK["p500"], "backgroundColor": "rgba(255,111,168,0.15)",
                     "fill": True, "tension": 0.4, "borderWidth": 3,
                     "pointBackgroundColor": PINK["p600"], "pointBorderColor": "#fff",
                     "pointBorderWidth": 2, "pointRadius": 5, "pointHoverRadius": 8,
                 }]},
        "options": {
            "responsive": True, "maintainAspectRatio": False,
            "animation": {"duration": 1200, "easing": "easeInOutCubic"},
            "interaction": {"mode": "index", "intersect": False},
            "plugins": {"legend": {"display": False}, "tooltip": _tooltip_pink()},
            "scales": {
                "x": {"title": {"display": True, "text": "Year"}, "grid": {"display": False}},
                "y": {"title": {"display": True, "text": "Number of Reviews"},
                      "grid": {"color": PINK["grid"]}, "beginAtZero": True},
            },
        },
        "__title": "Review Trends Over the Years",
    }
    return _shell("lineC", json.dumps(cfg), height)


# ── 4. BAR — Top 15 breweries by avg rating ──
def bar_html(df, height=420):
    brew = df.groupby("brewery_name").agg(
        avg=("review_overall", "mean"), cnt=("review_overall", "count")).reset_index()
    brew = brew[brew["cnt"] >= 30].nlargest(15, "avg")
    if brew.empty:
        brew = df.groupby("brewery_name").agg(
            avg=("review_overall", "mean"), cnt=("review_overall", "count")).reset_index().nlargest(15, "avg")
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(brew))]
    cfg = {
        "type": "bar",
        "data": {"labels": brew["brewery_name"].tolist(), "datasets": [{
            "label": "Avg Rating", "data": [round(float(v), 2) for v in brew["avg"]],
            "backgroundColor": colors, "borderColor": "#fff", "borderWidth": 1,
            "borderRadius": 6, "hoverBackgroundColor": PINK["p700"],
        }]},
        "options": {
            "indexAxis": "y", "responsive": True, "maintainAspectRatio": False,
            "animation": {"duration": 1100, "easing": "easeOutQuart"},
            "plugins": {"legend": {"display": False}, "tooltip": _tooltip_pink()},
            "scales": {
                "x": {"title": {"display": True, "text": "Average Overall Rating"},
                      "grid": {"color": PINK["grid"]}, "beginAtZero": False},
                "y": {"grid": {"display": False}, "ticks": {"font": {"size": 10}}},
            },
        },
        "__title": "Top 15 Breweries by Rating",
    }
    return _shell("barC", json.dumps(cfg), height)


# ── 5. BUBBLE — breweries: avg rating vs review count (size=count) ──
def bubble_html(df, height=380):
    brew = df.groupby("brewery_name").agg(
        avg=("review_overall", "mean"), cnt=("review_overall", "count")).reset_index()
    brew = brew[brew["cnt"] >= 20].nlargest(40, "cnt")
    if brew.empty:
        brew = df.groupby("brewery_name").agg(
            avg=("review_overall", "mean"), cnt=("review_overall", "count")).reset_index().nlargest(40, "cnt")
    maxc = max(1, int(brew["cnt"].max()))
    points = [{
        "x": round(float(r["avg"]), 3),
        "y": int(r["cnt"]),
        "r": float(np.clip(r["cnt"] / maxc * 26, 5, 28)),
        "name": r["brewery_name"],
    } for _, r in brew.iterrows()]
    cfg = {
        "type": "bubble",
        "data": {"datasets": [{
            "label": "Breweries",
            "data": points,
            "backgroundColor": "rgba(255,111,168,0.55)",
            "borderColor": PINK["p700"], "borderWidth": 1,
            "hoverBackgroundColor": "rgba(216,75,130,0.75)",
        }]},
        "options": {
            "responsive": True, "maintainAspectRatio": False,
            "animation": {"duration": 1100},
            "plugins": {"legend": {"display": False},
                        "tooltip": {**_tooltip_pink()}},
            "scales": {
                "x": {"title": {"display": True, "text": "Average Rating"},
                      "grid": {"color": PINK["grid"]}},
                "y": {"title": {"display": True, "text": "Total Reviews"},
                      "grid": {"color": PINK["grid"]}, "beginAtZero": True},
            },
        },
        "__title": "Breweries — Rating vs Popularity",
    }
    extra = """
    chart.options.plugins.tooltip.callbacks = {
      label: function(c){ const d=c.raw; return d.name+': '+d.y+' reviews, avg '+d.x; }
    };
    chart.update();
    """
    return _shell("bubbleC", json.dumps(cfg), height, extra_js=extra)


# ── 6. FUNNEL — review counts by ABV category (styled horizontal bar) ──
def funnel_html(df, height=320):
    bins = [0, 4, 6, 8, 12, 60]
    labels = ["Light (0-4%)", "Medium (4-6%)", "Strong (6-8%)", "V.Strong (8-12%)", "Extreme (12%+)"]
    cats = pd.cut(df["beer_abv"], bins=bins, labels=labels, right=False)
    counts = cats.value_counts().reindex(labels).fillna(0)
    # sort descending so it reads like a funnel (widest first)
    order = counts.sort_values(ascending=False)
    cfg = {
        "type": "bar",
        "data": {"labels": order.index.tolist(), "datasets": [{
            "label": "Reviews", "data": [int(v) for v in order.values],
            "backgroundColor": PALETTE[:len(order)], "borderColor": "#fff",
            "borderWidth": 1, "borderRadius": 8, "hoverBackgroundColor": PINK["p700"],
        }]},
        "options": {
            "indexAxis": "y", "responsive": True, "maintainAspectRatio": False,
            "animation": {"duration": 1100, "easing": "easeOutQuart"},
            "plugins": {"legend": {"display": False}, "tooltip": _tooltip_pink()},
            "scales": {
                "x": {"title": {"display": True, "text": "Number of Reviews"},
                      "grid": {"color": PINK["grid"]}, "beginAtZero": True},
                "y": {"grid": {"display": False}},
            },
        },
        "__title": "Reviews by ABV Category (Funnel)",
    }
    return _shell("funnelC", json.dumps(cfg), height)
