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
st.sidebar.title("Project summary")
st.sidebar.write("Dashboard built from source-verified public data only.")
st.sidebar.markdown("### Official sources")
for label, url in SOURCE_PAGES.items():
    st.sidebar.markdown(f"- [{label}]({url})")

# العنوان الرئيسي والفرعي
st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

st.warning(
    "Important: this app separates current public metrics from historical context. "
    "It does not provide diagnosis, treatment advice, or patient-level prediction."
)

# عرض معلومات أساسية باستخدام Mertic
col1, col2, col3, col4 = st.columns(4)
col1.metric("Hospital", data["hospital_name"])
col2.metric("CCN", data["ccn"])
col3.metric("Location", f'{data["city"]}, {data["state"]}')
col4.metric("Latest update used", latest_update)

metric_a, metric_b, metric_c = st.columns(3)
metric_a.metric("Readmission mix", readmission_mix)
metric_b.metric("Leapfrog grade", safety_grade)
metric_c.metric("Beds (historical context)", beds)

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
st.caption(data["disclaimer"])
