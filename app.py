import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import APP_SUBTITLE, APP_TITLE, SOURCE_PAGES
from src.data_loader import load_verified_data
from src.utils import (
    build_distribution_dataframe,
    facts_to_dataframe,
    freshness_order,
    get_fact_value,
)

st.set_page_config(
    page_title="Johns Hopkins Readmission Intelligence",
    page_icon="🏥",
    layout="wide",
)

# Load data
data = load_verified_data()

facts_df = facts_to_dataframe(data["verified_facts"])

facts_df["freshness"] = pd.Categorical(
    facts_df["freshness"],
    categories=freshness_order(),
    ordered=True,
)

facts_df = facts_df.sort_values(
    by=["freshness", "category", "label"]
).reset_index(drop=True)

current_df = facts_df[facts_df["freshness"] == "current"].reset_index(drop=True)

historical_df = facts_df[facts_df["freshness"] != "current"].reset_index(drop=True)

distribution_df = build_distribution_dataframe(
    data["readmission_distribution"]
)

source_audit_df = pd.DataFrame(data["source_audit"])

readmission_mix = get_fact_value(
    facts_df,
    "Readmission measure distribution"
)

latest_update = get_fact_value(
    facts_df,
    "Latest federal public quality update used in this app"
)

safety_grade = get_fact_value(
    facts_df,
    "Leapfrog safety grade"
)

beds = get_fact_value(
    facts_df,
    "Hospital beds"
)

# Sidebar
st.sidebar.markdown("## 🏥 Dashboard Information")

st.sidebar.info(
    "Professional healthcare intelligence dashboard built using "
    "official Medicare, CMS, Leapfrog, and Johns Hopkins public sources."
)

st.sidebar.markdown("### Data Governance Principles")

st.sidebar.markdown(
    """
- Official public sources only
- No patient-level data
- Historical and current metrics separated
- Source-verifiable facts only
- Portfolio-safe healthcare analytics
"""
)

st.sidebar.markdown("### Official Sources")

for label, url in SOURCE_PAGES.items():
    st.sidebar.markdown(f"- [{label}]({url})")

# Custom styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.7rem;
        font-weight: 800;
        color: #002D72;
        margin-bottom: 0rem;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 2rem;
    }

    .info-box {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 12px;
        border-left: 6px solid #2563EB;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main title
st.markdown(
    '<div class="main-title">Johns Hopkins Readmission & Quality Intelligence Dashboard</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Source-verified healthcare quality, safety, and readmission intelligence dashboard built from official public U.S. sources.</div>',
    unsafe_allow_html=True,
)

# Professional disclosure
st.markdown(
    """
    <div class="info-box">
    <strong>Professional disclosure:</strong><br>
    This dashboard presents source-verified public healthcare quality information only.
    It does not provide diagnosis, treatment recommendations, or patient-level prediction.
    Historical metrics are clearly separated from current public indicators.
    </div>
    """,
    unsafe_allow_html=True,
)

# Hospital overview
st.markdown("## Hospital Overview")

top_col1, top_col2 = st.columns(2)

with top_col1:
    st.metric("Hospital", data["hospital_name"])
    st.metric("CCN", data["ccn"])
    st.metric("Location", f'{data["city"]}, {data["state"]}')

with top_col2:
    st.metric("Latest Update Used", latest_update)
    st.metric("Leapfrog Grade", safety_grade)
    st.metric("Beds", beds)

# Readmission summary
st.markdown("## Read
