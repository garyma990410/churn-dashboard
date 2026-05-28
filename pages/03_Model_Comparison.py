import streamlit as st, pandas as pd, json
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.plotting import bar_comparison, dark_layout, DARK_BG, SURFACE, COLORS

st.title("Model Comparison")
st.caption("模型比較")

try:
    with open("models/model_metrics.json") as f:
        metrics = json.load(f)
    df = pd.DataFrame(metrics).T
    df.index.name = "Model"
    st.dataframe(df.style.highlight_max(color="#8b5cf6", axis=0), use_container_width=True)
    st.markdown("---")
    st.plotly_chart(bar_comparison(df), use_container_width=True)
    st.markdown("---")
    st.subheader("Best Model · 最佳模型")
    best = df["AUC"].idxmax()
    b = df.loc[best]
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Model", best)
    c2.metric("AUC", b["AUC"])
    c3.metric("Recall 召回率", b["Recall"])
    c4.metric("F1", b["F1"])
except FileNotFoundError:
    st.warning("Run `python train.py` to generate model metrics.")