import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.style.use("seaborn-v0_8-whitegrid")
OUT = "/home/claude/task3/python_viz"

df = pd.read_csv("/home/claude/task3/data/sales_data.csv", parse_dates=["OrderDate"])

# ---------- 1. Line plot: revenue trend over time (monthly) ----------
monthly = df.set_index("OrderDate").resample("ME")["Revenue"].sum()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly.index, monthly.values, marker="o", color="#2563eb", linewidth=2)
ax.set_title("Monthly Revenue Trend (2024-2025)", fontsize=14, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig(f"{OUT}/01_line_revenue_trend.png", dpi=150)
plt.close()

# ---------- 2. Bar chart: revenue by category (comparison) ----------
cat_rev = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(cat_rev.index, cat_rev.values, color="#059669")
ax.set_title("Total Revenue by Category", fontsize=14, fontweight="bold")
ax.set_ylabel("Revenue ($)")
for b in bars:
    ax.text(b.get_x() + b.get_width()/2, b.get_height(), f"${b.get_height():,.0f}",
            ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUT}/02_bar_revenue_by_category.png", dpi=150)
plt.close()

# ---------- 3. Histogram: distribution of order revenue ----------
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(df["Revenue"], bins=40, color="#7c3aed", edgecolor="white")
ax.set_title("Distribution of Order Revenue", fontsize=14, fontweight="bold")
ax.set_xlabel("Revenue ($)")
ax.set_ylabel("Number of Orders")
plt.tight_layout()
plt.savefig(f"{OUT}/03_histogram_revenue_distribution.png", dpi=150)
plt.close()

# ---------- 4. Scatter plot: correlation (price vs quantity, colored by revenue) ----------
fig, ax = plt.subplots(figsize=(9, 5))
sc = ax.scatter(df["UnitPrice"], df["Quantity"], c=df["Revenue"], cmap="viridis", alpha=0.6, s=25)
ax.set_title("Unit Price vs Quantity Ordered", fontsize=14, fontweight="bold")
ax.set_xlabel("Unit Price ($)")
ax.set_ylabel("Quantity")
cbar = plt.colorbar(sc)
cbar.set_label("Revenue ($)")
plt.tight_layout()
plt.savefig(f"{OUT}/04_scatter_price_vs_quantity.png", dpi=150)
plt.close()

# ---------- 5. Subplots: multiple charts together ----------
fig, axes = plt.subplots(2, 2, figsize=(13, 9))

region_rev = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
axes[0, 0].bar(region_rev.index, region_rev.values, color="#f59e0b")
axes[0, 0].set_title("Revenue by Region")
axes[0, 0].tick_params(axis="x", rotation=30)

daily = df.set_index("OrderDate").resample("W")["Revenue"].sum()
axes[0, 1].plot(daily.index, daily.values, color="#ef4444")
axes[0, 1].set_title("Weekly Revenue Trend")
axes[0, 1].tick_params(axis="x", rotation=30)

axes[1, 0].hist(df["Quantity"], bins=range(1, 7), color="#0ea5e9", edgecolor="white", align="left")
axes[1, 0].set_title("Quantity per Order")
axes[1, 0].set_xticks(range(1, 6))

top_products = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(8)
axes[1, 1].barh(top_products.index[::-1], top_products.values[::-1], color="#8b5cf6")
axes[1, 1].set_title("Top 8 Products by Revenue")

fig.suptitle("Sales Overview Dashboard (Matplotlib Subplots)", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUT}/05_subplots_overview.png", dpi=150)
plt.close()

print("Matplotlib visualizations saved.")
