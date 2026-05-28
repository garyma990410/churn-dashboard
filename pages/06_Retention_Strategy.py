import streamlit as st, pandas as pd, plotly.express as px
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.plotting import DARK_BG, SURFACE, COLORS

@st.cache_data
def load():
    try: return pd.read_csv("outputs/customer_scores.csv")
    except: return pd.DataFrame()

df = load()
st.title("Retention Strategy")
st.caption("續留策略")

if df.empty:
    st.warning("Run `python train.py` first."); st.stop()

if "risk_tier" not in df.columns or "value_tier" not in df.columns:
    st.warning("Risk/value tiers not found. Run train.py."); st.stop()

segments = {
    ("High","High Value"):  ("Priority Retention 優先挽留",   "#8b5cf6", "專屬客服 · 首月半價折扣 · 綁卡優惠"),
    ("High","Low Value"):   ("Automated Defense 自動防禦",    "#ff5da8", "App 推播 · EDM · 低成本點數任務"),
    ("Medium","High Value"):("Loyalty Growth 忠誠培育",       "#42c3ff", "升級方案 · 年繳制 · VIP 特權"),
    ("Medium","Low Value"): ("Nurturing Pool 養成培育",       "#42e8b4", "個人化推薦 · 新手引導"),
    ("Low","High Value"):   ("VIP Maintenance 高價值維護",    "#ff8b3d", "定期關懷 · 週年禮遇"),
}

def segment(row):
    key = (row.get("risk_tier","Low"), row.get("value_tier","Low Value"))
    return segments.get(key, ("Standard 一般", "#666", "常規推播"))[0]

df["segment"] = df.apply(segment, axis=1)
seg_counts = df["segment"].value_counts().reset_index()
seg_counts.columns = ["Segment","Count"]

c1, c2 = st.columns([1,1])
with c1:
    st.subheader("Segment Distribution · 客群分布")
    fig = px.pie(seg_counts, values="Count", names="Segment",
                 color_discrete_sequence=COLORS, hole=0.45)
    fig.update_layout(paper_bgcolor=DARK_BG, font_color="#f1efff")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Segment Cards · 策略卡片")
    for (rt, vt), (seg_name, color, action) in segments.items():
        cnt = len(df[(df["risk_tier"]==rt) & (df["value_tier"]==vt)])
        st.markdown(f"""
<div style="background:linear-gradient(135deg,{color}22,#1e1a38);
border:1px solid {color}44;border-radius:12px;padding:.8rem 1rem;margin-bottom:.6rem">
<b style="color:{color}">{seg_name}</b>&nbsp;·&nbsp;
<span style="color:#b9b3e4">{cnt:,} customers</span><br>
<small style="color:#867cb8">{action}</small>
</div>""", unsafe_allow_html=True)