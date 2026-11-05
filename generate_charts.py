"""
Generate all charts/graphs used in the Churn Predictor project as PNG images.
"""
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Create output directory
os.makedirs("charts", exist_ok=True)

# Load artifacts and dataset
artifacts = joblib.load("churn_artifacts.pkl")
df = pd.read_csv("telco_clean.csv")
model = artifacts["model"]
feature_cols = artifacts["features"]

print("Generating charts...\n")

# ══════════════════════════════════════════════════════════════
# CHART 1: Gauge Meter — Single Customer Churn Risk (Example)
# ══════════════════════════════════════════════════════════════

# High risk example
fig_gauge_high = go.Figure(go.Indicator(
    mode="gauge+number",
    value=78.3,
    domain={"x": [0, 1], "y": [0, 1]},
    title={"text": "Churn Risk (%)", "font": {"size": 20}},
    gauge={
        "axis": {"range": [0, 100], "tickwidth": 2},
        "bar": {"color": "red"},
        "steps": [
            {"range": [0, 30], "color": "#d4edda"},
            {"range": [30, 60], "color": "#fff3cd"},
            {"range": [60, 100], "color": "#f8d7da"},
        ],
        "threshold": {
            "line": {"color": "black", "width": 4},
            "thickness": 0.75,
            "value": 50,
        },
    },
))
fig_gauge_high.update_layout(
    height=400, width=500,
    margin=dict(l=30, r=30, t=60, b=30),
    paper_bgcolor="white",
    title_text="Tab 1: High Churn Risk Example (78.3%)",
    title_x=0.5,
)
fig_gauge_high.write_image("charts/1_gauge_high_risk.png", scale=2)
print("✅ Chart 1: Gauge Meter (High Risk) saved")

# Low risk example
fig_gauge_low = go.Figure(go.Indicator(
    mode="gauge+number",
    value=22.1,
    domain={"x": [0, 1], "y": [0, 1]},
    title={"text": "Churn Risk (%)", "font": {"size": 20}},
    gauge={
        "axis": {"range": [0, 100], "tickwidth": 2},
        "bar": {"color": "green"},
        "steps": [
            {"range": [0, 30], "color": "#d4edda"},
            {"range": [30, 60], "color": "#fff3cd"},
            {"range": [60, 100], "color": "#f8d7da"},
        ],
        "threshold": {
            "line": {"color": "black", "width": 4},
            "thickness": 0.75,
            "value": 50,
        },
    },
))
fig_gauge_low.update_layout(
    height=400, width=500,
    margin=dict(l=30, r=30, t=60, b=30),
    paper_bgcolor="white",
    title_text="Tab 1: Low Churn Risk Example (22.1%)",
    title_x=0.5,
)
fig_gauge_low.write_image("charts/2_gauge_low_risk.png", scale=2)
print("✅ Chart 2: Gauge Meter (Low Risk) saved")


# ══════════════════════════════════════════════════════════════
# CHART 3: Feature Importance (Tab 3)
# ══════════════════════════════════════════════════════════════

importance_df = pd.DataFrame({
    "Feature": feature_cols,
    "Importance": model.feature_importances_,
}).sort_values(by="Importance", ascending=True)

fig_imp = px.bar(
    importance_df,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Tab 3: LightGBM Split-Based Feature Importance",
    color="Importance",
    color_continuous_scale="Blues",
)
fig_imp.update_layout(
    height=550, width=800,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title_x=0.5,
    font=dict(size=13),
)
fig_imp.write_image("charts/3_feature_importance.png", scale=2)
print("✅ Chart 3: Feature Importance saved")


# ══════════════════════════════════════════════════════════════
# CHART 4: Churn Distribution by Contract Type (Tab 4)
# ══════════════════════════════════════════════════════════════

df["Churn_Label"] = df["Churn"].map({0: "Retained", 1: "Churned"})

fig_contract = px.histogram(
    df,
    x="Contract",
    color="Churn_Label",
    barmode="group",
    title="Tab 4: Churn Distribution by Contract Type",
    color_discrete_map={"Retained": "#28a745", "Churned": "#dc3545"},
    category_orders={"Contract": ["Month-to-month", "One year", "Two year"]},
)
fig_contract.update_layout(
    height=500, width=750,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title_x=0.5,
    font=dict(size=13),
    legend_title_text="Status",
    xaxis_title="Contract Type",
    yaxis_title="Number of Customers",
)
fig_contract.write_image("charts/4_churn_by_contract.png", scale=2)
print("✅ Chart 4: Churn by Contract Type saved")


# ══════════════════════════════════════════════════════════════
# CHART 5: Tenure Distribution by Churn Status — Box Plot (Tab 4)
# ══════════════════════════════════════════════════════════════

fig_tenure = px.box(
    df,
    x="Churn_Label",
    y="tenure",
    title="Tab 4: Tenure Distribution by Churn Status",
    color="Churn_Label",
    color_discrete_map={"Retained": "#28a745", "Churned": "#dc3545"},
)
fig_tenure.update_layout(
    height=500, width=650,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title_x=0.5,
    font=dict(size=13),
    legend_title_text="Status",
    xaxis_title="Churn Status",
    yaxis_title="Tenure (Months)",
)
fig_tenure.write_image("charts/5_tenure_boxplot.png", scale=2)
print("✅ Chart 5: Tenure Box Plot saved")


# ══════════════════════════════════════════════════════════════
# CHART 6: Overall Churn Rate — Pie Chart (Extra for Report)
# ══════════════════════════════════════════════════════════════

churn_counts = df["Churn_Label"].value_counts()
fig_pie = px.pie(
    values=churn_counts.values,
    names=churn_counts.index,
    title="Overall Churn Rate Distribution",
    color=churn_counts.index,
    color_discrete_map={"Retained": "#28a745", "Churned": "#dc3545"},
    hole=0.4,
)
fig_pie.update_traces(textposition="inside", textinfo="percent+label+value")
fig_pie.update_layout(
    height=480, width=600,
    paper_bgcolor="white",
    title_x=0.5,
    font=dict(size=13),
)
fig_pie.write_image("charts/6_churn_pie_chart.png", scale=2)
print("✅ Chart 6: Churn Pie Chart saved")


# ══════════════════════════════════════════════════════════════
# CHART 7: Monthly Charges Distribution by Churn (Extra)
# ══════════════════════════════════════════════════════════════

fig_charges = px.histogram(
    df,
    x="MonthlyCharges",
    color="Churn_Label",
    barmode="overlay",
    nbins=40,
    title="Monthly Charges Distribution by Churn Status",
    color_discrete_map={"Retained": "#28a745", "Churned": "#dc3545"},
    opacity=0.7,
)
fig_charges.update_layout(
    height=450, width=750,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title_x=0.5,
    font=dict(size=13),
    xaxis_title="Monthly Charges ($)",
    yaxis_title="Count",
    legend_title_text="Status",
)
fig_charges.write_image("charts/7_monthly_charges_distribution.png", scale=2)
print("✅ Chart 7: Monthly Charges Distribution saved")


# ══════════════════════════════════════════════════════════════
# CHART 8: Churn by Internet Service Type (Extra)
# ══════════════════════════════════════════════════════════════

fig_internet = px.histogram(
    df,
    x="InternetService",
    color="Churn_Label",
    barmode="group",
    title="Churn Distribution by Internet Service Type",
    color_discrete_map={"Retained": "#28a745", "Churned": "#dc3545"},
)
fig_internet.update_layout(
    height=480, width=700,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title_x=0.5,
    font=dict(size=13),
    xaxis_title="Internet Service",
    yaxis_title="Number of Customers",
    legend_title_text="Status",
)
fig_internet.write_image("charts/8_churn_by_internet_service.png", scale=2)
print("✅ Chart 8: Churn by Internet Service saved")


# ══════════════════════════════════════════════════════════════
# CHART 9: Churn by Payment Method (Extra)
# ══════════════════════════════════════════════════════════════

fig_payment = px.histogram(
    df,
    x="PaymentMethod",
    color="Churn_Label",
    barmode="group",
    title="Churn Distribution by Payment Method",
    color_discrete_map={"Retained": "#28a745", "Churned": "#dc3545"},
)
fig_payment.update_layout(
    height=480, width=800,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title_x=0.5,
    font=dict(size=13),
    xaxis_title="Payment Method",
    yaxis_title="Number of Customers",
    legend_title_text="Status",
)
fig_payment.write_image("charts/9_churn_by_payment_method.png", scale=2)
print("✅ Chart 9: Churn by Payment Method saved")


# ══════════════════════════════════════════════════════════════
# CHART 10: Correlation — Tenure vs Monthly Charges (Scatter)
# ══════════════════════════════════════════════════════════════

sample_df = df.sample(n=1500, random_state=42)  # sample for readability
fig_scatter = px.scatter(
    sample_df,
    x="tenure",
    y="MonthlyCharges",
    color="Churn_Label",
    title="Tenure vs Monthly Charges (Sample: 1,500 Customers)",
    color_discrete_map={"Retained": "#28a745", "Churned": "#dc3545"},
    opacity=0.6,
)
fig_scatter.update_layout(
    height=500, width=750,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title_x=0.5,
    font=dict(size=13),
    xaxis_title="Tenure (Months)",
    yaxis_title="Monthly Charges ($)",
    legend_title_text="Status",
)
fig_scatter.write_image("charts/10_tenure_vs_charges_scatter.png", scale=2)
print("✅ Chart 10: Tenure vs Charges Scatter Plot saved")


# ══════════════════════════════════════════════════════════════
# CHART 11: ROC-AUC Visualization
# ══════════════════════════════════════════════════════════════

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc

X = df[feature_cols].copy()
y = df["Churn"]
cat_cols = artifacts["categorical"]
for col in cat_cols:
    X[col] = X[col].astype("category")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
y_pred_proba = model.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

fig_roc = go.Figure()
fig_roc.add_trace(go.Scatter(
    x=fpr, y=tpr,
    mode="lines",
    name=f"LightGBM (AUC = {roc_auc:.4f})",
    line=dict(color="royalblue", width=3),
))
fig_roc.add_trace(go.Scatter(
    x=[0, 1], y=[0, 1],
    mode="lines",
    name="Random Baseline (AUC = 0.5)",
    line=dict(color="gray", width=2, dash="dash"),
))
fig_roc.update_layout(
    title="ROC Curve — LightGBM Churn Model",
    title_x=0.5,
    xaxis_title="False Positive Rate (FPR)",
    yaxis_title="True Positive Rate (TPR)",
    height=500, width=650,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(size=13),
    legend=dict(x=0.55, y=0.1),
)
fig_roc.write_image("charts/11_roc_curve.png", scale=2)
print("✅ Chart 11: ROC Curve saved")


# ══════════════════════════════════════════════════════════════
# CHART 12: Confusion Matrix Heatmap
# ══════════════════════════════════════════════════════════════

from sklearn.metrics import confusion_matrix

y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

fig_cm = px.imshow(
    cm,
    text_auto=True,
    labels=dict(x="Predicted", y="Actual", color="Count"),
    x=["Retained (0)", "Churned (1)"],
    y=["Retained (0)", "Churned (1)"],
    color_continuous_scale="Blues",
    title="Confusion Matrix — LightGBM Model",
)
fig_cm.update_layout(
    height=480, width=550,
    paper_bgcolor="white",
    title_x=0.5,
    font=dict(size=14),
)
fig_cm.write_image("charts/12_confusion_matrix.png", scale=2)
print("✅ Chart 12: Confusion Matrix saved")


# ══════════════════════════════════════════════════════════════
print(f"\n{'='*50}")
print(f"All 12 charts saved in: {os.path.abspath('charts')}")
print(f"{'='*50}")
