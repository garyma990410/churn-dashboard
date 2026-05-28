import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

DARK_BG   = "#13111f"
SURFACE   = "#201c37"
COLORS    = ["#8b5cf6", "#42c3ff", "#42e8b4", "#ff8b3d", "#ff5da8"]
FONT      = dict(family="Inter, sans-serif", color="#f1efff")

def dark_layout(fig, title=""):
    fig.update_layout(
        title=title,
        paper_bgcolor=DARK_BG, plot_bgcolor=SURFACE,
        font=FONT, margin=dict(l=16, r=16, t=40, b=16),
    )
    return fig

def donut(value, total, label, color, hole=0.68):
    fig = go.Figure(go.Pie(
        values=[value, total - value],
        labels=[label, ""],
        hole=hole,
        marker_colors=[color, "#2a2545"],
        textinfo="none",
        showlegend=False,
    ))
    fig.add_annotation(text=f"<b>{value/total*100:.1f}%</b>",
                       font=dict(size=18, color="#f1efff"), showarrow=False)
    return dark_layout(fig, label)

def bar_comparison(df: pd.DataFrame):
    fig = px.bar(df.reset_index(), x="Model",
                 y=["AUC","Recall","Precision","F1"],
                 barmode="group",
                 color_discrete_sequence=COLORS)
    return dark_layout(fig, "Model Comparison")

def risk_gauge(score: float):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(score * 100, 1),
        number={"suffix": "%", "font": {"color": "#f1efff"}},
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor="#f1efff"),
            bar=dict(color="#8b5cf6"),
            steps=[
                dict(range=[0, 20], color="#2a2545"),
                dict(range=[20, 50], color="#ff8b3d"),
                dict(range=[50, 100], color="#ff5da8"),
            ],
        ),
    ))
    return dark_layout(fig, "Churn Risk Score")

def shap_bar(feature_names, shap_vals):
    df = pd.DataFrame({"Feature": feature_names, "SHAP": shap_vals})
    df = df.sort_values("SHAP", ascending=True)
    fig = px.bar(df, x="SHAP", y="Feature", orientation="h",
                 color_discrete_sequence=["#8b5cf6"])
    return dark_layout(fig, "Feature Importance (SHAP mean |value|)")