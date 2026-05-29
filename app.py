import streamlit as st

st.set_page_config(
    page_title="Customer Retention Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Global dark CSS
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:#13111f}
[data-testid="stSidebar"]{background:#1a1730}
[data-testid="stSidebar"] *{color:#d9d4ff !important}
.block-container{padding-top:1.2rem}
h1,h2,h3{color:#f1efff !important}
.metric-card{
  background:linear-gradient(180deg,#262247,#1e1a38);
  border:1px solid rgba(179,171,255,.14);
  border-radius:14px; padding:1rem 1.2rem;
}
</style>
""", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("pages/00_Home.py",              title="Home",              icon="🏠"),
    st.Page("pages/01_Overview.py",          title="Overview",          icon="📊"),
    st.Page("pages/02_Data_Snapshot.py",     title="Data Snapshot",     icon="📋"),
    st.Page("pages/03_Model_Comparison.py",  title="Model Comparison",  icon="🤖"),
    st.Page("pages/04_Customer_Query.py",    title="Customer Query",     icon="🔍"),
    st.Page("pages/05_Driver_Analysis.py",   title="Driver Analysis",    icon="📈"),
    st.Page("pages/06_Retention_Strategy.py",title="Retention Strategy", icon="🎯"),
    st.Page("pages/07_Financial_Impact.py",  title="Financial Impact",   icon="💰"),
    st.Page("pages/08_Governance.py",        title="Governance",         icon="🔒"),
])
pg.run()