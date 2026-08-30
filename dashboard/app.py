# ============================================================
# ICESTREAM - ENTERPRISE DATA ENGINEERING DASHBOARD
# ============================================================

from pathlib import Path
import sys

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="IceStream | Data Intelligence Platform",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = BASE_DIR / "reports"


# ============================================================
# CUSTOM CSS - A1 GRADE UI
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #f5f7fb;
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #101828;
        border-right: 1px solid #25304a;
    }

    section[data-testid="stSidebar"] * {
        color: #e6edf7;
    }

    /* ---------- HEADER ---------- */

    .hero {
        background: linear-gradient(
            135deg,
            #101828 0%,
            #172554 50%,
            #0f766e 100%
        );
        padding: 30px 35px;
        border-radius: 18px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
    }

    .hero-title {
        font-size: 38px;
        font-weight: 800;
        color: white;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #cbd5e1;
        margin-top: 0;
    }

    .status-badge {
        display: inline-block;
        background: rgba(34, 197, 94, 0.15);
        color: #86efac;
        padding: 7px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        margin-top: 12px;
    }

    /* ---------- KPI CARDS ---------- */

    .kpi-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
    }

    .kpi-title {
        color: #64748b;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    .kpi-value {
        color: #0f172a;
        font-size: 30px;
        font-weight: 800;
        margin-top: 8px;
    }

    .kpi-description {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 4px;
    }

    /* ---------- SECTION ---------- */

    .section-title {
        font-size: 24px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 28px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 18px;
    }

    /* ---------- INFO CARDS ---------- */

    .info-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.05);
    }

    .info-title {
        font-size: 14px;
        font-weight: 700;
        color: #475569;
        margin-bottom: 8px;
    }

    .info-value {
        font-size: 25px;
        font-weight: 800;
        color: #0f172a;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        padding: 30px 0 10px 0;
    }

    /* ---------- STREAMLIT ELEMENTS ---------- */

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5e7eb;
        padding: 15px;
        border-radius: 14px;
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

@st.cache_data
def load_csv(path):
    """Load CSV safely."""
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def find_report(filename):
    """Find report file."""
    return REPORTS_DIR / filename


# ============================================================
# LOAD DATA
# ============================================================

sensor = load_csv(PROCESSED_DIR / "sensor_readings.csv")
features = load_csv(PROCESSED_DIR / "sensor_features.csv")
assets = load_csv(PROCESSED_DIR / "assets.csv")
inventory = load_csv(PROCESSED_DIR / "inventory.csv")
maintenance = load_csv(PROCESSED_DIR / "maintenance_records.csv")
shipments = load_csv(PROCESSED_DIR / "shipments.csv")

anomaly_results = load_csv(
    find_report("anomaly_detection_results.csv")
)

anomaly_summary = load_csv(
    find_report("asset_anomaly_summary.csv")
)

risk_results = load_csv(
    find_report("maintenance_risk_scoring.csv")
)

pipeline_health = load_csv(
    find_report("pipeline_health_report.csv")
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;padding:10px 0 25px 0;">
            <div style="font-size:48px;">❄️</div>
            <h2 style="margin:0;">IceStream</h2>
            <p style="color:#94a3b8;">Data Intelligence Platform</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "Executive Overview",
            "Sensor Intelligence",
            "Anomaly Detection",
            "Predictive Maintenance",
            "Asset Risk",
            "Pipeline Health"
        ]
    )

    st.markdown("---")

    st.markdown("### Platform")

    st.caption("Real-time logistics analytics")
    st.caption("Predictive maintenance")
    st.caption("Data quality monitoring")
    st.caption("Machine learning anomaly detection")

    st.markdown("---")

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            ❄️ IceStream Data Intelligence
        </div>

        <div class="hero-subtitle">
            Closed-loop logistics monitoring, anomaly detection,
            predictive maintenance and data quality intelligence.
        </div>

        <div class="status-badge">
            ● PLATFORM OPERATIONAL
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">High-level operational intelligence across the IceStream platform.</div>',
        unsafe_allow_html=True
    )

    total_assets = len(assets)

    total_sensor_records = (
        len(sensor)
        if not sensor.empty
        else 0
    )

    total_maintenance = len(maintenance)

    total_shipments = len(shipments)

    high_risk_assets = 0

    if not risk_results.empty and "risk_level" in risk_results.columns:
        high_risk_assets = int(
            (risk_results["risk_level"] == "HIGH").sum()
        )

    anomalies = 0

    if not anomaly_results.empty:
        if "is_anomaly" in anomaly_results.columns:
            anomalies = int(
                anomaly_results["is_anomaly"].sum()
            )
        elif "anomaly" in anomaly_results.columns:
            anomalies = int(
                anomaly_results["anomaly"].sum()
            )

    cols = st.columns(5)

    kpis = [
        ("TOTAL ASSETS", total_assets, "Registered logistics assets"),
        ("SENSOR RECORDS", f"{total_sensor_records:,}", "Processed telemetry"),
        ("ANOMALIES", f"{anomalies:,}", "ML detected events"),
        ("HIGH-RISK ASSETS", high_risk_assets, "Immediate attention"),
        ("MAINTENANCE EVENTS", total_maintenance, "Historical maintenance"),
    ]

    for col, (title, value, description) in zip(cols, kpis):

        with col:

            st.markdown(
                f"""
                <div class="kpi-card">

                    <div class="kpi-title">
                        {title}
                    </div>

                    <div class="kpi-value">
                        {value}
                    </div>

                    <div class="kpi-description">
                        {description}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # Risk distribution
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Operational Risk Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        if not features.empty and "risk_level" in features.columns:

            risk_counts = (
                features["risk_level"]
                .value_counts()
                .reset_index()
            )

            risk_counts.columns = [
                "risk_level",
                "count"
            ]

            fig = px.pie(
                risk_counts,
                names="risk_level",
                values="count",
                hole=0.55,
                title="Sensor Risk Distribution"
            )

            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=60, b=20),
                legend_title_text="Risk"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with col2:

        if not risk_results.empty:

            if "risk_level" in risk_results.columns:

                counts = (
                    risk_results["risk_level"]
                    .value_counts()
                    .reset_index()
                )

                counts.columns = [
                    "risk_level",
                    "count"
                ]

                fig = px.bar(
                    counts,
                    x="risk_level",
                    y="count",
                    title="Asset Maintenance Risk",
                    text="count"
                )

                fig.update_layout(
                    height=400,
                    margin=dict(l=20, r=20, t=60, b=20)
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

    # --------------------------------------------------------
    # Asset status
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Asset Fleet Status</div>',
        unsafe_allow_html=True
    )

    if not assets.empty and "status" in assets.columns:

        status_counts = (
            assets["status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = [
            "status",
            "count"
        ]

        fig = px.bar(
            status_counts,
            x="status",
            y="count",
            text="count",
            title="Current Asset Status"
        )

        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# SENSOR INTELLIGENCE
# ============================================================

elif page == "Sensor Intelligence":

    st.markdown(
        '<div class="section-title">Sensor Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Telemetry behaviour and operating conditions.</div>',
        unsafe_allow_html=True
    )

    if not features.empty:

        col1, col2, col3 = st.columns(3)

        temperature = (
            features["temperature"]
            if "temperature" in features.columns
            else pd.Series(dtype=float)
        )

        vibration = (
            features["vibration"]
            if "vibration" in features.columns
            else pd.Series(dtype=float)
        )

        with col1:
            st.metric(
                "Average Temperature",
                f"{temperature.mean():.2f}"
            )

        with col2:
            st.metric(
                "Maximum Temperature",
                f"{temperature.max():.2f}"
            )

        with col3:
            st.metric(
                "Average Vibration",
                f"{vibration.mean():.2f}"
            )

        col1, col2 = st.columns(2)

        with col1:

            if not temperature.empty:

                fig = px.histogram(
                    features,
                    x="temperature",
                    nbins=40,
                    title="Temperature Distribution"
                )

                fig.update_layout(
                    height=400
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        with col2:

            if not vibration.empty:

                fig = px.histogram(
                    features,
                    x="vibration",
                    nbins=40,
                    title="Vibration Distribution"
                )

                fig.update_layout(
                    height=400
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        # Scatter

        if (
            "temperature" in features.columns
            and "vibration" in features.columns
        ):

            fig = px.scatter(
                features,
                x="temperature",
                y="vibration",
                color="risk_level"
                if "risk_level" in features.columns
                else None,
                hover_data=["asset_id"]
                if "asset_id" in features.columns
                else None,
                title="Temperature vs Vibration"
            )

            fig.update_layout(
                height=500
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# ============================================================
# ANOMALY DETECTION
# ============================================================

elif page == "Anomaly Detection":

    st.markdown(
        '<div class="section-title">Machine Learning Anomaly Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Isolation-based anomaly analysis of sensor telemetry.</div>',
        unsafe_allow_html=True
    )

    if not anomaly_results.empty:

        anomaly_column = None

        for column in [
            "is_anomaly",
            "anomaly",
            "anomaly_flag"
        ]:

            if column in anomaly_results.columns:
                anomaly_column = column
                break

        if anomaly_column:

            total = len(anomaly_results)

            anomaly_count = int(
                anomaly_results[anomaly_column].sum()
            )

            normal_count = total - anomaly_count

            anomaly_rate = (
                anomaly_count / total * 100
                if total
                else 0
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Total Records",
                    f"{total:,}"
                )

            with c2:
                st.metric(
                    "Anomalous Records",
                    f"{anomaly_count:,}"
                )

            with c3:
                st.metric(
                    "Anomaly Rate",
                    f"{anomaly_rate:.2f}%"
                )

            chart_data = pd.DataFrame(
                {
                    "Status": [
                        "Normal",
                        "Anomalous"
                    ],
                    "Records": [
                        normal_count,
                        anomaly_count
                    ]
                }
            )

            fig = px.pie(
                chart_data,
                names="Status",
                values="Records",
                hole=0.55,
                title="Normal vs Anomalous Records"
            )

            fig.update_layout(
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.markdown("### Anomaly Results")

        st.dataframe(
            anomaly_results.head(100),
            use_container_width=True,
            height=400
        )


# ============================================================
# PREDICTIVE MAINTENANCE
# ============================================================

elif page == "Predictive Maintenance":

    st.markdown(
        '<div class="section-title">Predictive Maintenance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Prioritize assets before operational failure occurs.</div>',
        unsafe_allow_html=True
    )

    predictive = load_csv(
        find_report("predictive_maintenance_results.csv")
    )

    if not predictive.empty:

        if "predicted_risk" in predictive.columns:

            distribution = (
                predictive["predicted_risk"]
                .value_counts()
                .reset_index()
            )

            distribution.columns = [
                "risk",
                "count"
            ]

            fig = px.bar(
                distribution,
                x="risk",
                y="count",
                text="count",
                title="Predicted Maintenance Risk"
            )

            fig.update_layout(
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.markdown("### Highest Priority Assets")

        st.dataframe(
            predictive.head(20),
            use_container_width=True,
            height=450
        )

    else:

        st.warning(
            "Predictive maintenance report is not available yet."
        )


# ============================================================
# ASSET RISK
# ============================================================

elif page == "Asset Risk":

    st.markdown(
        '<div class="section-title">Asset Risk Scoring</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Operational risk ranking based on sensor behaviour and anomalies.</div>',
        unsafe_allow_html=True
    )

    if not risk_results.empty:

        if "risk_score" in risk_results.columns:

            top_risk = (
                risk_results
                .sort_values(
                    "risk_score",
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                top_risk.sort_values(
                    "risk_score"
                ),
                x="risk_score",
                y="asset_id",
                orientation="h",
                text="risk_score",
                title="Top 10 Highest-Risk Assets"
            )

            fig.update_layout(
                height=500
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.markdown("### Maintenance Priorities")

        st.dataframe(
            risk_results,
            use_container_width=True,
            height=500
        )


# ============================================================
# PIPELINE HEALTH
# ============================================================

elif page == "Pipeline Health":

    st.markdown(
        '<div class="section-title">Pipeline Health</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Data engineering pipeline quality and reliability monitoring.</div>',
        unsafe_allow_html=True
    )

    if not pipeline_health.empty:

        if "status" in pipeline_health.columns:

            passed = int(
                (
                    pipeline_health["status"]
                    .astype(str)
                    .str.upper()
                    == "PASSED"
                ).sum()
            )

            failed = int(
                (
                    pipeline_health["status"]
                    .astype(str)
                    .str.upper()
                    == "FAILED"
                ).sum()
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Datasets Checked",
                    len(pipeline_health)
                )

            with c2:
                st.metric(
                    "Passed",
                    passed
                )

            with c3:
                st.metric(
                    "Failed",
                    failed
                )

        st.markdown("### Dataset Validation")

        st.dataframe(
            pipeline_health,
            use_container_width=True,
            height=500
        )

        if "status" in pipeline_health.columns:

            status_counts = (
                pipeline_health["status"]
                .value_counts()
                .reset_index()
            )

            status_counts.columns = [
                "status",
                "count"
            ]

            fig = px.pie(
                status_counts,
                names="status",
                values="count",
                hole=0.55,
                title="Pipeline Dataset Health"
            )

            fig.update_layout(
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:

        st.warning(
            "Pipeline health report is not available."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        ❄️ IceStream Data Intelligence Platform
        &nbsp; | &nbsp;
        Data Engineering • Machine Learning • Predictive Analytics
        &nbsp; | &nbsp;
        Production Dashboard
    </div>
    """,
    unsafe_allow_html=True
)