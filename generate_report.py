"""
Generate a professional Word document report for the
Telco Customer Churn Prediction project.
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
import os

doc = Document()

# ─── Page margins ───
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# ─── Helper: set paragraph font ───
def set_run(run, size=12, bold=False, color=None, font_name="Calibri"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = font_name
    if color:
        run.font.color.rgb = RGBColor(*color)

def add_heading_styled(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = "Calibri"
    return h

def add_para(text, bold=False, size=12, alignment=None, space_after=6):
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_run(run, size=size, bold=bold)
    if alignment:
        p.alignment = alignment
    p.paragraph_format.space_after = Pt(space_after)
    return p

def add_bullet(text, bold_prefix="", size=11):
    p = doc.add_paragraph(style="List Bullet")
    if bold_prefix:
        run_b = p.add_run(bold_prefix)
        set_run(run_b, size=size, bold=True)
        run_t = p.add_run(text)
        set_run(run_t, size=size)
    else:
        run_t = p.add_run(text)
        set_run(run_t, size=size)
    return p

def add_table(headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Light Grid Accent 1"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.bold = True
                run.font.size = Pt(11)
                run.font.name = "Calibri"
    # Data rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(11)
                    run.font.name = "Calibri"
    doc.add_paragraph()  # spacer
    return table


# ══════════════════════════════════════════════════════════════
#                       TITLE PAGE
# ══════════════════════════════════════════════════════════════

doc.add_paragraph("\n\n\n")

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run("CUSTOMER CHURN PREDICTION\n& ANALYTICS DASHBOARD")
set_run(run, size=28, bold=True, color=(0, 51, 102))

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run("A Mini Project Report")
set_run(run, size=18, color=(80, 80, 80))

doc.add_paragraph()

details = doc.add_paragraph()
details.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = details.add_run(
    "Using Machine Learning (LightGBM) and Streamlit Dashboard\n"
    "on IBM Telco Customer Churn Dataset (7,043 Records)"
)
set_run(run, size=13, color=(100, 100, 100))

doc.add_paragraph("\n\n")

# ── Student details placeholder ──
info_table_data = [
    ["Submitted By:", "[Your Name]"],
    ["Roll Number:", "[Your Roll No.]"],
    ["Class / Branch:", "[Your Class & Branch]"],
    ["Guide Name:", "[Your Guide/Teacher Name]"],
    ["College Name:", "[Your College Name]"],
    ["Academic Year:", "2026-2027"],
]
info_table = doc.add_table(rows=len(info_table_data), cols=2)
info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, (label, value) in enumerate(info_table_data):
    info_table.rows[i].cells[0].text = label
    info_table.rows[i].cells[1].text = value
    for cell in info_table.rows[i].cells:
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.size = Pt(12)
                run.font.name = "Calibri"
        if cell == info_table.rows[i].cells[0]:
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.bold = True

doc.add_page_break()


# ══════════════════════════════════════════════════════════════
#                     TABLE OF CONTENTS
# ══════════════════════════════════════════════════════════════

add_heading_styled("Table of Contents", level=1)

toc_items = [
    "1. Abstract",
    "2. Introduction",
    "3. Problem Statement",
    "4. Objectives",
    "5. Literature Review",
    "6. System Requirements",
    "7. Dataset Description",
    "8. Methodology",
    "9. System Architecture",
    "10. Implementation",
    "    10.1 Data Preprocessing (train.py)",
    "    10.2 Model Training (LightGBM)",
    "    10.3 Dashboard Application (app.py)",
    "11. Dashboard Features (4 Tabs)",
    "    11.1 Single Customer Risk Prediction",
    "    11.2 Batch CSV Scoring",
    "    11.3 Feature Importance (XAI)",
    "    11.4 Dataset Analytics (EDA)",
    "12. Results and Evaluation",
    "13. Screenshots",
    "14. Technologies Used",
    "15. Future Scope",
    "16. Conclusion",
    "17. References",
]

for item in toc_items:
    p = doc.add_paragraph()
    run = p.add_run(item)
    set_run(run, size=12)
    p.paragraph_format.space_after = Pt(2)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════
#                      1. ABSTRACT
# ══════════════════════════════════════════════════════════════

add_heading_styled("1. Abstract", level=1)

add_para(
    "Customer churn is one of the most critical challenges faced by the telecommunications industry. "
    "Churn refers to the phenomenon where customers discontinue their subscription to a service. "
    "Acquiring new customers is estimated to cost five to seven times more than retaining existing ones, "
    "making churn prediction a high-priority business problem."
)
add_para(
    "This project presents an end-to-end Customer Churn Prediction system built using Python, "
    "the LightGBM (Light Gradient Boosting Machine) algorithm, and an interactive Streamlit web dashboard. "
    "The system is trained on the IBM Telco Customer Churn Dataset containing 7,043 customer records "
    "with 21 attributes covering demographics, account information, and subscribed services."
)
add_para(
    "The trained model achieves an ROC-AUC score of 0.8406 (84.06%), demonstrating strong predictive "
    "capability. The Streamlit dashboard provides four interactive tabs: Single Customer Risk Prediction "
    "with a real-time gauge meter, Batch CSV Scoring for bulk predictions, Feature Importance visualization "
    "for Explainable AI (XAI), and comprehensive Dataset Analytics with interactive Plotly charts."
)
add_para(
    "Keywords: Customer Churn, Machine Learning, LightGBM, Gradient Boosting, Streamlit, "
    "Explainable AI, Telco Dataset, Predictive Analytics.",
    bold=True, size=11
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════
#                    2. INTRODUCTION
# ══════════════════════════════════════════════════════════════

add_heading_styled("2. Introduction", level=1)

add_para(
    "The telecommunications industry is one of the most competitive sectors globally, "
    "with customers having multiple service providers to choose from. In such a saturated market, "
    "customer retention becomes paramount for business sustainability and revenue growth."
)
add_para(
    "Customer churn, also known as customer attrition, occurs when a customer stops doing business "
    "with a company. In the telecom sector, this translates to a customer canceling their phone, "
    "internet, or bundled service subscription. Industry reports suggest that the average annual "
    "churn rate in telecom ranges from 15% to 25%."
)
add_para(
    "Machine Learning provides a data-driven approach to predict which customers are most likely "
    "to churn. By analyzing historical customer data — including demographics, service subscriptions, "
    "billing patterns, and account tenure — predictive models can identify at-risk customers before "
    "they leave. This enables companies to proactively deploy targeted retention strategies such as "
    "personalized discounts, service upgrades, or loyalty programs."
)
add_para(
    "This project implements a complete churn prediction pipeline: from data acquisition and "
    "preprocessing, through model training and evaluation, to deployment as an interactive web "
    "dashboard accessible to non-technical business users."
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════
#                  3. PROBLEM STATEMENT
# ══════════════════════════════════════════════════════════════

add_heading_styled("3. Problem Statement", level=1)

add_para(
    "A telecommunications company is experiencing a significant customer churn rate of approximately "
    "26.5%. The company needs a system that can:"
)
add_bullet("Predict whether an individual customer is likely to churn based on their profile and usage patterns.", bold_prefix="")
add_bullet("Score large batches of customers simultaneously to identify at-risk segments.", bold_prefix="")
add_bullet("Provide transparency into which factors drive churn (Explainable AI).", bold_prefix="")
add_bullet("Offer an intuitive, non-technical dashboard for business stakeholders to interact with predictions.", bold_prefix="")

add_para(
    "The goal is to build a machine learning model with high predictive accuracy and deploy it "
    "through a user-friendly web interface that empowers the company's retention team to take "
    "timely, data-driven actions."
)


# ══════════════════════════════════════════════════════════════
#                     4. OBJECTIVES
# ══════════════════════════════════════════════════════════════

add_heading_styled("4. Objectives", level=1)

objectives = [
    "To collect and preprocess the IBM Telco Customer Churn Dataset (7,043 records).",
    "To perform Exploratory Data Analysis (EDA) to understand churn patterns and feature distributions.",
    "To train a LightGBM Classifier for binary churn prediction with high accuracy.",
    "To evaluate model performance using ROC-AUC, precision, recall, and F1-score metrics.",
    "To build an interactive Streamlit web dashboard with four functional tabs.",
    "To implement Explainable AI (XAI) through feature importance visualization.",
    "To enable batch CSV scoring for enterprise-scale churn prediction.",
    "To provide actionable retention recommendations based on prediction outcomes.",
]
for obj in objectives:
    add_bullet(obj)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════
#                  5. LITERATURE REVIEW
# ══════════════════════════════════════════════════════════════

add_heading_styled("5. Literature Review", level=1)

add_para("5.1 Customer Churn in Telecommunications", bold=True, size=13)
add_para(
    "Numerous studies have investigated customer churn prediction in the telecom industry. "
    "Huang et al. (2012) demonstrated that ensemble methods such as Random Forest and Gradient "
    "Boosting outperform traditional logistic regression in churn prediction tasks. The key factors "
    "identified across studies include contract type, tenure, monthly charges, and customer service "
    "interactions."
)

add_para("5.2 Gradient Boosting and LightGBM", bold=True, size=13)
add_para(
    "LightGBM, developed by Microsoft Research (Ke et al., 2017), is a gradient boosting framework "
    "that uses tree-based learning algorithms. It is designed for efficiency and scalability, offering "
    "faster training speeds and lower memory usage compared to traditional GBDT implementations. "
    "LightGBM introduces two novel techniques: Gradient-based One-Side Sampling (GOSS) and Exclusive "
    "Feature Bundling (EFB), which significantly reduce computation time while maintaining accuracy."
)

add_para("5.3 Explainable AI (XAI)", bold=True, size=13)
add_para(
    "With the increasing adoption of machine learning in business-critical decisions, the need for "
    "model interpretability has grown. Feature importance analysis, as provided by tree-based models, "
    "offers a straightforward way to understand which input variables most influence predictions. "
    "This transparency is essential for building trust with business stakeholders and ensuring "
    "regulatory compliance."
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════
#                 6. SYSTEM REQUIREMENTS
# ══════════════════════════════════════════════════════════════

add_heading_styled("6. System Requirements", level=1)

add_para("6.1 Hardware Requirements", bold=True, size=13)
add_table(
    ["Component", "Minimum Requirement"],
    [
        ["Processor", "Intel Core i3 / AMD Ryzen 3 or above"],
        ["RAM", "4 GB (8 GB recommended)"],
        ["Storage", "500 MB free disk space"],
        ["Display", "1366 x 768 resolution or higher"],
        ["Internet", "Required for dataset download"],
    ],
)

add_para("6.2 Software Requirements", bold=True, size=13)
add_table(
    ["Software", "Version", "Purpose"],
    [
        ["Python", "3.10+", "Programming language"],
        ["Streamlit", "1.30+", "Web dashboard framework"],
        ["Pandas", "2.0+", "Data manipulation"],
        ["NumPy", "1.24+", "Numerical operations"],
        ["Scikit-learn", "1.3+", "Train/test split, metrics"],
        ["LightGBM", "4.0+", "ML model (Gradient Boosting)"],
        ["Plotly", "5.18+", "Interactive visualizations"],
        ["Joblib", "1.3+", "Model serialization"],
        ["Web Browser", "Chrome / Edge / Firefox", "Dashboard viewing"],
    ],
)


# ══════════════════════════════════════════════════════════════
#                  7. DATASET DESCRIPTION
# ══════════════════════════════════════════════════════════════

add_heading_styled("7. Dataset Description", level=1)

add_para(
    "The project uses the IBM Telco Customer Churn Dataset, a widely-used benchmark dataset for "
    "churn prediction research. The dataset is publicly available on IBM's GitHub repository."
)

add_table(
    ["Property", "Details"],
    [
        ["Source", "IBM Watson Analytics Sample Dataset"],
        ["Total Records", "7,043 customers"],
        ["Total Features", "21 columns"],
        ["Target Variable", "Churn (Yes/No → 1/0)"],
        ["Churn Rate", "~26.5% (1,869 churned out of 7,043)"],
        ["Format", "CSV (Comma-Separated Values)"],
    ],
)

add_para("7.1 Feature Description", bold=True, size=13)
add_table(
    ["Feature", "Type", "Description"],
    [
        ["customerID", "String", "Unique customer identifier"],
        ["gender", "Categorical", "Male / Female"],
        ["SeniorCitizen", "Binary", "1 = Senior, 0 = Not Senior"],
        ["Partner", "Categorical", "Yes / No"],
        ["Dependents", "Categorical", "Yes / No"],
        ["tenure", "Numeric", "Months with the company (0-72)"],
        ["PhoneService", "Categorical", "Yes / No"],
        ["MultipleLines", "Categorical", "Yes / No / No phone service"],
        ["InternetService", "Categorical", "DSL / Fiber optic / No"],
        ["OnlineSecurity", "Categorical", "Yes / No / No internet service"],
        ["TechSupport", "Categorical", "Yes / No / No internet service"],
        ["Contract", "Categorical", "Month-to-month / One year / Two year"],
        ["PaperlessBilling", "Categorical", "Yes / No"],
        ["PaymentMethod", "Categorical", "Electronic check / Mailed check / Bank transfer / Credit card"],
        ["MonthlyCharges", "Numeric", "Monthly billing amount ($18.25 - $118.75)"],
        ["TotalCharges", "Numeric", "Total amount billed ($0 - $8,684.80)"],
        ["Churn", "Binary (Target)", "Yes = Churned, No = Retained"],
    ],
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════
#                    8. METHODOLOGY
# ══════════════════════════════════════════════════════════════

add_heading_styled("8. Methodology", level=1)

add_para(
    "The project follows the standard Machine Learning pipeline methodology:"
)

steps = [
    ("Data Collection: ", "Download the IBM Telco Churn dataset (7,043 records) from GitHub."),
    ("Data Cleaning: ", "Handle missing values in TotalCharges column by replacing blanks with 0. "
     "Convert target variable Churn from Yes/No to 1/0."),
    ("Feature Selection: ", "Select 15 key business features covering demographics, services, and billing."),
    ("Data Encoding: ", "Convert categorical string columns to LightGBM-compatible category dtype."),
    ("Data Splitting: ", "80% training set and 20% test set using stratified sampling to maintain "
     "class balance."),
    ("Model Training: ", "Train LightGBM Classifier with 150 estimators, learning rate 0.05, "
     "and max depth 5."),
    ("Model Evaluation: ", "Evaluate using ROC-AUC score on the held-out test set."),
    ("Model Serialization: ", "Save trained model and metadata using Joblib for deployment."),
    ("Dashboard Development: ", "Build Streamlit app with 4 interactive tabs for prediction and analytics."),
    ("Deployment: ", "Launch locally via streamlit run app.py on http://localhost:8501."),
]
for prefix, text in steps:
    add_bullet(text, bold_prefix=prefix)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════
#                 9. SYSTEM ARCHITECTURE
# ══════════════════════════════════════════════════════════════

add_heading_styled("9. System Architecture", level=1)

add_para(
    "The system follows a two-phase architecture: an offline Training Phase and an online "
    "Prediction/Dashboard Phase."
)

add_para("9.1 Training Phase (train.py)", bold=True, size=13)
add_para(
    "IBM Dataset (CSV) → Data Cleaning → Feature Selection → "
    "Train/Test Split (80/20) → LightGBM Training (150 trees) → "
    "Evaluation (ROC-AUC: 0.8406) → Save Model (churn_artifacts.pkl) + Clean Data (telco_clean.csv)"
)

add_para("9.2 Dashboard Phase (app.py)", bold=True, size=13)
add_para(
    "User opens http://localhost:8501 → Streamlit loads saved model and dataset → "
    "User interacts with 4 tabs → Model generates real-time predictions → "
    "Results displayed via Plotly charts, gauges, tables, and downloadable CSVs."
)

add_para("9.3 Project File Structure", bold=True, size=13)
add_table(
    ["File", "Purpose"],
    [
        ["train.py", "Data download, cleaning, model training, and artifact export"],
        ["app.py", "Streamlit dashboard with 4 interactive tabs"],
        ["churn_artifacts.pkl", "Serialized LightGBM model + feature metadata"],
        ["telco_clean.csv", "Cleaned dataset for dashboard analytics"],
    ],
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════
#                   10. IMPLEMENTATION
# ══════════════════════════════════════════════════════════════

add_heading_styled("10. Implementation", level=1)

# ── 10.1 Data Preprocessing ──
add_para("10.1 Data Preprocessing (train.py)", bold=True, size=14)

add_para(
    "The preprocessing stage handles data quality issues in the raw dataset:"
)
add_bullet("TotalCharges column contains blank spaces for new customers with zero tenure. "
           "These are converted to numeric type with missing values filled as 0.",
           bold_prefix="Missing Values: ")
add_bullet("The Churn column is mapped from 'Yes'/'No' strings to binary 1/0 integers.",
           bold_prefix="Target Encoding: ")
add_bullet("15 features are selected based on business relevance, covering customer demographics, "
           "service subscriptions, and billing information.",
           bold_prefix="Feature Selection: ")
add_bullet("String categorical columns (gender, Partner, Contract, etc.) are converted to "
           "pandas categorical dtype for native LightGBM handling.",
           bold_prefix="Categorical Encoding: ")

add_para("\nCode snippet — Data cleaning:", bold=True, size=11)
code = (
    'df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")\n'
    'df["TotalCharges"] = df["TotalCharges"].fillna(0)\n'
    'df["Churn"] = df["Churn"].apply(lambda x: 1 if x == "Yes" else 0)'
)
p = doc.add_paragraph()
run = p.add_run(code)
run.font.name = "Consolas"
run.font.size = Pt(10)
p.paragraph_format.space_after = Pt(8)

# ── 10.2 Model Training ──
add_para("10.2 Model Training (LightGBM)", bold=True, size=14)

add_para(
    "LightGBM (Light Gradient Boosting Machine) is an advanced ensemble learning algorithm "
    "developed by Microsoft. It builds multiple decision trees sequentially, where each new tree "
    "corrects the errors made by the previous trees. This technique is called Gradient Boosting."
)

add_para("Model Hyperparameters:", bold=True, size=12)
add_table(
    ["Parameter", "Value", "Explanation"],
    [
        ["n_estimators", "150", "Number of boosting rounds (decision trees)"],
        ["learning_rate", "0.05", "Step size for gradient descent (controls overfitting)"],
        ["max_depth", "5", "Maximum depth of each tree (controls complexity)"],
        ["random_state", "42", "Seed for reproducibility"],
    ],
)

add_para("\nCode snippet — Model training:", bold=True, size=11)
code2 = (
    'lgb_model = LGBMClassifier(\n'
    '    n_estimators=150, learning_rate=0.05,\n'
    '    max_depth=5, random_state=42\n'
    ')\n'
    'lgb_model.fit(X_train, y_train)'
)
p = doc.add_paragraph()
run = p.add_run(code2)
run.font.name = "Consolas"
run.font.size = Pt(10)

# ── 10.3 Dashboard ──
add_para("\n10.3 Dashboard Application (app.py)", bold=True, size=14)

add_para(
    "The dashboard is built using Streamlit, an open-source Python framework for creating "
    "data-driven web applications. It loads the pre-trained model and cleaned dataset at startup "
    "using Streamlit's caching mechanism (@st.cache_resource) for optimal performance."
)
add_para(
    "The interface is organized into 4 tabs, each serving a distinct business function. "
    "Plotly is used for all visualizations, providing interactive hover, zoom, and export capabilities."
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════
#              11. DASHBOARD FEATURES (4 TABS)
# ══════════════════════════════════════════════════════════════

add_heading_styled("11. Dashboard Features (4 Tabs)", level=1)

# Tab 1
add_para("11.1 Tab 1: Single Customer Risk Prediction", bold=True, size=14)
add_para("Purpose: ", bold=True, size=12)
add_para(
    "Predict the churn probability for an individual customer based on their profile."
)
add_para("How it works:", bold=True, size=12)
add_bullet("User fills a form with 15 customer attributes (gender, tenure, contract, charges, etc.).")
add_bullet("On submission, the data is passed to the LightGBM model for prediction.")
add_bullet("The model returns a probability between 0% and 100%.")
add_bullet("A Plotly Gauge Meter visualizes the risk level with color coding:")
add_bullet("  Green (0-30%) = Low Risk, Yellow (30-60%) = Medium Risk, Red (60-100%) = High Risk.")
add_bullet("If probability ≥ 50%, the system displays a High Risk warning with specific retention recommendations:")
add_bullet("  — Offer contract upgrade discount (Month-to-month → Annual).")
add_bullet("  — Bundle free Tech Support or Online Security for Fiber Optic users.")
add_bullet("  — Convert payment from Electronic check to automatic payment.")

# Tab 2
add_para("\n11.2 Tab 2: Batch CSV Scoring", bold=True, size=14)
add_para("Purpose: ", bold=True, size=12)
add_para(
    "Score multiple customers simultaneously by uploading a CSV file."
)
add_para("How it works:", bold=True, size=12)
add_bullet("User downloads a CSV template with the correct column format (5 sample records).")
add_bullet("User populates the template with their customer data and uploads it.")
add_bullet("The model scores every row, adding two new columns: Churn_Probability (%) and Predicted_Status (Churn Risk / Retained).")
add_bullet("Results are displayed in an interactive data table and can be downloaded as a scored CSV file.")

# Tab 3
add_para("\n11.3 Tab 3: Feature Importance (Explainable AI)", bold=True, size=14)
add_para("Purpose: ", bold=True, size=12)
add_para(
    "Visualize which features the model considers most important for making predictions."
)
add_para("How it works:", bold=True, size=12)
add_bullet("Extracts the split-based feature importance from the trained LightGBM model.")
add_bullet("Displays a horizontal bar chart showing each feature's importance score.")
add_bullet("Key insight: TotalCharges, MonthlyCharges, and tenure are the top 3 most important features.")
add_bullet("Contract type also ranks highly — Month-to-month customers churn the most.")
add_bullet("Demographic features like gender have minimal impact on churn prediction.")

add_para(
    "This tab implements Explainable AI (XAI) — making the model's decision-making process "
    "transparent and understandable to business users, which is essential for trust and regulatory compliance."
)

# Tab 4
add_para("\n11.4 Tab 4: Dataset Analytics (EDA)", bold=True, size=14)
add_para("Purpose: ", bold=True, size=12)
add_para(
    "Provide a comprehensive Exploratory Data Analysis of the entire 7,043-record dataset."
)
add_para("Components:", bold=True, size=12)
add_bullet("4 KPI Metric Cards: Total Customers (7,043), Churn Rate (~26.5%), Avg Tenure (~32 months), Avg Monthly Bill (~$64.76).",
           bold_prefix="Metrics: ")
add_bullet("Grouped bar chart showing churn distribution across Month-to-month, One year, and Two year contracts. "
           "Month-to-month contracts show the highest churn rate.",
           bold_prefix="Chart 1 — Churn by Contract Type: ")
add_bullet("Box plot comparing tenure distribution between churned and retained customers. "
           "Churned customers typically have shorter tenures (1-15 months).",
           bold_prefix="Chart 2 — Tenure by Churn Status: ")

doc.add_page_break()


# ══════════════════════════════════════════════════════════════
#              12. RESULTS AND EVALUATION
# ══════════════════════════════════════════════════════════════

add_heading_styled("12. Results and Evaluation", level=1)

add_para("12.1 Model Performance", bold=True, size=13)

add_table(
    ["Metric", "Score", "Interpretation"],
    [
        ["ROC-AUC Score", "0.8406 (84.06%)", "Strong discriminative ability between churn and non-churn"],
        ["Training Set Size", "5,634 records", "80% of total dataset"],
        ["Test Set Size", "1,409 records", "20% of total dataset (stratified)"],
        ["Number of Trees", "150", "Ensemble of 150 decision trees"],
    ],
)

add_para("12.2 Key Findings", bold=True, size=13)
add_bullet("Month-to-month contract customers have the highest churn rate.",
           bold_prefix="Contract Type: ")
add_bullet("Customers with tenure less than 12 months are most likely to churn.",
           bold_prefix="Tenure: ")
add_bullet("Higher monthly charges correlate with increased churn probability.",
           bold_prefix="Monthly Charges: ")
add_bullet("Customers using Electronic check as payment method show higher churn.",
           bold_prefix="Payment Method: ")
add_bullet("Fiber optic internet users without Tech Support or Online Security churn more.",
           bold_prefix="Internet Service: ")
add_bullet("Gender and phone service have minimal impact on churn prediction.",
           bold_prefix="Low-Impact Features: ")


# ══════════════════════════════════════════════════════════════
#                   13. SCREENSHOTS
# ══════════════════════════════════════════════════════════════

doc.add_page_break()
add_heading_styled("13. Screenshots", level=1)

add_para(
    "[Insert screenshots of the running Streamlit dashboard here]",
    bold=True, size=12
)
add_para("Suggested screenshots to include:", size=11)
add_bullet("Tab 1: Single Customer Prediction form with Gauge Meter result")
add_bullet("Tab 2: Batch CSV upload with scored results table")
add_bullet("Tab 3: Feature Importance horizontal bar chart")
add_bullet("Tab 4: Dataset Analytics with KPI cards and Plotly charts")
add_para(
    "\n(Tip: Open http://localhost:8501, take screenshots of each tab, and paste them here.)",
    size=11
)


# ══════════════════════════════════════════════════════════════
#                14. TECHNOLOGIES USED
# ══════════════════════════════════════════════════════════════

doc.add_page_break()
add_heading_styled("14. Technologies Used", level=1)

add_table(
    ["Technology", "Version", "Purpose"],
    [
        ["Python", "3.13", "Core programming language"],
        ["Pandas", "2.x", "Data loading, cleaning, manipulation"],
        ["NumPy", "1.x", "Numerical computations and array operations"],
        ["Scikit-learn", "1.9", "Train/test split, ROC-AUC evaluation metrics"],
        ["LightGBM", "4.7", "Gradient Boosting Machine Learning model"],
        ["Streamlit", "1.x", "Interactive web dashboard framework"],
        ["Plotly", "7.x", "Interactive charts, gauge meters, bar/box plots"],
        ["Joblib", "1.6", "Model serialization (save/load .pkl files)"],
    ],
)


# ══════════════════════════════════════════════════════════════
#                   15. FUTURE SCOPE
# ══════════════════════════════════════════════════════════════

add_heading_styled("15. Future Scope", level=1)

future_items = [
    ("SHAP Analysis: ", "Integrate SHAP (SHapley Additive exPlanations) for individual prediction "
     "explanations — showing why each specific customer was predicted as high/low risk."),
    ("Hyperparameter Tuning: ", "Use Optuna or GridSearchCV for automated hyperparameter optimization "
     "to potentially improve ROC-AUC beyond 0.84."),
    ("Deep Learning: ", "Experiment with neural network architectures (TabNet, etc.) for comparison."),
    ("Real-time Data Pipeline: ", "Connect to a live database (PostgreSQL/MySQL) for real-time "
     "customer data ingestion instead of static CSV."),
    ("Cloud Deployment: ", "Deploy on AWS/Azure/GCP or Streamlit Cloud for remote access."),
    ("Customer Segmentation: ", "Add K-Means clustering to segment customers by risk profile."),
    ("SMS/Email Alerts: ", "Automatically trigger retention campaign emails when high-risk customers are detected."),
    ("A/B Testing Module: ", "Track retention campaign effectiveness with built-in A/B testing analytics."),
]
for prefix, text in future_items:
    add_bullet(text, bold_prefix=prefix)


# ══════════════════════════════════════════════════════════════
#                    16. CONCLUSION
# ══════════════════════════════════════════════════════════════

add_heading_styled("16. Conclusion", level=1)

add_para(
    "This project successfully demonstrates an end-to-end machine learning pipeline for customer "
    "churn prediction in the telecommunications domain. The LightGBM model, trained on 7,043 real "
    "customer records from IBM's Telco dataset, achieves an ROC-AUC score of 0.8406 — indicating "
    "strong predictive performance."
)
add_para(
    "The interactive Streamlit dashboard transforms the trained model into a practical business tool. "
    "The four-tab layout covers all key use cases: individual risk assessment with visual gauges, "
    "bulk scoring via CSV upload, transparent AI explanations through feature importance charts, "
    "and comprehensive exploratory analytics."
)
add_para(
    "Key business insights revealed by the model include: (1) contract type is a dominant churn "
    "driver — month-to-month customers are at highest risk; (2) higher monthly charges without "
    "corresponding tenure increase signal churn; and (3) payment method and internet service type "
    "are significant predictive features."
)
add_para(
    "The project bridges the gap between data science and business decision-making, providing an "
    "accessible, actionable, and transparent prediction system that can be used by non-technical "
    "retention teams to reduce customer attrition and improve revenue retention."
)


# ══════════════════════════════════════════════════════════════
#                    17. REFERENCES
# ══════════════════════════════════════════════════════════════

doc.add_page_break()
add_heading_styled("17. References", level=1)

references = [
    "[1] IBM Telco Customer Churn Dataset — "
    "https://github.com/IBM/telco-customer-churn-on-icp4d",
    "[2] Ke, G., et al. (2017). 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree.' "
    "Advances in Neural Information Processing Systems (NeurIPS).",
    "[3] Streamlit Documentation — https://docs.streamlit.io/",
    "[4] Plotly Python Graphing Library — https://plotly.com/python/",
    "[5] Scikit-learn: Machine Learning in Python — https://scikit-learn.org/",
    "[6] Pandas Documentation — https://pandas.pydata.org/docs/",
    "[7] Huang, B., Kechadi, M. T., & Buckley, B. (2012). 'Customer churn prediction in "
    "telecommunications.' Expert Systems with Applications, 39(1), 1414-1425.",
    "[8] LightGBM Documentation — https://lightgbm.readthedocs.io/",
]
for ref in references:
    p = doc.add_paragraph()
    run = p.add_run(ref)
    set_run(run, size=11)
    p.paragraph_format.space_after = Pt(4)


# ══════════════════════════════════════════════════════════════
#                       SAVE
# ══════════════════════════════════════════════════════════════

output_path = "Churn_Prediction_Project_Report.docx"
doc.save(output_path)
print(f"Report saved successfully: {os.path.abspath(output_path)}")
print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")
