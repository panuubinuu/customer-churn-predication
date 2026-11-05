import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Telco Churn Analytics & AI Predictor",
    page_icon="📊",
    layout="wide",
)


# Load artifacts and dataset
@st.cache_resource
def load_assets():
    artifacts = joblib.load("churn_artifacts.pkl")
    dataset = pd.read_csv("telco_clean.csv")
    return artifacts, dataset


artifacts, df = load_assets()
model = artifacts["model"]
feature_cols = artifacts["features"]
cat_cols = artifacts["categorical"]

st.title("Telco Customer Churn Intelligence Dashboard")
st.caption(
    "Powered by LightGBM Ensemble Classification and Interactive Analytics"
)

# Create 4 comprehensive tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Single Customer Risk",
    "Batch Prediction (CSV)",
    "Feature Importance",
    "Dataset Analytics",
])

# ----------------- TAB 1: Single Prediction -----------------
with tab1:
    st.subheader("Predict Individual Customer Churn Probability")
    st.write(
        "Adjust customer demographics, subscription tenure, and service options"
        " below:"
    )

    with st.form("single_prediction_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("##### Demographics")
            gender = st.selectbox("Gender", ["Female", "Male"])
            senior = st.selectbox(
                "Senior Citizen", [0, 1], format_func=lambda x: "Yes" if x else "No"
            )
            partner = st.selectbox("Partner", ["Yes", "No"])
            dependents = st.selectbox("Dependents", ["Yes", "No"])

        with col2:
            st.markdown("##### Services & Usage")
            tenure = st.slider("Tenure (Months)", min_value=0, max_value=72, value=12)
            phone_service = st.selectbox("Phone Service", ["Yes", "No"])
            multiple_lines = st.selectbox(
                "Multiple Lines", ["No", "Yes", "No phone service"]
            )
            internet_service = st.selectbox(
                "Internet Service", ["Fiber optic", "DSL", "No"]
            )
            online_security = st.selectbox(
                "Online Security", ["No", "Yes", "No internet service"]
            )
            tech_support = st.selectbox(
                "Tech Support", ["No", "Yes", "No internet service"]
            )

        with col3:
            st.markdown("##### Account & Billing")
            contract = st.selectbox(
                "Contract Type", ["Month-to-month", "One year", "Two year"]
            )
            paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)",
                ],
            )
            monthly_charges = st.number_input(
                "Monthly Charges ($)", min_value=15.0, max_value=150.0, value=70.0
            )
            total_charges = st.number_input(
                "Total Charges ($)", min_value=0.0, max_value=9000.0, value=840.0
            )

        submit_btn = st.form_submit_button(
            "Calculate Churn Probability", use_container_width=True
        )

    if submit_btn:
        raw_input = {
            "gender": gender,
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "TechSupport": tech_support,
            "Contract": contract,
            "PaperlessBilling": paperless,
            "PaymentMethod": payment_method,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
        }
        input_df = pd.DataFrame([raw_input])
        for col in cat_cols:
            input_df[col] = input_df[col].astype("category")

        prob = model.predict_proba(input_df)[0][1]

        st.divider()
        res_col1, res_col2 = st.columns([1, 2])

        with res_col1:
            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=prob * 100,
                    domain={"x": [0, 1], "y": [0, 1]},
                    title={"text": "Churn Risk (%)"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "red" if prob >= 0.5 else "green"},
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
                )
            )
            fig.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)

        with res_col2:
            st.markdown("#### Diagnostic Summary")
            if prob >= 0.5:
                st.error(
                    f"**High Churn Risk ({prob * 100:.1f}%)**: Customer is at"
                    " imminent risk of cancellation."
                )
                st.markdown("""
                **Recommended Retention Actions:**
                * Offer a transition discount from Month-to-month to an Annual contract.
                * If on Fiber Optic with high charges, bundle free Tech Support or Online Security.
                * Check if payment method can be converted from Electronic check to automatic payment.
                """)
            else:
                st.success(
                    f"**Low Churn Risk ({prob * 100:.1f}%)**: Customer shows high"
                    " loyalty stability."
                )
                st.markdown(
                    "Customer engagement is healthy. Consider cross-selling premium"
                    " add-on features."
                )

# ----------------- TAB 2: Batch Scoring -----------------
with tab2:
    st.subheader("Batch Customer Scoring via CSV")
    st.write("Upload a CSV file containing multiple customer records to score:")

    sample_download = df[feature_cols].head(5).to_csv(index=False)
    st.download_button(
        "Download CSV Template",
        sample_download,
        "sample_batch.csv",
        "text/csv",
    )

    uploaded_file = st.file_uploader(
        "Upload CSV", type=["csv"], key="batch_uploader"
    )
    if uploaded_file:
        batch_df = pd.read_csv(uploaded_file)
        batch_processed = batch_df[feature_cols].copy()
        for col in cat_cols:
            batch_processed[col] = batch_processed[col].astype("category")

        probabilities = model.predict_proba(batch_processed)[:, 1]
        batch_df["Churn_Probability"] = np.round(probabilities * 100, 2)
        batch_df["Predicted_Status"] = np.where(
            probabilities >= 0.5, "Churn Risk", "Retained"
        )

        st.write(f"Scored **{len(batch_df)}** records successfully:")
        st.dataframe(batch_df, use_container_width=True)

        csv_data = batch_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Scored Results CSV",
            csv_data,
            "churn_predictions_scored.csv",
            "text/csv",
            use_container_width=True,
        )

# ----------------- TAB 3: Feature Importance -----------------
with tab3:
    st.subheader("LightGBM Global Feature Importance")
    st.write(
        "This chart displays the number of times each feature was chosen as a"
        " split node in the ensemble trees:"
    )

    importance_df = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": model.feature_importances_,
    }).sort_values(by="Importance", ascending=True)

    fig_imp = px.bar(
        importance_df,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Split-Based Feature Importance",
        color="Importance",
        color_continuous_scale="Blues",
    )
    fig_imp.update_layout(height=500)
    st.plotly_chart(fig_imp, use_container_width=True)

    st.info(
        "**Key Observation:** Continuous billing parameters (`TotalCharges`,"
        " `MonthlyCharges`, `tenure`) and contract duration contribute the"
        " highest split decision frequency."
    )

# ----------------- TAB 4: Dataset Analytics -----------------
with tab4:
    st.subheader("Exploratory Data Analysis (7,043 Records)")

    metric1, metric2, metric3, metric4 = st.columns(4)
    total_cust = len(df)
    churn_rate = df["Churn"].mean() * 100
    avg_tenure = df["tenure"].mean()
    avg_bill = df["MonthlyCharges"].mean()

    metric1.metric("Total Customers", f"{total_cust:,}")
    metric2.metric("Overall Churn Rate", f"{churn_rate:.1f}%")
    metric3.metric("Avg Tenure", f"{avg_tenure:.1f} mos")
    metric4.metric("Avg Monthly Bill", f"${avg_bill:.2f}")

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig_contract = px.histogram(
            df,
            x="Contract",
            color="Churn",
            barmode="group",
            title="Churn Distribution by Contract Type",
            color_discrete_map={0: "#28a745", 1: "#dc3545"},
        )
        st.plotly_chart(fig_contract, use_container_width=True)

    with chart_col2:
        fig_tenure = px.box(
            df,
            x="Churn",
            y="tenure",
            title="Tenure Distribution by Churn Status",
            color="Churn",
            color_discrete_map={0: "#28a745", 1: "#dc3545"},
        )
        st.plotly_chart(fig_tenure, use_container_width=True)
