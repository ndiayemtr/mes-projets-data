from pathlib import Path

import streamlit as st
import pandas as pd

from utils import predict_churn

st.set_page_config(layout="wide")

st.title("Customer Churn Dashboard")

# ======================
# LOAD DATA
# ======================

BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "data.csv")

# ======================
# KPI
# ======================
st.subheader("KPI Globaux")

col1, col2, col3 = st.columns(3)

col1.metric("Churn Rate", f"{round(df['Churn'].mean()*100,2)} %")
col2.metric("Monthly Charges", round(df["MonthlyCharges"].mean(),2))
col3.metric("Avg Tenure", round(df["tenure"].mean(),1))

st.divider()

# ======================
# FILTERS
# ======================
st.sidebar.header("Filters")

contract_filter = st.sidebar.multiselect(
    "Contract",
    df["Contract"].unique(),
    df["Contract"].unique()
)

df_filtered = df[df["Contract"].isin(contract_filter)]

# ======================
# CHARTS
# ======================
st.subheader("Churn by Contract")

st.bar_chart(df_filtered.groupby("Contract")["Churn"].mean())

st.subheader("Monthly Charges Distribution")

st.line_chart(df_filtered["MonthlyCharges"].head(300))

# ======================
# PREDICTION
# ======================
st.sidebar.header("Client Simulation")

tenure = st.sidebar.slider("Tenure", 0, 72, 12)
monthly = st.sidebar.slider("Monthly Charges", 20, 120, 60)

contract = st.sidebar.selectbox("Contract", df["Contract"].unique())
payment = st.sidebar.selectbox("Payment Method", df["PaymentMethod"].unique())
paperless = st.sidebar.selectbox("Paperless Billing", [0,1])
ratio = st.sidebar.slider("Charge Ratio", 0.0, 3.5, 1.0)

if st.sidebar.button("Predict Churn"):

    input_data = {
        "tenure": tenure,
        "MonthlyCharges": monthly,
        "Contract": contract,
        "PaymentMethod": payment,
        "PaperlessBilling": paperless,
        "charge_ratio": ratio
    }

    proba, pred = predict_churn(input_data)

    st.subheader("Prediction Result")

    col1, col2 = st.columns(2)

    col1.metric("Churn Probability", f"{round(proba*100,2)} %")

    if pred == 1:
        col2.error("High Risk Customer")
        st.warning("Recommend: Discount / Retention offer")
    else:
        col2.success("Stable Customer")