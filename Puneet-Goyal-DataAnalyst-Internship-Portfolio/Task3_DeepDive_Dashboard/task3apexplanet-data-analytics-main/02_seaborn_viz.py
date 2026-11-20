import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")
OUT = "/home/claude/task3/python_viz"

df = pd.read_csv("/home/claude/task3/data/sales_data.csv", parse_dates=["OrderDate"])
df["Month"] = df["OrderDate"].dt.month_name().str[:3]
df["MonthNum"] = df["OrderDate"].dt.month

# ---------- 1. Heatmap: correlation matrix ----------
numeric_df = df[["UnitPrice", "Quantity", "Revenue", "MonthNum"]]
corr = numeric_df.corr()
fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", square=True, ax=ax)
ax.set_title("Correlation Matrix (Numeric Features)", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUT}/06_heatmap_correlation.png", dpi=150)
plt.close()

# Also a heatmap of revenue by Region x Category (pivot) - more business-relevant
pivot = df.pivot_table(index="Region", columns="Category", values="Revenue", aggfunc="sum")
fig, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(pivot, annot=True, fmt=",.0f", cmap="YlGnBu", ax=ax)
ax.set_title("Revenue Heatmap: Region x Category", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUT}/06b_heatmap_region_category.png", dpi=150)
plt.close()

# ---------- 2. Pairplot: multi-variable relationships ----------
sample = df.sample(500, random_state=1)  # sample for readability/perf
g = sns.pairplot(sample[["UnitPrice", "Quantity", "Revenue", "Category"]], hue="Category",
                  plot_kws={"alpha": 0.6, "s": 25})
g.fig.suptitle("Pairplot: Price, Quantity, Revenue by Category", y=1.02, fontsize=13, fontweight="bold")
g.savefig(f"{OUT}/07_pairplot_multivariable.png", dpi=150)
plt.close()

# ---------- 3. Boxplot: distributions across categories ----------
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df, x="Category", y="Revenue", hue="Category", palette="Set2", ax=ax, legend=False)
ax.set_title("Revenue Distribution by Category (Boxplot)", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUT}/08_boxplot_revenue_by_category.png", dpi=150)
plt.close()

# ---------- 4. FacetGrid: multi-dimensional data ----------
g = sns.FacetGrid(df, col="Region", col_wrap=3, height=3.2, sharey=True)
g.map_dataframe(sns.histplot, x="Revenue", bins=25, color="#2563eb")
g.set_titles("{col_name}")
g.fig.suptitle("Revenue Distribution by Region (FacetGrid)", y=1.03, fontsize=13, fontweight="bold")
g.savefig(f"{OUT}/09_facetgrid_revenue_by_region.png", dpi=150)
plt.close()

print("Seaborn visualizations saved.")
