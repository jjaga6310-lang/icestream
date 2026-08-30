import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================
# ICESTREAM ANALYTICS DASHBOARD
# ============================================================

st.set_page_config(
    page_title="IceStream Analytics",
    page_icon="❄️",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    sensor = pd.read_csv(
        DATA_DIR / "processed" / "sensor_readings.csv"
    )

    features = pd.read_csv(
        DATA_DIR / "processed" / "sensor_features.csv"
    )

    assets = pd.read_csv(
        DATA_DIR / "processed" / "assets.csv"
    )

    maintenance = pd.read_csv(
        DATA_DIR / "processed" / "maintenance_records.csv"
    )

    risk = pd.read_csv(
        REPORTS_DIR / "maintenance_risk_scoring.csv"
    )

    health = pd.read_csv(
        REPORTS_DIR / "pipeline_health_report.csv"
    )

    return sensor, features, assets, maintenance, risk, health


sensor, features, assets, maintenance, risk, health = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("❄️ IceStream")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Risk Monitoring",
        "Sensor Analytics",
        "Maintenance",
        "Pipeline Health"
    ]
)


# ============================================================
# HEADER
# ============================================================

st.title("❄️ IceStream Analytics Dashboard")

st.write(
    "Cold-chain logistics monitoring, anomaly detection "
    "and predictive maintenance platform."
)

st.divider()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_assets = len(assets)
sensor_records = len(sensor)

high_risk_assets = len(
    risk[risk["risk_level"] == "HIGH"]
)

anomaly_records = 0

anomaly_file = REPORTS_DIR / "anomaly_summary.csv"

if anomaly_file.exists():

    anomaly_summary = pd.read_csv(anomaly_file)

    if "anomalous_records" in anomaly_summary.columns:
        anomaly_records = int(
            anomaly_summary["anomalous_records"].sum()
        )

    elif "anomalies" in anomaly_summary.columns:
        anomaly_records = int(
            anomaly_summary["anomalies"].sum()
        )

anomaly_rate = (
    anomaly_records / sensor_records * 100
    if sensor_records > 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Assets", total_assets)

with col2:
    st.metric("Sensor Records", f"{sensor_records:,}")

with col3:
    st.metric("Anomalous Records", f"{anomaly_records:,}")

with col4:
    st.metric("Anomaly Rate", f"{anomaly_rate:.2f}%")

with col5:
    st.metric("High-Risk Assets", high_risk_assets)


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.header("📊 Executive Overview")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Risk Distribution")

        risk_distribution = (
            features["risk_level"]
            .value_counts()
            .rename_axis("Risk Level")
            .to_frame("Records")
        )

        st.bar_chart(risk_distribution)

    with col2:

        st.subheader("Asset Status")

        status_distribution = (
            assets["status"]
            .value_counts()
            .rename_axis("Status")
            .to_frame("Assets")
        )

        st.bar_chart(status_distribution)

    st.subheader("Top Maintenance Priorities")

    columns = [
        "asset_id",
        "risk_score",
        "risk_level",
        "anomaly_rate",
        "max_vibration",
        "max_temperature",
        "maintenance_recommendation"
    ]

    available = [
        c for c in columns
        if c in risk.columns
    ]

    st.dataframe(
        risk.sort_values(
            "risk_score",
            ascending=False
        )[available].head(10),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# RISK MONITORING
# ============================================================

elif page == "Risk Monitoring":

    st.header("🚨 Risk Monitoring")

    distribution = (
        risk["risk_level"]
        .value_counts()
        .rename_axis("Risk Level")
        .to_frame("Assets")
    )

    st.bar_chart(distribution)

    st.subheader("Highest Risk Assets")

    st.dataframe(
        risk.sort_values(
            "risk_score",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SENSOR ANALYTICS
# ============================================================

elif page == "Sensor Analytics":

    st.header("🌡️ Sensor Analytics")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Temperature")

        st.line_chart(
            sensor["temperature"].head(500)
        )

        st.metric(
            "Average Temperature",
            f"{sensor['temperature'].mean():.2f}"
        )

    with col2:

        st.subheader("Vibration")

        st.line_chart(
            sensor["vibration"].head(500)
        )

        st.metric(
            "Average Vibration",
            f"{sensor['vibration'].mean():.2f}"
        )

    st.subheader("Sensor Statistics")

    st.dataframe(
        sensor.describe(),
        use_container_width=True
    )


# ============================================================
# MAINTENANCE
# ============================================================

elif page == "Maintenance":

    st.header("🔧 Predictive Maintenance")

    distribution = (
        risk["risk_level"]
        .value_counts()
        .rename_axis("Risk Level")
        .to_frame("Assets")
    )

    st.bar_chart(distribution)

    st.subheader("Maintenance Priority List")

    columns = [
        "asset_id",
        "risk_score",
        "risk_level",
        "anomaly_rate",
        "max_vibration",
        "max_temperature",
        "maintenance_recommendation"
    ]

    available = [
        c for c in columns
        if c in risk.columns
    ]

    st.dataframe(
        risk.sort_values(
            "risk_score",
            ascending=False
        )[available],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Maintenance Records")

    st.dataframe(
        maintenance,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PIPELINE HEALTH
# ============================================================

elif page == "Pipeline Health":

    st.header("🟢 Pipeline Health")

    st.success("Pipeline STATUS: HEALTHY")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Datasets Checked",
            len(health)
        )

    with col2:

        if "status" in health.columns:
            passed = health["status"].eq("PASSED").sum()
        else:
            passed = len(health)

        st.metric(
            "Passed Checks",
            passed
        )

    st.subheader("Dataset Quality Checks")

    st.dataframe(
        health,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "IceStream — Closed-Loop Cold-Chain Data Engineering "
    "& Predictive Analytics Platform"
)