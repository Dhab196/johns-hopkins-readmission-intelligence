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

# تحميل البيانات مع معالجة الأخطاء
data = load_verified_data()
if not data:
    st.error("تعذر تحميل بيانات الحقائق الموثقة. يرجى التأكد من وجود 'data/manual/jhh_verified_facts.json'.")
    st.stop()

facts_df = facts_to_dataframe(data["verified_facts"])
facts_df["freshness"] = pd.Categorical(
    facts_df["freshness"],
    categories=freshness_order(),
    ordered=True,
)
facts_df = facts_df.sort_values(by=["freshness", "category", "label"]).reset_index(drop=True)

current_df = facts_df[facts_df["freshness"] == "current"].reset_index(drop=True)
historical_df = facts_df[facts_df["freshness"] != "current"].reset_index(drop=True)

distribution_df = build_distribution_dataframe(data.get("readmission_distribution", {}))
source_audit_df = pd.DataFrame(data.get("source_audit", []))

readmission_mix = get_fact_value(facts_df, "Readmission measure distribution")
latest_update = get_fact_value(facts_df, "Latest federal public quality update used in this app")
safety_grade = get_fact_value(facts_df, "Leapfrog safety grade")
beds = get_fact_value(facts_df, "Hospital beds")

# الشريط الجانبي للتطبيق
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
st.sidebar.write("Dashboard built from source-verified public data only.")
st.sidebar.markdown("### Official sources")
for label, url in SOURCE_PAGES.items():
    st.sidebar.markdown(f"- [{label}]({url})")

# العنوان الرئيسي والفرعي
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

    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 1.5rem;
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
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Johns Hopkins Readmission & Quality Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Source-verified healthcare quality, safety, and readmission intelligence dashboard built from official public U.S. sources.</div>',
    unsafe_allow_html=True
st.markdown(
    """
    <div class="info-box">
    <strong>Professional disclosure:</strong><br>
    This dashboard presents source-verified public healthcare quality information only.
    It does not provide diagnosis, treatment recommendations, or patient-level prediction.
    Historical metrics are clearly separated from current public indicators.
    </div>
    """,
    unsafe_allow_html=True
)
# عرض معلومات أساسية باستخدام Mertic
st.markdown("## Hospital overview")

top_col1, top_col2 = st.columns(2)

with top_col1:
    st.metric("Hospital", data["hospital_name"])
    st.metric("CCN", data["ccn"])
    st.metric("Location", f'{data["city"]}, {data["state"]}')

with top_col2:
    st.metric("Latest update used", latest_update)
    st.metric("Leapfrog grade", safety_grade)
    st.metric("Beds", beds)

st.markdown("## Readmission summary")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    st.metric(
        "Readmission distribution",
        readmission_mix
    )

with summary_col2:
    st.info(
        "Source-verified public healthcare quality dashboard "
        "built using Medicare, CMS, Leapfrog, and Johns Hopkins sources."
    )
# إنشاء علامات التبويب
tabs = st.tabs([
    "Overview",
    "Verified facts",
    "Interventions",
    "Sources & methodology",
])

with tabs[0]:
    st.subheader("Executive summary")
    st.write(
        "This dashboard presents source-verified information about readmission, safety, "
        "and institutional context for The Johns Hopkins Hospital. Current metrics are displayed "
        "separately from historical context."
    )

    fig = px.bar(
        distribution_df,
        x="comparison",
        y="count",
        text="count",
        color="comparison",
        color_discrete_map={
            "Above national average": "#D97706",
            "Same as national average": "#2563EB",
            "Below national average": "#059669",
        },
        title="Readmission measure distribution"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
    showlegend=False,
    xaxis_title="",
    yaxis_title="Number of measures",
    margin=dict(l=20, r=20, t=60, b=20),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14),
    )
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Data integrity rules")
    st.markdown(
        "- Only publicly available source-verified information is included.\n"
        "- Current and historical information are separated.\n"
        "- Historical outcomes are labeled with their original year.\n"
        "- No patient-level data or private clinical claims are used."
    )

with tabs[1]:
    st.subheader("Current official metrics")
    current_columns = ["category", "label", "value", "detail", "as_of", "source_url"]
    st.dataframe(
        current_df.reindex(columns=current_columns),
        use_container_width=True,
    )

    st.subheader("Historical and institutional context")
    historical_columns = ["category", "label", "value", "detail", "as_of", "freshness", "source_url"]
    st.dataframe(
        historical_df.reindex(columns=historical_columns),
        use_container_width=True,
    )

    st.subheader("Full verified fact register")
    st.dataframe(facts_df, use_container_width=True)

with tabs[2]:
    st.subheader("Official interventions described by source pages")
    for item in data["official_interventions"]:
        with st.expander(item["name"]):
            st.write(item["summary"])
            st.markdown(f"[Open official source]({item['source_url']})")

    st.info(
        "These intervention descriptions are included as institutional context. "
        "Historical outcomes from 2016 are shown separately."
    )

with tabs[3]:
    st.subheader("Source audit")
    st.dataframe(source_audit_df, use_container_width=True)

    st.subheader("Methodology")
    st.markdown(
        "1. Identify official public sources (Medicare, CMS, Johns Hopkins, Leapfrog).\n"
        "2. Extract source-verifiable facts suitable for public portfolio use.\n"
        "3. Label each fact as current or historical.\n"
        "4. Present current federal/public quality indicators separately from historical context.\n"
        "5. Avoid unsupported patient-level predictions or private data."
    )

    st.subheader("Direct source links")
    for label, url in SOURCE_PAGES.items():
        st.markdown(f"- [{label}]({url})")

st.divider()
st.markdown("---")

st.caption(
    "Johns Hopkins Readmission & Quality Intelligence Dashboard | "
    "Built with Python, Streamlit, Pandas, and Plotly | "
    "Source-verified public healthcare intelligence"
)

st.caption(data["disclaimer"])
