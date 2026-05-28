import streamlit as st, pandas as pd
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from config import (DEFAULT_MONTHLY_REVENUE, DEFAULT_EXTENSION_MONTHS,
                    DEFAULT_SUCCESS_RATE, DEFAULT_OUTREACH_COST)

@st.cache_data
def load():
    try: return pd.read_csv("outputs/customer_scores.csv")
    except: return pd.DataFrame()

df = load()
st.title("Financial Impact")
st.caption("財務影響試算")

st.sidebar.markdown("## 💰 Assumption Sliders 假設參數")
monthly_rev = st.sidebar.slider("Monthly Revenue / Customer (USD) 每位月收入",
                                 1.0, 50.0, DEFAULT_MONTHLY_REVENUE, 0.5)
ext_months  = st.sidebar.slider("Extension Months 延長留存月數", 1, 24, DEFAULT_EXTENSION_MONTHS)
success_r   = st.sidebar.slider("Retention Success Rate 挽留成功率", 0.01, 0.50,
                                 DEFAULT_SUCCESS_RATE, 0.01)
outreach    = st.sidebar.slider("Outreach Cost / Customer (USD) 每位接觸成本",
                                 0.5, 20.0, DEFAULT_OUTREACH_COST, 0.5)
deploy_cost = st.sidebar.number_input("System Deployment Cost (USD) 系統導入成本",
                                       value=52000, step=1000)

if df.empty:
    st.warning("Run `python train.py` first."); st.stop()

if "risk_tier" in df.columns:
    high_risk = len(df[df["risk_tier"]=="High"])
else:
    high_risk = int(len(df) * 0.20)

saved         = int(high_risk * success_r)
retained_rev  = saved * monthly_rev * ext_months
outreach_cost = high_risk * outreach
net_benefit   = retained_rev - outreach_cost - deploy_cost
roi           = (net_benefit / deploy_cost * 100) if deploy_cost > 0 else 0

c1,c2,c3,c4 = st.columns(4)
c1.metric("High-Risk Contacts 接觸高風險客數", f"{high_risk:,}")
c2.metric("Estimated Saved 預計挽留人數", f"{saved:,}")
c3.metric("Retained Revenue 保留收入 (USD)", f"${retained_rev:,.0f}")
c4.metric("Net Benefit 淨效益 (USD)", f"${net_benefit:,.0f}",
          delta=f"ROI {roi:.1f}%")

st.markdown("---")
col_a, col_b = st.columns(2)
with col_a:
    st.markdown(f"""
| Item 項目 | Value 數值 |
|---|---|
| High-risk customers | {high_risk:,} |
| Estimated retained | {saved:,} |
| Retained revenue | ${retained_rev:,.0f} |
| Outreach cost | ${outreach_cost:,.0f} |
| Deployment cost | ${deploy_cost:,} |
| Net benefit | ${net_benefit:,.0f} |
| ROI | {roi:.1f}% |
""")
with col_b:
    import plotly.graph_objects as go
    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative","relative","relative","total"],
        x=["Retained Revenue","Outreach Cost","Deploy Cost","Net Benefit"],
        y=[retained_rev, -outreach_cost, -deploy_cost, net_benefit],
        connector={"line":{"color":"#8b5cf6"}},
        increasing={"marker":{"color":"#42e8b4"}},
        decreasing={"marker":{"color":"#ff5da8"}},
        totals={"marker":{"color":"#8b5cf6"}},
    ))
    fig.update_layout(paper_bgcolor="#13111f", plot_bgcolor="#201c37",
                      font_color="#f1efff", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)