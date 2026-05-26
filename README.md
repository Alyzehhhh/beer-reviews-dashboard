# 🍺 World Wide Beer Reviews Dashboard

A professional data visualization dashboard that analyzes **1.5 million beer reviews** from BeerAdvocate. The dashboard shows meaningful insights through **15+ chart types**, interactive filters, and a clean pastel-themed interface.

## Dataset

- **Source:** BeerAdvocate
- **Size:** 1,586,614 reviews
- **Time Span:** August 1996 to January 2012
- **Features:** 13 columns including brewery info, beer details, and 5 rating dimensions (overall, aroma, appearance, palate, taste)

## Key Insights

1. **IPAs dominate** — American IPA is the most reviewed beer style with 117K+ reviews
2. **Taste matters most** — Taste rating has the highest correlation (0.90) with overall rating
3. **Craft is king** — Small craft breweries consistently outperform large-scale producers
4. **The craft boom** — Review activity peaked between 2008-2011, matching the craft beer movement
5. **ABV sweet spot** — Most reviewed beers sit between 5-8% ABV

## How to Install

```bash
# Clone or unzip the project
cd dashboard_project

# Install required packages
pip install -r requirements.txt
```

## How to Run

```bash
# Start the dashboard
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Project Structure

```
/dashboard_project/
├── data/
│   └── beer_reviews.csv       # The original dataset (DO NOT RENAME)
├── notebooks/
│   └── analysis.ipynb         # Exploratory Data Analysis notebook
├── app.py                     # Main dashboard application
├── charts.py                  # All chart/visualization functions
├── filters.py                 # Filter and data processing functions
├── requirements.txt           # Python package list
└── README.md                  # This file
```

## Filters

All filters are connected to every chart. When you change a filter, all charts update at the same time.

| Filter | What It Does |
|--------|-------------|
| Year Range Slider | Pick a range of years to look at |
| Beer Style Dropdown | Choose one beer style to focus on |
| ABV Range Slider | Filter by alcohol percentage |
| Brewery Multi-Select | Pick specific breweries from the top 50 |
| Beer Name Search | Type a name to find specific beers |
| Reset Button | Clear all filters and start fresh |

## Charts Included

### Required Charts (10)
1. **Pie Chart** — Top 10 beer style distribution
2. **Histogram** — How overall ratings are spread out
3. **Line Chart** — Review count trends over the years
4. **Bar Chart** — Top 15 breweries by average rating
5. **Scatter Plot** — ABV vs overall rating, colored by taste
6. **Box Plot** — Rating spread across top beer styles
7. **Heatmap** — Correlation between all rating features
8. **Area Chart** — Review trends by top 5 styles over time
9. **Count Plot** — Most reviewed beer styles
10. **Violin Plot** — Taste rating distribution by style

### Bonus Charts (5)
11. **Pair Plot** — All rating dimensions compared
12. **Bubble Chart** — Brewery popularity vs quality (interactive)
13. **Radar Chart** — Rating profile for top 5 styles (interactive)
14. **Stacked Bar** — Rating breakdown by style
15. **Donut Chart** — ABV category distribution

## Tools & Libraries

- **Python 3.x** — Main language
- **Pandas** — Data loading, cleaning, filtering
- **NumPy** — Number operations
- **Matplotlib** — Charts and plots
- **Seaborn** — Statistical visualizations
- **Streamlit** — Dashboard interface
- **Plotly** — Interactive charts (bubble, radar)

## Course Info

- **Course:** Exploratory Data Analysis
- **Instructor:** Ali Hassan Sherazi
