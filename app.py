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
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------
# LOAD DATA SAFELY
# ---------------------------------------------------

data = load_verified_data() or {}

verified_facts = data.get("verified_facts", [])
source_audit = data.get("source_audit", [])
official_interventions = data.get("official_interventions", [])
distribution_source = data.get("readmission_distribution", {})

facts_df = facts_to_dataframe(verified_facts)

if not facts_df.empty and "freshness" in facts_df.columns:
    facts_df["freshness"] = pd.Categorical(
        facts_df["freshness"],
        categories=freshness_order(),
        ordered=True,
    )
    facts_df = facts_df.sort_values(
        by=["freshness", "category", "label"]
    ).reset_index(drop=True)
else:
    facts_df = pd.DataFrame(columns=["category", "label", "value", "detail", "as_of", "freshness", "source_url"])

current_df = facts_df[facts_df.get("freshness", pd.Series(dtype=str)) == "current"].reset_index(drop=True) if not facts_df.empty else pd.DataFrame()
historical_df = facts_df[facts_df.get("freshness", pd.Series(dtype=str)) != "current"].reset_index(drop=True) if not facts_df.empty else pd.DataFrame()

distribution_df = build_distribution_dataframe(distribution_source)
source_audit_df = pd.DataFrame(source_audit)

readmission_mix = get_fact_value(facts_df, "Readmission measure distribution")
latest_update = get_fact_value(facts_df, "Latest federal public quality update used in this app")
safety_grade = get_fact_value(facts_df, "Leapfrog safety grade")
beds = get_fact_value(facts_df, "Hospital beds")

hospital_name = data.get("hospital_name", "The Johns Hopkins Hospital")
ccn = data.get("ccn", "210009")
city = data.get("city", "Baltimore")
state = data.get("state", "Maryland")
disclaimer = data.get(
    "disclaimer",
    "This dashboard summarizes publicly available institutional quality and safety information. It does not provide diagnosis, treatment advice, or patient-level prediction.",
)

# ---------------------------------------------------
# THEME / STYLING
# ---------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #F8FBFF 0%, #EEF4FB 100%);
    }

    .hero {
        background: linear-gradient(135deg, #002D72 0%, #0B5CAB 55%, #134B8A 100%);
        border-radius: 24px;
        padding: 28px 28px 24px 28px;
        color: white;
        box-shadow: 0 16px 40px rgba(2, 8, 23, 0.16);
        margin-bottom: 22px;
        border: 1px solid rgba(255,255,255,0.15);
    }

    .eyebrow {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.18);
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 14px;
        letter-spacing: 0.2px;
    }

    .hero-title {
        font-size: 2.5rem;
        line-height: 1.1;
        font-weight: 800;
        margin: 0 0 10px 0;
    }

    .hero-subtitle {
        font-size: 1.02rem;
        line-height: 1.65;
        opacity: 0.96;
        max-width: 980px;
        margin: 0;
    }

    .disclosure {
        background: #EFF6FF;
        border-left: 6px solid #2563EB;
        padding: 16px 18px;
        border-radius: 16px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
        margin: 14px 0 8px 0;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0F172A;
        margin: 28px 0 12px 0;
    }

    .jh-card {
        background: white;
        border-radius: 18px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        padding: 18px;
    }

    .footer {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 14px 16px;
        text-align: center;
        color: #334155;
        margin-top: 24px;
    }

    .logo-badge {
        width: 72px;
        height: 72px;
        border-radius: 18px;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        font-weight: 800;
        margin-bottom: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #002D72 0%, #0B5CAB 100%);
        color: white;
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 14px;
        border: 1px solid rgba(255,255,255,0.12);
    ">
        <div style="font-size: 0.9rem; opacity: 0.95; margin-bottom: 8px;">Johns Hopkins Medicine</div>
        <div style="font-size: 1.3rem; font-weight: 800; line-height: 1.2;">Readmission Intelligence</div>
        <div style="font-size: 0.92rem; margin-top: 10px; opacity: 0.95;">
            Executive healthcare quality dashboard
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.info(
    "Professional healthcare intelligence dashboard built using official Medicare, CMS, Leapfrog, and Johns Hopkins public sources."
)

st.sidebar.markdown("### Data Governance")

st.sidebar.markdown(
    """
- Official public sources only
- No patient-level data
- Current and historical metrics separated
- Source-verifiable facts only
- Portfolio-safe healthcare analytics
"""
)

st.sidebar.markdown("### Official Sources")

for label, url in SOURCE_PAGES.items():
    st.sidebar.markdown(f"- [{label}]({url})")

# ---------------------------------------------------
# HERO
# ---------------------------------------------------

st.markdown(
    f"""
    <div class="hero">
        <div class="logo-badge">JH</div>
        <div class="eyebrow">Johns Hopkins Medicine • Baltimore, Maryland</div>
        <div class="hero-title">Johns Hopkins Readmission & Quality Intelligence Dashboard</div>
        <p class="hero-subtitle">
            Source-verified public healthcare intelligence dashboard for quality,
            safety, readmission, and institutional context. Built for executive review,
            portfolio presentation, and ATS-friendly documentation.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="disclosure">
        <strong>Professional disclosure:</strong><br>
        This dashboard presents source-verified public healthcare quality information only.
        It does not provide diagnosis, treatment recommendations, or patient-level prediction.
        Historical metrics are clearly separated from current public indicators.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------
# OVERVIEW METRICS
# ---------------------------------------------------

st.markdown('<div class="section-title">Hospital Overview</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Hospital", hospital_name)

with m2:
    st.metric("CCN", ccn)

with m3:
    st.metric("Location", f"{city}, {state}")

with m4:
    st.metric("Latest Update", latest_update)

m5, m6, m7 = st.columns(3)

with m5:
    st.metric("Readmission Mix", readmission_mix)

with m6:
    st.metric("Leapfrog Grade", safety_grade)

with m7:
    st.metric("Beds", beds)

# ---------------------------------------------------
# READMISSION SUMMARY
# ---------------------------------------------------

st.markdown('<div class="section-title">Readmission Summary</div>', unsafe_allow_html=True)

left, right = st.columns([1.25, 1])

with left:
    if not distribution_df.empty:
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
            title="Readmission Measure Distribution",
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Number of Measures",
            margin=dict(l=18, r=18, t=55, b=18),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(size=14),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No distribution data available.")

with right:
    st.markdown(
        """
        <div class="jh-card">
            <h4 style="margin-top:0;color:#0F172A;">Dashboard Snapshot</h4>
            <p style="margin-bottom:10px;color:#334155;">
                <strong>Readmission distribution:</strong><br>
                1 above / 6 same / 3 below national average
            </p>
            <p style="margin-bottom:10px;color:#334155;">
                <strong>Location:</strong><br>
                Baltimore, Maryland
            </p>
            <p style="margin-bottom:0;color:#334155;">
                <strong>Design focus:</strong> executive-grade healthcare intelligence,
                clear governance, and public-source traceability.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------
# TABS
# ---------------------------------------------------

tabs = st.tabs(
    [
        "Overview",
        "Verified Facts",
        "Interventions",
        "Sources & Methodology",
    ]
)

with tabs[0]:
    st.subheader("Executive Summary")
    st.write(
        "This dashboard presents source-verified public information about readmission, safety, "
        "and institutional context for The Johns Hopkins Hospital."
    )

    st.markdown("### Data Integrity Rules")
    st.markdown(
        """
- Only publicly available source-verified information is included
- Current and historical information are separated
- Historical outcomes are labeled with their original year
- No patient-level data is used
- No unsupported predictive claims are included
"""
    )

with tabs[1]:
    st.subheader("Current Official Metrics")
    current_columns = ["category", "label", "value", "detail", "as_of", "source_url"]
    if not current_df.empty:
        st.dataframe(
            current_df.reindex(columns=current_columns),
            use_container_width=True,
        )
    else:
        st.info("No current metrics available.")

    st.subheader("Historical & Institutional Context")
    historical_columns = ["category", "label", "value", "detail", "as_of", "freshness", "source_url"]
    if not historical_df.empty:
        st.dataframe(
            historical_df.reindex(columns=historical_columns),
            use_container_width=True,
        )
    else:
        st.info("No historical context available.")

with tabs[2]:
    st.subheader("Official Interventions")
    if official_interventions:
        for item in official_interventions:
            with st.expander(item.get("name", "Intervention")):
                st.write(item.get("summary", "No summary available."))
                source_url = item.get("source_url")
                if source_url:
                    st.markdown(f"[Open official source]({source_url})")
    else:
        st.info("No intervention data available.")

with tabs[3]:
    st.subheader("Source Audit")
    if not source_audit_df.empty:
        st.dataframe(
            source_audit_df,
            use_container_width=True,
        )
    else:
        st.info("No source audit rows available.")

    st.subheader("Methodology")
    st.markdown(
        """
1. Identify official public sources (Medicare, CMS, Johns Hopkins, Leapfrog).
2. Extract source-verifiable facts suitable for public portfolio use.
3. Label each fact as current or historical.
4. Present current federal/public quality indicators separately from historical context.
5. Avoid unsupported patient-level predictions or private data.
"""
    )

    st.subheader("Direct Source Links")
    for label, url in SOURCE_PAGES.items():
        st.markdown(f"- [{label}]({url})")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown(
    """
    <div class="footer">
        Johns Hopkins Readmission & Quality Intelligence Dashboard<br>
        Built with Python, Streamlit, Pandas, and Plotly
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(disclaimer)
