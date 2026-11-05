import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

print("Downloading Telco Churn dataset...")
url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
df = pd.read_csv(url)

# Clean TotalCharges (contains blanks/spaces for new customers with tenure = 0)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Target variable mapping
df["Churn"] = df["Churn"].apply(lambda x: 1 if x == "Yes" else 0)

# Select key business features
features = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "TechSupport",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
]

X = df[features].copy()
y = df["Churn"]

# Convert string columns to categorical type for LightGBM
cat_cols = X.select_dtypes(include=["object"]).columns.tolist()
for col in cat_cols:
    X[col] = X[col].astype("category")

# Stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Train LightGBM Classifier
lgb_model = LGBMClassifier(
    n_estimators=150, learning_rate=0.05, max_depth=5, random_state=42
)
lgb_model.fit(X_train, y_train)

# Evaluation
y_pred_proba = lgb_model.predict_proba(X_test)[:, 1]
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")

# Save artifacts
package = {"model": lgb_model, "features": features, "categorical": cat_cols}
joblib.dump(package, "churn_artifacts.pkl")
# Also save cleaned CSV sample for app analytics
df.to_csv("telco_clean.csv", index=False)
print(
    "Artifacts saved: churn_artifacts.pkl and telco_clean.csv ready for app."
)
