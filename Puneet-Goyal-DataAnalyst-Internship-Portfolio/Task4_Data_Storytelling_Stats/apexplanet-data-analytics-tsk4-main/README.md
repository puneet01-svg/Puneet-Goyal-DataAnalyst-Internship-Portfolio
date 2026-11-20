# Task 4: Advanced Analytics & Statistical Modeling

**Timeline:** 11 Days (Day 28–38) &nbsp;|&nbsp; **Objective:** Apply statistical analysis, time series forecasting, customer segmentation, and basic predictive modeling to retail sales data.

## 📁 Repository Contents

| File | Description |
|---|---|
| `Task4_Advanced_Analytics_Statistical_Modeling.ipynb` | Main deliverable — full Jupyter notebook, already executed, with all charts and results embedded. Open directly on GitHub or in Jupyter/VS Code. |
| `task4_analysis_script.py` | The same analysis as a plain `.py` script (jupytext-style `# %%` cell markers), useful for running end-to-end from the command line or diffing in code review. |
| `sales_data.csv` | Source dataset (not included here if not re-uploaded — see **Dataset** below). |

## 📊 Dataset

`sales_data.csv` — 3,000 retail orders spanning **2024-01-01 to 2025-12-31**:

| Column | Description |
|---|---|
| `OrderID` | Unique order identifier |
| `OrderDate` | Date of the order |
| `CustomerID` | Unique customer identifier (597 unique customers) |
| `Region` | North / South / East / West / Central |
| `Category` | Apparel / Electronics / Furniture / Groceries / Sports |
| `Product` | Specific product name (25 unique products) |
| `UnitPrice` | Price per unit ($) |
| `Quantity` | Units purchased (1–5) |
| `Revenue` | `UnitPrice × Quantity` |

No missing values; data required no cleaning beyond parsing `OrderDate` as a datetime.

## 🧪 Methodology & Notebook Structure

1. **Data Overview** — shape, dtypes, missing values, summary stats.
2. **Descriptive Statistics** — mean, median, mode, variance, std dev, skewness, kurtosis for `UnitPrice`, `Quantity`, `Revenue`.
3. **Inferential Statistics**
   - 95% confidence interval for mean order revenue
   - Independent-samples t-test (East vs. West revenue)
   - Chi-square test of independence (Category × Region)
   - One-way ANOVA (Revenue across all 5 regions)
   - Pearson correlation matrix + correlation-vs-causation discussion
4. **Time Series Analysis**
   - Daily / weekly / monthly resampling
   - Classical additive decomposition (trend / seasonal / residual)
   - Stationarity check (Augmented Dickey-Fuller)
   - Smoothing (7- and 30-day moving average, exponential smoothing)
   - Forecasting (AR-on-differenced-series, ARIMA-style) evaluated with MAE / RMSE / MAPE on a held-out test period
5. **Customer Segmentation (K-Means)**
   - RFM-style feature engineering (Recency, Frequency, Monetary, AvgOrderValue, CategoryDiversity)
   - Feature scaling with `StandardScaler`
   - Optimal-k selection via elbow method + silhouette score
   - PCA 2D visualization of clusters
   - Cluster profiling and segment-based recommendations
6. **Predictive Modeling**
   - Target: `Churned` (Recency > 90 days proxy) — Logistic Regression & Decision Tree classifiers, evaluated with Accuracy / Precision / Recall / F1 / ROC-AUC
   - Target: customer lifetime `Monetary` value — Linear Regression, evaluated with R² / MAE / RMSE
   - Feature importance analysis and documented model limitations
7. **Summary & Business Recommendations** — findings-to-action table tying every analysis back to a concrete business decision.

## ⚠️ Environment Note: `statsmodels` Unavailable

The analysis was built in a sandbox with **no internet access**, so `statsmodels` could not be
installed. Every function it would normally provide was **re-implemented from first principles**
using `numpy`/`scipy` so the notebook still runs end-to-end with zero missing steps:

- `adfuller()` → manual Augmented Dickey-Fuller regression via OLS (`numpy.linalg.lstsq`)
- `seasonal_decompose()` → manual additive decomposition (centered moving-average trend + monthly seasonal index)
- `ARIMA`/`SARIMA` → manual AR(p) model fit by OLS on a differenced series (ARIMA(p,1,0)-style), integrated back to level for forecasting

These substitutions are called out inline in the notebook wherever they appear. If you have
`statsmodels` available in your own environment, swap in `adfuller()`, `seasonal_decompose()`,
and `ARIMA`/`SARIMAX` for production-grade equivalents — the manual versions here are for
environment-portability, not because they're preferred.

## ▶️ How to Run

```bash
pip install pandas numpy scipy scikit-learn matplotlib seaborn
# statsmodels is optional — the notebook works without it (see note above);
# install it too if you want to swap in the native adfuller/seasonal_decompose/ARIMA calls.

jupyter notebook Task4_Advanced_Analytics_Statistical_Modeling.ipynb
# — or —
python task4_analysis_script.py
```

Place `sales_data.csv` in the same directory (or update the path at the top of the notebook/script)
before running.

## 🔑 Key Findings

- **Revenue is right-skewed** (mean $453.88 vs. median $210.92) — a small share of high-ticket Electronics/Furniture orders pulls the average up; report the median alongside the mean.
- **East vs. West revenue:** no statistically significant difference (p = 0.469).
- **Category mix vs. Region:** independent — no significant association (p = 0.459).
- **Revenue across all 5 regions (ANOVA):** at least one region differs significantly (p = 0.028) — worth a regional drill-down.
- **Time series:** monthly revenue shows a clear seasonal pattern (build peaks around Q4); the series is non-stationary in levels (differencing needed for forecasting).
- **Customer segmentation:** 4 actionable segments identified via K-Means (e.g., high-value/recent "champions" vs. low-value dormant customers).
- **Churn prediction:** Decision Tree outperforms Logistic Regression (Accuracy 0.62 vs. 0.55); order **Frequency** is by far the strongest churn signal.
- **Revenue prediction:** Linear Regression explains ~82.5% of variance in customer lifetime revenue (R² = 0.825), driven mainly by purchase Frequency.

## 📝 Model Limitations (documented in notebook §6.4)

- 597 customers is a modest sample for production ML — treat results as directional.
- `Churned` is a heuristic proxy (90-day recency cutoff), not a true cancellation event.
- Dataset transactions appear close to randomly generated, which caps the achievable forecast/predictive accuracy (flagged wherever relevant, e.g. the ~41% forecast MAPE).
- Linear/logistic models assume linear relationships; Random Forest / Gradient Boosting would likely perform better in production.
- `Product`/`Region` categorical fields weren't one-hot encoded into the predictive models — a straightforward next step.
