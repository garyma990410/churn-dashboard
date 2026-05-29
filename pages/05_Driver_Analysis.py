import streamlit as st, pandas as pd, pickle, numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.plotting import shap_bar, dark_layout, COLORS, DARK_BG, SURFACE
from config import FEATURE_COLS
import plotly.express as px

st.title("Driver Analysis")
st.caption("流失驅動因子")

FEATS = FEATURE_COLS + ["high_cancel_risk","activity_ratio","payment_low"]

@st.cache_data
def load():
    try: return pd.read_csv("outputs/customer_scores.csv", encoding='big5')
    except: return pd.DataFrame()

@st.cache_resource
def load_model():
    try:
        with open("models/lightgbm.pkl","rb") as f: return pickle.load(f)
    except: return None

df = load()
clf = load_model()

if df.empty or clf is None:
    st.error("無法載入客戶數據或模型。請確保已執行過 python train.py"); st.stop()

feats_in_df = [c for c in FEATS if c in df.columns]
importances = clf.feature_importances_ if hasattr(clf,"feature_importances_") else np.zeros(len(feats_in_df))
st.plotly_chart(shap_bar(feats_in_df, importances[:len(feats_in_df)]),
                use_container_width=True)

st.markdown("---")
st.subheader("Feature Correlation with Churn · 特徵與流失相關性")
numeric = df[feats_in_df + ["是否流失"]].corr()["是否流失"].drop("是否流失").reset_index()
numeric.columns = ["Feature","Correlation"]
numeric = numeric.sort_values("Correlation", ascending=True)
fig = px.bar(numeric, x="Correlation", y="Feature", orientation="h",
             color="Correlation", color_continuous_scale=["#42c3ff","#8b5cf6","#ff5da8"])
fig.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=SURFACE, font_color="#f1efff")
st.plotly_chart(fig, use_container_width=True)