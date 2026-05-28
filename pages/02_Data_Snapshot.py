import streamlit as st, pandas as pd, plotly.express as px
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.plotting import dark_layout, DARK_BG, SURFACE, COLORS

@st.cache_data
def load():
    try: return pd.read_csv("outputs/customer_scores.csv")
    except: return pd.read_csv("data/抽樣後.csv")

df = load()
st.title("Data Snapshot")
st.caption("資料概況")

c1,c2,c3 = st.columns(3)
c1.metric("Rows 筆數", f"{len(df):,}")
c2.metric("Columns 欄位", df.shape[1])
c3.metric("Churn Rate 流失率", f"{df['是否流失'].mean():.2%}")

st.markdown("---")
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Churn Distribution · 流失分布")
    cnt = df["是否流失"].value_counts().reset_index()
    cnt.columns = ["is_churn","count"]
    fig = px.pie(cnt, values="count", names="is_churn",
                 color_discrete_sequence=[COLORS[0], COLORS[1]], hole=0.5)
    fig.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=SURFACE, font_color="#f1efff")
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.subheader("Auto-Renew vs Churn · 自動續約與流失")
    grp = df.groupby("是否自動續約")["是否流失"].mean().reset_index()
    grp.columns = ["auto_renew","churn_rate"]
    fig2 = px.bar(grp, x="auto_renew", y="churn_rate",
                  color_discrete_sequence=[COLORS[2]])
    fig2.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=SURFACE, font_color="#f1efff")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.subheader("Active Days Distribution · 活躍天數分布")
fig3 = px.histogram(df, x="近一個月活躍天數", nbins=32,
                    color_discrete_sequence=[COLORS[3]])
fig3.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=SURFACE, font_color="#f1efff")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.subheader("Raw Data Preview · 資料預覽")
st.sidebar.markdown("## ⚙️ Data Filters")
show_churn = st.sidebar.selectbox("Churn Filter", ["All", "Churned", "Retained"])
if show_churn == "Churned":   df = df[df["是否流失"]==1]
elif show_churn == "Retained": df = df[df["是否流失"]==0]
st.dataframe(df.head(200), use_container_width=True)