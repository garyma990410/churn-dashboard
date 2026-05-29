import streamlit as st, pandas as pd, plotly.graph_objects as go
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.plotting import dark_layout, donut, COLORS
from config import HIGH_RISK_THRESH

@st.cache_data
def load():
    try: return pd.read_csv("outputs/customer_scores.csv", encoding='big5')
    except FileNotFoundError: return pd.DataFrame()

df = load()
st.title("Overview")
st.caption("客戶流失預警總覽")

if df.empty:
    st.error("無法載入客戶數據。請確保已執行過 python train.py 並生成了 outputs/customer_scores.csv")
    st.stop()

total        = len(df)
churn_rate   = df["是否流失"].mean()
high_risk    = (df["churn_score"] >= HIGH_RISK_THRESH).sum()
auto_renew   = (df["是否自動續約"] == 1).mean()
cancel_rate  = (df["近一次交易是否取消"] == 1).mean()
avg_active   = df["近一個月活躍天數"].mean()

c1,c2,c3,c4,c5,c6 = st.columns(6)
for col, label, val in zip(
    [c1,c2,c3,c4,c5,c6],
    ["Total Customers 總客戶","Churn Rate 流失率",
     "High-Risk 高風險","Auto-Renew 自動續約",
     "Cancel Rate 取消率","Avg Active Days 均活躍天"],
    [f"{total:,}", f"{churn_rate:.2%}",
     f"{high_risk:,}", f"{auto_renew:.2%}",
     f"{cancel_rate:.2%}", f"{avg_active:.1f}"]
):
    with col:
        st.markdown(f'''<div class="metric-card"><p style="color:#b9b3e4;font-size:.8rem">{label}</p>
        <h2 style="color:#f1efff;margin:0">{val}</h2></div>''', unsafe_allow_html=True)

st.markdown("---")
st.subheader("Risk Distribution · 5 Donuts 五大維度甜甜圈")
d1,d2,d3,d4,d5 = st.columns(5)

panels = [
    ("High-Risk Customers\n高風險客群", high_risk, total, COLORS[0]),
    ("Active Users\n近期活躍用戶",
     (df["近一個月活躍天數"] > 10).sum(), total, COLORS[1]),
    ("Auto-Renew Ratio\n自動續約比",
     (df["是否自動續約"]==1).sum(), total, COLORS[2]),
    ("High-Value Customers\n高價值客群",
     (df["近兩個月付費次數"]>=2).sum(), total, COLORS[3]),
    ("Cancel Risk\n近期取消風險",
     (df["近一次交易是否取消"]==1).sum(), total, COLORS[4]),
]
for col, (label, val, tot, color) in zip([d1,d2,d3,d4,d5], panels):
    with col:
        main, sub = label.split("\n")
        st.plotly_chart(donut(val, tot, "", color), use_container_width=True)
        st.markdown(f"**{main}**")
        st.caption(sub)