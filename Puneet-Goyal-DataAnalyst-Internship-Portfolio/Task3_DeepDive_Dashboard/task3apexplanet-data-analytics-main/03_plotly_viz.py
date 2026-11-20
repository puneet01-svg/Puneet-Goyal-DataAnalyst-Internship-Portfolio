import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

OUT = "/home/claude/task3/python_viz"
df = pd.read_csv("/home/claude/task3/data/sales_data.csv", parse_dates=["OrderDate"])

# ============================================================
# 1. Interactive line chart with dropdown filter (by Region) + range slider
# ============================================================
categories = sorted(df["Category"].unique())
daily_all = df.set_index("OrderDate").resample("W")["Revenue"].sum().reset_index()

fig = go.Figure()

# Trace for "All"
fig.add_trace(go.Scatter(x=daily_all["OrderDate"], y=daily_all["Revenue"],
                          mode="lines", name="All Categories", visible=True,
                          line=dict(color="#2563eb", width=2)))

for cat in categories:
    d = df[df["Category"] == cat].set_index("OrderDate").resample("W")["Revenue"].sum().reset_index()
    fig.add_trace(go.Scatter(x=d["OrderDate"], y=d["Revenue"], mode="lines",
                              name=cat, visible=False))

buttons = [dict(label="All Categories",
                method="update",
                args=[{"visible": [True] + [False]*len(categories)},
                      {"title": "Weekly Revenue Trend - All Categories"}])]
for i, cat in enumerate(categories):
    vis = [False]*(len(categories)+1)
    vis[i+1] = True
    buttons.append(dict(label=cat, method="update",
                         args=[{"visible": vis}, {"title": f"Weekly Revenue Trend - {cat}"}]))

fig.update_layout(
    title="Weekly Revenue Trend - All Categories",
    updatemenus=[dict(active=0, buttons=buttons, x=1.15, y=1.1, xanchor="left")],
    xaxis=dict(rangeslider=dict(visible=True), title="Date"),
    yaxis=dict(title="Revenue ($)"),
    template="plotly_white",
    height=550,
)
fig.write_html(f"{OUT}/10_plotly_interactive_trend.html", include_plotlyjs="cdn")

# ============================================================
# 2. Interactive scatter with dropdown (color by Region/Category) + range slider on x
# ============================================================
fig2 = px.scatter(df, x="UnitPrice", y="Quantity", color="Category", size="Revenue",
                   hover_data=["Product", "Region", "OrderDate"],
                   title="Price vs Quantity (colored by Category)",
                   template="plotly_white", opacity=0.7)
fig2.update_layout(
    updatemenus=[dict(
        buttons=[
            dict(label="By Category", method="restyle", args=["marker.color", [None]]),
        ],
        direction="down", x=1.15, y=1.1
    )],
    height=550,
)
fig2.write_html(f"{OUT}/11_plotly_interactive_scatter.html", include_plotlyjs="cdn")

# ============================================================
# 3. Interactive bar chart: revenue by product, dropdown to filter by Region
# ============================================================
regions = sorted(df["Region"].unique())
fig3 = go.Figure()

prod_all = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False).reset_index()
fig3.add_trace(go.Bar(x=prod_all["Product"], y=prod_all["Revenue"], name="All Regions", visible=True,
                       marker_color="#059669"))

for r in regions:
    d = df[df["Region"] == r].groupby("Product")["Revenue"].sum().sort_values(ascending=False).reset_index()
    fig3.add_trace(go.Bar(x=d["Product"], y=d["Revenue"], name=r, visible=False, marker_color="#f59e0b"))

buttons3 = [dict(label="All Regions", method="update",
                  args=[{"visible": [True] + [False]*len(regions)},
                        {"title": "Revenue by Product - All Regions"}])]
for i, r in enumerate(regions):
    vis = [False]*(len(regions)+1)
    vis[i+1] = True
    buttons3.append(dict(label=r, method="update",
                          args=[{"visible": vis}, {"title": f"Revenue by Product - {r}"}]))

fig3.update_layout(
    title="Revenue by Product - All Regions",
    updatemenus=[dict(active=0, buttons=buttons3, x=1.15, y=1.1)],
    template="plotly_white",
    xaxis_tickangle=-40,
    height=550,
)
fig3.write_html(f"{OUT}/12_plotly_interactive_bar_by_region.html", include_plotlyjs="cdn")

print("Plotly interactive HTML visualizations saved.")
