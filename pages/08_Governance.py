import streamlit as st, pandas as pd, datetime

st.title("Governance")
st.caption("治理稽核")

c1,c2,c3 = st.columns(3)
c1.metric("Model Version", "LightGBM v1.0")
c2.metric("Last Trained", "2026-05")
c3.metric("Data Source", "CSV (抽樣後.csv)")

st.markdown("---")
st.subheader("Audit Log · 操作紀錄")
log = pd.DataFrame([
    {"Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
     "Action": "Dashboard loaded", "User": "analyst", "Note": ""},
])
st.dataframe(log, use_container_width=True)
st.markdown("---")
st.subheader("Manual Review Queue · 待人工覆核名單")
try:
    df = pd.read_csv("outputs/customer_scores.csv", encoding='big5')
    review = df[df.get("risk_tier","") == "High"].sample(min(30, len(df)))
    st.dataframe(review.reset_index(drop=True), use_container_width=True)
except:
    st.info("無法載入客戶評分資料。請確保已執行過 python train.py")