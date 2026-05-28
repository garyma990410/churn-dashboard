import streamlit as st, pandas as pd
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.plotting import risk_gauge

@st.cache_data
def load():
    try: return pd.read_csv("outputs/customer_scores.csv")
    except: return pd.DataFrame()

df = load()
st.title("Customer Query")
st.caption("客戶流失風險查詢")

st.sidebar.markdown("## 🔍 Customer Search 客戶查詢")
query = st.sidebar.text_input("Enter msno / Customer ID")

if df.empty:
    st.warning("Run `python train.py` first."); st.stop()

if query:
    row = df[df["msno"].astype(str).str.contains(query, case=False, na=False)]
    if row.empty:
        st.error("Customer not found. 查無此客戶。")
    else:
        r = row.iloc[0]
        c1,c2,c3 = st.columns(3)
        c1.metric("Risk Tier 風險層", r.get("risk_tier","N/A"))
        c2.metric("Value Tier 價值層", r.get("value_tier","N/A"))
        c3.metric("Churn Label 實際標籤", "Churned" if r["是否流失"]==1 else "Retained")
        st.plotly_chart(risk_gauge(r.get("churn_score", 0.0)), use_container_width=True)
        st.markdown("---")
        st.subheader("Customer Profile · 客戶特徵")
        display_cols = ["msno","是否流失","會員年資天數","年齡","是否自動續約",
                        "近一次交易是否取消","近兩個月付費次數","近一個月活躍天數"]
        if "churn_score" in row.columns:
            display_cols += ["churn_score","risk_tier","value_tier"]
        st.dataframe(row[display_cols].T.rename(columns={row.index[0]: "Value"}),
                     use_container_width=True)
else:
    st.info("Enter a customer ID in the sidebar to query.")
    st.subheader("High-Risk Customers · 高風險名單")
    if "risk_tier" in df.columns:
        high = df[df["risk_tier"]=="High"].head(50)
        st.dataframe(high.reset_index(drop=True), use_container_width=True)