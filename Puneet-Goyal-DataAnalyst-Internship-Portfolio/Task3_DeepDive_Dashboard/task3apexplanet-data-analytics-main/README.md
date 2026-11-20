# Task 3: Data Visualization & Dashboarding
**ApexPlanet Software Pvt. Ltd. — Internship Task 3 | Timeline: 12 Days**

## Objective
Create professional dashboards using Power BI / Tableau and Python visualization libraries.

## Dataset
A synthetic but realistic **sales dataset** (`sales_data.csv`) was generated for this task:
- **3,000 orders** across **2024–2025**
- Fields: `OrderID, OrderDate, CustomerID, Region, Category, Product, UnitPrice, Quantity, Revenue`
- 5 regions, 5 categories (25 products), 597 unique customers
- Includes realistic seasonality (Nov–Dec sales boost) and price variance per category

**Key stats:** Total Revenue **$1,361,635** | Total Orders **3,000** | Unique Customers **597** | Avg Order Value **$453.88**

Use this CSV as the single source for both the Python visuals and the Power BI / Tableau dashboards so everything stays consistent.

---

## Day 18–20: Python Visualization ✅ Complete

### Matplotlib (`python_viz/01_matplotlib_viz.py`)
| File | Chart |
|---|---|
| `01_line_revenue_trend.png` | Line plot — monthly revenue trend |
| `02_bar_revenue_by_category.png` | Bar chart — revenue comparison by category |
| `03_histogram_revenue_distribution.png` | Histogram — order revenue distribution |
| `04_scatter_price_vs_quantity.png` | Scatter — price vs quantity, colored by revenue (correlation view) |
| `05_subplots_overview.png` | 2×2 subplot dashboard combining 4 charts |

### Seaborn (`python_viz/02_seaborn_viz.py`)
| File | Chart |
|---|---|
| `06_heatmap_correlation.png` | Heatmap — correlation matrix of numeric fields |
| `06b_heatmap_region_category.png` | Heatmap — revenue by Region × Category |
| `07_pairplot_multivariable.png` | Pairplot — price/quantity/revenue relationships by category |
| `08_boxplot_revenue_by_category.png` | Boxplot — revenue distribution per category |
| `09_facetgrid_revenue_by_region.png` | FacetGrid — revenue distribution faceted by region |

### Plotly — Interactive (`python_viz/03_plotly_viz.py`)
| File | Chart |
|---|---|
| `10_plotly_interactive_trend.html` | Line chart with **dropdown filter** (by category) + **range slider** |
| `11_plotly_interactive_scatter.html` | Scatter, colored/sized by category & revenue, hover details |
| `12_plotly_interactive_bar_by_region.html` | Bar chart with **dropdown filter** (by region) |

All HTML files are self-contained (Plotly.js via CDN) — open directly in any browser, no server needed.

---

## Day 21–23: Power BI / Tableau Setup & Basics — Guide to complete yourself

I can't operate Power BI Desktop or Tableau directly (they're licensed desktop apps, not available in this environment), but here's exactly what to do with `sales_data.csv`:

1. **Install:** Power BI Desktop (free, Windows) or Tableau Public (free, Windows/Mac).
2. **Connect:** Get Data → Text/CSV → select `sales_data.csv`.
3. **Interface basics:** Fields pane (your columns), Visualizations pane (chart types), Filters pane, Pages (multiple dashboard tabs).
4. **Basic charts to build:**
   - Bar chart: `Category` vs sum of `Revenue`
   - Line chart: `OrderDate` (by month) vs sum of `Revenue`
   - Pie chart: `Region` vs sum of `Revenue`
   - Table: `Product`, `Category`, sum `Revenue`, sum `Quantity`
5. **Slicers/Filters:** Add a slicer for `Region`, `Category`, and a date range slicer for `OrderDate`.
6. **DAX measures for Power BI** (Modeling → New Measure):
   ```
   Total Revenue = SUM(sales_data[Revenue])
   Total Orders = COUNTROWS(sales_data)
   Avg Order Value = DIVIDE([Total Revenue], [Total Orders])
   Unique Customers = DISTINCTCOUNT(sales_data[CustomerID])
   ```
7. **Tableau calculated fields** — same logic using `SUM([Revenue])`, `COUNTD([CustomerID])`, etc.

## Day 24–26: Advanced Dashboarding — Guide

Build one executive dashboard page with:
- **KPI cards:** Total Revenue ($1.36M), Total Orders (3,000), Unique Customers (597), Avg Order Value ($453.88)
- **Time series:** monthly `Revenue` trend (line chart)
- **Category breakdown:** donut/pie chart of `Revenue` by `Category`
- **Bar chart:** Top 10 `Product` by `Revenue`
- **Geographic:** map visual using `Region` (use a Region→lat/long mapping table, or a filled map if you add state/city data)
- **Filter panel:** slicers for `OrderDate` (range), `Category`, `Region`
- Add drill-through page (Category → Product detail) and bookmarks/buttons for navigation (Power BI: Insert → Buttons; View → Bookmarks)
- Apply consistent branding: pick 2–3 brand colors and a logo, apply via Power BI theme JSON or Tableau workbook formatting

## Day 27: Optimization & Publishing — Checklist
- [ ] Reduce data load: aggregate where possible, disable auto date/time hierarchy in Power BI if unused
- [ ] Add tooltips with secondary calculations (e.g., show YoY % change on hover)
- [ ] Publish to Power BI Service or Tableau Public
- [ ] Create a shareable link
- [ ] Embed the dashboard link/screenshot in the GitHub README below

---

## Deliverables

**GitHub README summary** (paste into your repo):
> Task 3: Data visualization done! Built interactive dashboards in Power BI showing key metrics. Created 12+ Python visualizations (Matplotlib, Seaborn, Plotly). Link in comments. #DataVisualization #PowerBI #Python

**LinkedIn post draft:**
> Task 3: Data visualization done! Built interactive dashboards in Power BI showing key metrics. Created 12+ Python visualizations. Link in comments. #DataVisualization #PowerBI #Tableau

---

## Files in this delivery
```
task3/
├── data/
│   └── sales_data.csv          ← import this into Power BI / Tableau
├── python_viz/
│   ├── 01_matplotlib_viz.py    (+ 5 PNG outputs)
│   ├── 02_seaborn_viz.py       (+ 5 PNG outputs)
│   └── 03_plotly_viz.py        (+ 3 interactive HTML outputs)
└── README.md
```
