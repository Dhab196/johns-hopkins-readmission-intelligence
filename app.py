import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import SOURCE_PAGES
from src.data_loader import load_verified_data
from src.utils import (
    build_distribution_dataframe,
    facts_to_dataframe,
    freshness_order,
    get_fact_value,
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Johns Hopkins Readmission Intelligence",
    page_icon="🏥",
    layout="wide",
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

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

current_df = facts_df[
    facts_df["freshness"] == "current"
].reset_index(drop=True)

historical_df = facts_df[
    facts_df["freshness"] != "current"
].reset_index(drop=True)

distribution_df = build_distribution_dataframe(
    data["readmission_distribution"]
)

source_audit_df = pd.DataFrame(
    data["source_audit"]
)

# ---------------------------------------------------
# KPI VALUES
# ---------------------------------------------------

readmission_mix = get_fact_value(
    facts_df,
    "Readmission measure distribution",
)

latest_update = get_fact_value(
    facts_df,
    "Latest federal public quality update used in this app",
)

safety_grade = get_fact_value(
    facts_df,
    "Leapfrog safety grade",
)

beds = get_fact_value(
    facts_df,
    "Hospital beds",
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F4F8FC;
    }

    .hero-container {
        background: linear-gradient(135deg, #002D72 0%, #0B5CAB 100%);
        padding: 2.5rem;
        border-radius: 22px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    }

    .hero-title {
        font-size: 2.9rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
        line-height: 1.7;
    }

    .jh-badge {
        display: inline-block;
        background-color: rgba(255,255,255,0.15);
        padding: 0.45rem 0.9rem;
        border-radius: 999px;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.2);
    }

    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(15,23,42,0.06);
        border: 1px solid #E2E8F0;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 2rem;
        margin-bottom
