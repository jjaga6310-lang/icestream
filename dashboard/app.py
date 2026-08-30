# ============================================================
# ICESTREAM - OPERATIONS INTELLIGENCE DASHBOARD
# Complete Streamlit Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="IceStream Operations Intelligence",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT PATHS
# ============================================================

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
REPORTS_DIR = PROJECT_DIR / "reports"


# ============================================================
# GLOBAL CSS
# IMPORTANT: CSS ONLY - NO HTML DISPLAY CONTENT
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f4f7fb;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background-color: #0b1220;
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    [data-testid="stSidebar"] .stCaption {
        color: #94a3b8 !important;
    }

    /* SIDEBAR BRAND */

    [data-testid="stSidebar"] h1 {
        color: #ffffff !important;
        font-size: 30px !important;
        font-weight: 900 !important;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #e2e8f0 !important;
        font-weight: 800 !important;
    }

    /* MAIN HEADINGS */

    h1 {
        color: #0f172a !important;
        font-weight: 900 !important;
    }

    h2 {
        color: #1d4ed8 !important;
        font-weight: 850 !important;
    }

    h3 {
        color: #1e3a8a !important;
        font-weight: 800 !important;
    }

    /* METRICS */

    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #dbe4ef;
        border-radius: 14px;
        padding: 17px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.06);
    }

    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 900 !important;
    }

    /* BUTTONS */

    .stButton > button {
        border-radius: 9px;
        font-weight: 800;
    }

    /* DATAFRAME */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
    }

    /* ALERTS */

    .stAlert {
        border-radius: 10px;
    }

    hr {
        border-color: #dbe4ef;
    }

    /* DATE INPUT TEXT */
    
    [data-testid="stSidebar"] input {
        color: #111827 !important;
        background-color: #ffffff !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="input"] {
        background-color: #ffffff !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] {
        color: #111827 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADER
# ============================================================

@st.cache_data(ttl=60)
def load_csv(filename):

    path = REPORTS_DIR / filename

    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


# ============================================================
# LOAD REPORTS
# ============================================================

anomaly = load_csv(
    "anomaly_detection_results.csv"
)

maintenance = load_csv(
    "maintenance_risk_scoring.csv"
)

pipeline = load_csv(
    "pipeline_health_report.csv"
)

anomaly_summary = load_csv(
    "anomaly_summary.csv"
)

asset_anomaly = load_csv(
    "asset_anomaly_summary.csv"
)

asset_risk = load_csv(
    "asset_risk_analysis.csv"
)

sensor_summary = load_csv(
    "sensor_summary_statistics.csv"
)


# ============================================================
# DATA PREPARATION
# ============================================================

if not anomaly.empty:

    if "recorded_at" in anomaly.columns:

        anomaly["recorded_at"] = pd.to_datetime(
            anomaly["recorded_at"],
            errors="coerce"
        )

    anomaly_numeric = [
        "temperature",
        "vibration",
        "pressure",
        "humidity",
        "fuel_level",
        "temperature_rolling_avg",
        "vibration_rolling_avg",
        "temperature_deviation",
        "vibration_deviation",
        "temperature_anomaly",
        "vibration_anomaly",
        "risk_score",
        "ml_anomaly",
        "anomaly_score"
    ]

    for col in anomaly_numeric:

        if col in anomaly.columns:

            anomaly[col] = pd.to_numeric(
                anomaly[col],
                errors="coerce"
            )


if not maintenance.empty:

    maintenance_numeric = [
        "avg_temperature",
        "max_temperature",
        "avg_vibration",
        "max_vibration",
        "avg_pressure",
        "avg_humidity",
        "avg_fuel_level",
        "sensor_records",
        "anomaly_count",
        "average_anomaly_score",
        "anomaly_rate",
        "anomaly_component",
        "vibration_component",
        "temperature_component",
        "avg_vibration_component",
        "risk_score"
    ]

    for col in maintenance_numeric:

        if col in maintenance.columns:

            maintenance[col] = pd.to_numeric(
                maintenance[col],
                errors="coerce"
            )


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_number(value, default=0):

    try:

        if pd.isna(value):
            return default

        return float(value)

    except Exception:

        return default


def number_format(value):

    try:
        return f"{int(value):,}"

    except Exception:
        return "0"


def decimal_format(value):

    try:
        return f"{float(value):.1f}"

    except Exception:
        return "0.0"


def percentage_format(value):

    try:
        return f"{float(value):.1f}%"

    except Exception:
        return "0.0%"


def make_chart(fig, title, height=420):

    fig.update_layout(

        title=dict(
            text=title,
            x=0.02,
            font=dict(
                size=18,
                color="#0f172a"
            )
        ),

        height=height,

        margin=dict(
            l=35,
            r=30,
            t=65,
            b=35
        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        font=dict(
            family="Arial",
            color="#334155"
        ),

        legend=dict(
            bgcolor="rgba(255,255,255,0)"
        )
    )

    fig.update_xaxes(
        showgrid=False
    )

    fig.update_yaxes(
        gridcolor="#e5e7eb",
        zeroline=False
    )

    return fig


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # ========================================================
    # BRAND
    # ========================================================

    st.title("❄️ ICESTREAM")

    st.caption(
        "OPERATIONS INTELLIGENCE"
    )

    st.divider()

    # ========================================================
    # NAVIGATION
    # ========================================================

    st.subheader("NAVIGATION")

    page = st.radio(
        "Dashboard",
        [
            "Command Center",
            "Executive Risk",
            "Asset Intelligence",
            "Asset Drill-Down",
            "Anomaly Detection",
            "Predictive Maintenance",
            "Data Health"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    # ========================================================
    # DASHBOARD CONTROL
    # ========================================================

    st.subheader("DASHBOARD CONTROL")

    if st.button(
        "🔄 Refresh Data",
        use_container_width=True
    ):

        st.cache_data.clear()
        st.rerun()

    st.divider()

    # ========================================================
    # FILTERS
    # ========================================================

    st.subheader("FILTERS")

    if "asset_id" in anomaly.columns:

        asset_options = sorted(
            anomaly[
                "asset_id"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    else:

        asset_options = []

    selected_assets = st.multiselect(
        "Assets",
        asset_options,
        placeholder="All assets"
    )

    if "risk_level" in maintenance.columns:

        risk_options = sorted(
            maintenance[
                "risk_level"
            ]
            .dropna()
            .astype(str)
            .str.upper()
            .unique()
            .tolist()
        )

    else:

        risk_options = []

    selected_risks = st.multiselect(
        "Risk Level",
        risk_options,
        placeholder="All risk levels"
    )

    # ========================================================
    # OBSERVATION PERIOD
    # ========================================================

    st.subheader("📅 OBSERVATION PERIOD")

    selected_dates = None

    if "recorded_at" in anomaly.columns:

        valid_dates = (
            anomaly[
                "recorded_at"
            ]
            .dropna()
        )

        if not valid_dates.empty:

            minimum_date = valid_dates.min().date()
            maximum_date = valid_dates.max().date()

            selected_dates = st.date_input(
                "Date range",
                value=(
                    minimum_date,
                    maximum_date
                ),
                min_value=minimum_date,
                max_value=maximum_date,
                format="DD/MM/YYYY"
            )

    st.divider()

    # ========================================================
    # SYSTEM HEALTH
    # ========================================================

    st.subheader("SYSTEM HEALTH")

    analytics_ready = not anomaly.empty

    ml_ready = (
        not anomaly.empty
        and "ml_anomaly" in anomaly.columns
        and "anomaly_score" in anomaly.columns
    )

    maintenance_ready = (
        not maintenance.empty
        and "risk_score" in maintenance.columns
    )

    pipeline_ready = not pipeline.empty

    if analytics_ready:
        st.success("● Analytics Engine — READY")
    else:
        st.error("● Analytics Engine — CHECK")

    if ml_ready:
        st.success("● ML Detection — READY")
    else:
        st.error("● ML Detection — CHECK")

    if maintenance_ready:
        st.success("● Maintenance Engine — READY")
    else:
        st.error("● Maintenance Engine — CHECK")

    if pipeline_ready:
        st.success("● Data Pipeline — READY")
    else:
        st.error("● Data Pipeline — CHECK")


# ============================================================
# FILTER DATA
# ============================================================

filtered_anomaly = anomaly.copy()

filtered_maintenance = maintenance.copy()


# ============================================================
# ASSET FILTER
# ============================================================

if selected_assets:

    if "asset_id" in filtered_anomaly.columns:

        filtered_anomaly = filtered_anomaly[
            filtered_anomaly[
                "asset_id"
            ]
            .astype(str)
            .isin(selected_assets)
        ]

    if "asset_id" in filtered_maintenance.columns:

        filtered_maintenance = filtered_maintenance[
            filtered_maintenance[
                "asset_id"
            ]
            .astype(str)
            .isin(selected_assets)
        ]


# ============================================================
# RISK FILTER
# ============================================================

if selected_risks:

    if "risk_level" in filtered_maintenance.columns:

        filtered_maintenance = filtered_maintenance[
            filtered_maintenance[
                "risk_level"
            ]
            .astype(str)
            .str.upper()
            .isin(selected_risks)
        ]


# ============================================================
# DATE FILTER
# ============================================================

if (
    selected_dates
    and isinstance(selected_dates, tuple)
    and len(selected_dates) == 2
    and "recorded_at" in filtered_anomaly.columns
):

    start_date = pd.Timestamp(
        selected_dates[0]
    )

    end_date = (
        pd.Timestamp(
            selected_dates[1]
        )
        + pd.Timedelta(days=1)
    )

    filtered_anomaly = filtered_anomaly[
        (
            filtered_anomaly[
                "recorded_at"
            ] >= start_date
        )
        &
        (
            filtered_anomaly[
                "recorded_at"
            ] < end_date
        )
    ]


# ============================================================
# GLOBAL KPIs
# ============================================================

if "asset_id" in filtered_anomaly.columns:

    monitored_assets = (
        filtered_anomaly[
            "asset_id"
        ]
        .nunique()
    )

else:

    monitored_assets = len(
        filtered_maintenance
    )


sensor_records = len(
    filtered_anomaly
)


if "ml_anomaly" in filtered_anomaly.columns:

    total_anomalies = int(
        filtered_anomaly[
            "ml_anomaly"
        ]
        .fillna(0)
        .sum()
    )

else:

    total_anomalies = 0


if sensor_records > 0:

    anomaly_rate = (
        total_anomalies
        /
        sensor_records
        *
        100
    )

else:

    anomaly_rate = 0


if (
    "risk_score" in filtered_maintenance.columns
    and not filtered_maintenance.empty
):

    average_risk = (
        pd.to_numeric(
            filtered_maintenance[
                "risk_score"
            ],
            errors="coerce"
        )
        .mean()
    )

    if pd.isna(average_risk):
        average_risk = 0

else:

    average_risk = 0


high_risk = 0
medium_risk = 0
low_risk = 0


if "risk_level" in filtered_maintenance.columns:

    risk_values = (
        filtered_maintenance[
            "risk_level"
        ]
        .astype(str)
        .str.upper()
    )

    high_risk = int(
        (
            risk_values == "HIGH"
        ).sum()
    )

    medium_risk = int(
        (
            risk_values == "MEDIUM"
        ).sum()
    )

    low_risk = int(
        (
            risk_values == "LOW"
        ).sum()
    )


# ============================================================
# PAGE 1 - COMMAND CENTER
# ============================================================

if page == "Command Center":

    st.title(
        "❄️ IceStream Operations Command Center"
    )

    st.write(
        "Real-time operational intelligence for fleet "
        "monitoring, anomaly detection and predictive maintenance."
    )

    st.divider()

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.metric(
            "MONITORED ASSETS",
            number_format(monitored_assets)
        )

    with k2:
        st.metric(
            "SENSOR OBSERVATIONS",
            number_format(sensor_records)
        )

    with k3:
        st.metric(
            "ANOMALIES",
            number_format(total_anomalies)
        )

    with k4:
        st.metric(
            "ANOMALY RATE",
            percentage_format(anomaly_rate)
        )

    with k5:
        st.metric(
            "AVERAGE RISK",
            decimal_format(average_risk)
        )

    st.divider()

    left, right = st.columns([1.55, 1])

    with left:

        st.subheader("Anomaly Activity")

        if {
            "recorded_at",
            "ml_anomaly"
        }.issubset(
            filtered_anomaly.columns
        ):

            temp = filtered_anomaly.copy()

            temp["date"] = (
                temp[
                    "recorded_at"
                ]
                .dt.date
            )

            daily = (
                temp
                .groupby("date")[
                    "ml_anomaly"
                ]
                .sum()
                .reset_index()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=daily["date"],
                    y=daily["ml_anomaly"],
                    mode="lines+markers",
                    fill="tozeroy",
                    name="Anomalies"
                )
            )

            fig = make_chart(
                fig,
                "Daily anomaly volume",
                420
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Anomaly trend data unavailable."
            )

    with right:

        st.subheader("Fleet Risk Profile")

        fig = go.Figure()

        fig.add_trace(
            go.Pie(
                labels=[
                    "HIGH",
                    "MEDIUM",
                    "LOW"
                ],
                values=[
                    high_risk,
                    medium_risk,
                    low_risk
                ],
                hole=0.60,
                textinfo="label+value"
            )
        )

        fig.update_layout(
            height=420,
            margin=dict(
                l=10,
                r=10,
                t=25,
                b=10
            ),
            paper_bgcolor="#ffffff"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("🚨 Priority Assets")

    if {
        "asset_id",
        "risk_score"
    }.issubset(
        filtered_maintenance.columns
    ):

        priority_cols = [
            c for c in [
                "asset_id",
                "risk_score",
                "risk_level",
                "anomaly_count",
                "anomaly_rate",
                "maintenance_recommendation"
            ]
            if c in filtered_maintenance.columns
        ]

        priority = (
            filtered_maintenance[
                priority_cols
            ]
            .sort_values(
                "risk_score",
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            priority,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PAGE 2 - EXECUTIVE RISK
# ============================================================

elif page == "Executive Risk":

    st.title(
        "Executive Risk Intelligence"
    )

    st.write(
        "Management-level overview of fleet exposure, "
        "asset risk ranking and operational priorities."
    )

    st.divider()

    # ========================================================
    # EXECUTIVE CALCULATIONS
    # ========================================================

    if "asset_id" in filtered_maintenance.columns:

        total_assets = (
            filtered_maintenance[
                "asset_id"
            ]
            .nunique()
        )

    else:

        total_assets = len(
            filtered_maintenance
        )

    if "risk_score" in filtered_maintenance.columns:

        risk_values_numeric = pd.to_numeric(
            filtered_maintenance[
                "risk_score"
            ],
            errors="coerce"
        ).dropna()

        if not risk_values_numeric.empty:

            average_risk = (
                risk_values_numeric.mean()
            )

        else:

            average_risk = 0

    else:

        average_risk = 0

    if "risk_level" in filtered_maintenance.columns:

        risk_levels = (
            filtered_maintenance[
                "risk_level"
            ]
            .astype(str)
            .str.upper()
        )

        high_risk = int(
            (
                risk_levels == "HIGH"
            ).sum()
        )

        medium_risk = int(
            (
                risk_levels == "MEDIUM"
            ).sum()
        )

        low_risk = int(
            (
                risk_levels == "LOW"
            ).sum()
        )

    else:

        high_risk = 0
        medium_risk = 0
        low_risk = 0

    high_percentage = (
        high_risk
        /
        total_assets
        *
        100
        if total_assets > 0
        else 0
    )

    # ========================================================
    # EXECUTIVE KPIs
    # ========================================================

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.metric(
            "FLEET ASSETS",
            number_format(total_assets)
        )

    with k2:

        st.metric(
            "AVERAGE RISK",
            decimal_format(average_risk)
        )

    with k3:

        st.metric(
            "HIGH-RISK EXPOSURE",
            percentage_format(high_percentage)
        )

    with k4:

        st.metric(
            "ANOMALY EVENTS",
            number_format(total_anomalies)
        )

    st.divider()

    # ========================================================
    # MANAGEMENT INSIGHTS
    # ========================================================

    st.subheader("Management Insights")

    insight1, insight2, insight3 = st.columns(3)

    # ========================================================
    # HIGHEST RISK ASSET
    # ========================================================

    with insight1:

        st.markdown("### Highest Risk Asset")

        if (
            not filtered_maintenance.empty
            and "risk_score"
            in filtered_maintenance.columns
        ):

            risk_data = (
                filtered_maintenance
                .copy()
            )

            risk_data["risk_score"] = pd.to_numeric(
                risk_data["risk_score"],
                errors="coerce"
            )

            risk_data = risk_data.dropna(
                subset=["risk_score"]
            )

            if not risk_data.empty:

                highest = (
                    risk_data
                    .sort_values(
                        "risk_score",
                        ascending=False
                    )
                    .iloc[0]
                )

                highest_asset = str(
                    highest.get(
                        "asset_id",
                        "Unknown"
                    )
                )

                highest_score = safe_number(
                    highest["risk_score"]
                )

                highest_level = str(
                    highest.get(
                        "risk_level",
                        "UNKNOWN"
                    )
                ).upper()

                st.info(
                    "Asset: " + highest_asset
                )

                st.metric(
                    "Risk Score",
                    f"{highest_score:.1f}"
                )

                st.write(
                    "Risk Level: "
                    + highest_level
                )

            else:

                st.info(
                    "No valid risk score available."
                )

        else:

            st.info(
                "Risk information unavailable."
            )

    # ========================================================
    # MOST ANOMALOUS ASSET
    # ========================================================

    with insight2:

        st.markdown("### Most Anomalous Asset")

        if {
            "asset_id",
            "ml_anomaly"
        }.issubset(
            filtered_anomaly.columns
        ):

            anomaly_by_asset = (
                filtered_anomaly
                .groupby(
                    "asset_id"
                )[
                    "ml_anomaly"
                ]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            if not anomaly_by_asset.empty:

                top_asset = str(
                    anomaly_by_asset.index[0]
                )

                top_count = int(
                    anomaly_by_asset.iloc[0]
                )

                st.warning(
                    "Asset: " + top_asset
                )

                st.metric(
                    "Detected Anomalies",
                    f"{top_count:,}"
                )

                if top_count > 0:

                    st.write(
                        "Highest concentration of "
                        "detected anomaly events."
                    )

                else:

                    st.write(
                        "No significant anomaly concentration."
                    )

            else:

                st.success(
                    "No anomaly concentration detected."
                )

        else:

            st.info(
                "Anomaly information unavailable."
            )

    # ========================================================
    # FLEET HEALTH
    # ========================================================

    with insight3:

        st.markdown("### Fleet Health")

        if average_risk >= 70:

            st.error(
                "CRITICAL"
            )

            st.metric(
                "Average Risk",
                f"{average_risk:.1f}"
            )

            st.write(
                "Immediate management attention "
                "and maintenance prioritization required."
            )

        elif average_risk >= 40:

            st.warning(
                "ATTENTION REQUIRED"
            )

            st.metric(
                "Average Risk",
                f"{average_risk:.1f}"
            )

            st.write(
                "Several assets require monitoring "
                "and planned maintenance."
            )

        else:

            st.success(
                "STABLE"
            )

            st.metric(
                "Average Risk",
                f"{average_risk:.1f}"
            )

            st.write(
                "Fleet risk is currently within "
                "a manageable operating range."
            )

    st.divider()

    # ========================================================
    # RISK CLASSIFICATION + TOP ASSETS
    # ========================================================

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("Risk Classification")

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=[
                    "HIGH",
                    "MEDIUM",
                    "LOW"
                ],
                y=[
                    high_risk,
                    medium_risk,
                    low_risk
                ],
                text=[
                    high_risk,
                    medium_risk,
                    low_risk
                ],
                textposition="outside",
                name="Assets"
            )
        )

        fig = make_chart(
            fig,
            "Fleet Risk Classification",
            400
        )

        fig.update_yaxes(
            title="Number of Assets"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        st.subheader("Top Risk Assets")

        if {
            "asset_id",
            "risk_score"
        }.issubset(
            filtered_maintenance.columns
        ):

            top = (
                filtered_maintenance[
                    [
                        "asset_id",
                        "risk_score"
                    ]
                ]
                .copy()
            )

            top["risk_score"] = pd.to_numeric(
                top["risk_score"],
                errors="coerce"
            )

            top = (
                top
                .dropna(
                    subset=["risk_score"]
                )
                .sort_values(
                    "risk_score",
                    ascending=False
                )
                .head(10)
                .sort_values(
                    "risk_score"
                )
            )

            if not top.empty:

                fig = go.Figure()

                fig.add_trace(
                    go.Bar(
                        x=top[
                            "risk_score"
                        ],
                        y=top[
                            "asset_id"
                        ].astype(str),
                        orientation="h",
                        text=top[
                            "risk_score"
                        ].round(1),
                        textposition="outside",
                        name="Risk Score"
                    )
                )

                chart_max = max(
                    100,
                    float(
                        top[
                            "risk_score"
                        ].max()
                    ) * 1.15
                )

                fig = make_chart(
                    fig,
                    "Highest Risk Assets",
                    400
                )

                fig.update_xaxes(
                    title="Risk Score",
                    range=[
                        0,
                        chart_max
                    ]
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info(
                    "No asset risk data available."
                )

        else:

            st.info(
                "Asset risk ranking unavailable."
            )

    st.divider()

    # ========================================================
    # EXECUTIVE PRIORITY REGISTER
    # ========================================================

    st.subheader(
        "Executive Priority Register"
    )

    if (
        "asset_id"
        in filtered_maintenance.columns
        and
        "risk_score"
        in filtered_maintenance.columns
    ):

        priority_columns = [
            c for c in [
                "asset_id",
                "risk_score",
                "risk_level",
                "anomaly_count",
                "anomaly_rate",
                "max_temperature",
                "max_vibration",
                "maintenance_recommendation"
            ]
            if c in filtered_maintenance.columns
        ]

        priority_table = (
            filtered_maintenance[
                priority_columns
            ]
            .copy()
        )

        priority_table["risk_score"] = pd.to_numeric(
            priority_table["risk_score"],
            errors="coerce"
        )

        priority_table = (
            priority_table
            .dropna(
                subset=["risk_score"]
            )
            .sort_values(
                "risk_score",
                ascending=False
            )
            .head(20)
        )

        st.dataframe(
            priority_table,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇ Download Executive Risk Report",
            priority_table.to_csv(
                index=False
            ).encode("utf-8"),
            "icestream_executive_risk_report.csv",
            "text/csv"
        )

    else:

        st.info(
            "Executive priority data is unavailable."
        )


# ============================================================
# PAGE 3 - ASSET INTELLIGENCE
# ============================================================

elif page == "Asset Intelligence":

    st.title(
        "Asset Intelligence"
    )

    st.write(
        "Fleet-wide comparison of asset health and risk."
    )

    st.divider()

    if {
        "asset_id",
        "risk_score"
    }.issubset(
        filtered_maintenance.columns
    ):

        ranking = (
            filtered_maintenance[
                [
                    "asset_id",
                    "risk_score"
                ]
            ]
            .dropna()
            .sort_values(
                "risk_score",
                ascending=False
            )
            .head(20)
            .sort_values(
                "risk_score"
            )
        )

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=ranking[
                    "risk_score"
                ],
                y=ranking[
                    "asset_id"
                ].astype(str),
                orientation="h",
                text=ranking[
                    "risk_score"
                ].round(1),
                textposition="outside"
            )
        )

        fig = make_chart(
            fig,
            "Asset Risk Ranking",
            600
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader(
        "Asset Register"
    )

    asset_columns = [
        c for c in [
            "asset_id",
            "risk_score",
            "risk_level",
            "avg_temperature",
            "max_temperature",
            "avg_vibration",
            "max_vibration",
            "avg_pressure",
            "avg_humidity",
            "avg_fuel_level",
            "anomaly_count",
            "anomaly_rate",
            "maintenance_recommendation"
        ]
        if c in filtered_maintenance.columns
    ]

    if asset_columns:

        table = (
            filtered_maintenance[
                asset_columns
            ]
            .sort_values(
                "risk_score",
                ascending=False
            )
        )

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇ Download Asset Intelligence",
            table.to_csv(
                index=False
            ).encode("utf-8"),
            "icestream_asset_intelligence.csv",
            "text/csv"
        )


# ============================================================
# PAGE 4 - ASSET DRILL-DOWN
# ============================================================

elif page == "Asset Drill-Down":

    st.title(
        "Asset Drill-Down"
    )

    st.write(
        "Investigate individual asset behaviour and sensor performance."
    )

    st.divider()

    if "asset_id" not in anomaly.columns:

        st.error(
            "Asset data is unavailable."
        )

    else:

        assets = sorted(
            anomaly[
                "asset_id"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        if not assets:

            st.warning(
                "No assets found."
            )

        else:

            selected_asset = st.selectbox(
                "Select Asset",
                assets
            )

            asset_data = anomaly[
                anomaly[
                    "asset_id"
                ]
                .astype(str)
                ==
                selected_asset
            ].copy()

            if "asset_id" in maintenance.columns:

                asset_info = maintenance[
                    maintenance[
                        "asset_id"
                    ]
                    .astype(str)
                    ==
                    selected_asset
                ].copy()

            else:

                asset_info = pd.DataFrame()

            asset_records = len(
                asset_data
            )

            asset_anomalies = 0

            if "ml_anomaly" in asset_data.columns:

                asset_anomalies = int(
                    asset_data[
                        "ml_anomaly"
                    ]
                    .fillna(0)
                    .sum()
                )

            asset_risk_score = 0
            asset_risk_level = "UNKNOWN"

            if not asset_info.empty:

                if "risk_score" in asset_info.columns:

                    asset_risk_score = safe_number(
                        asset_info[
                            "risk_score"
                        ].iloc[0]
                    )

                if "risk_level" in asset_info.columns:

                    asset_risk_level = str(
                        asset_info[
                            "risk_level"
                        ].iloc[0]
                    ).upper()

            k1, k2, k3, k4 = st.columns(4)

            with k1:
                st.metric(
                    "OBSERVATIONS",
                    number_format(
                        asset_records
                    )
                )

            with k2:
                st.metric(
                    "ANOMALIES",
                    number_format(
                        asset_anomalies
                    )
                )

            with k3:
                st.metric(
                    "RISK SCORE",
                    decimal_format(
                        asset_risk_score
                    )
                )

            with k4:
                st.metric(
                    "RISK LEVEL",
                    asset_risk_level
                )

            st.divider()

            sensor_columns = [
                c for c in [
                    "temperature",
                    "vibration",
                    "pressure",
                    "humidity",
                    "fuel_level"
                ]
                if c in asset_data.columns
            ]

            if sensor_columns:

                selected_sensor = st.selectbox(
                    "Select Sensor",
                    sensor_columns
                )

                if "recorded_at" in asset_data.columns:

                    fig = go.Figure()

                    fig.add_trace(
                        go.Scatter(
                            x=asset_data[
                                "recorded_at"
                            ],
                            y=asset_data[
                                selected_sensor
                            ],
                            mode="lines",
                            name=selected_sensor
                        )
                    )

                    fig = make_chart(
                        fig,
                        f"{selected_sensor.title()} Trend — {selected_asset}",
                        430
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            c1, c2 = st.columns(2)

            with c1:

                if {
                    "recorded_at",
                    "risk_score"
                }.issubset(
                    asset_data.columns
                ):

                    fig = go.Figure()

                    fig.add_trace(
                        go.Scatter(
                            x=asset_data[
                                "recorded_at"
                            ],
                            y=asset_data[
                                "risk_score"
                            ],
                            mode="lines",
                            name="Risk Score"
                        )
                    )

                    fig = make_chart(
                        fig,
                        "Asset Risk Trend",
                        360
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            with c2:

                if {
                    "recorded_at",
                    "anomaly_score"
                }.issubset(
                    asset_data.columns
                ):

                    fig = go.Figure()

                    fig.add_trace(
                        go.Scatter(
                            x=asset_data[
                                "recorded_at"
                            ],
                            y=asset_data[
                                "anomaly_score"
                            ],
                            mode="lines",
                            name="Anomaly Score"
                        )
                    )

                    fig = make_chart(
                        fig,
                        "ML Anomaly Score",
                        360
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            st.subheader(
                "Maintenance Recommendation"
            )

            if not asset_info.empty:

                recommendation = asset_info.iloc[
                    0
                ].get(
                    "maintenance_recommendation",
                    "No recommendation available."
                )

                st.info(
                    str(recommendation)
                )

            else:

                st.info(
                    "No maintenance recommendation available."
                )


# ============================================================
# PAGE 5 - ANOMALY DETECTION
# ============================================================

elif page == "Anomaly Detection":

    st.title(
        "Machine Learning Anomaly Detection"
    )

    st.write(
        "Monitor abnormal sensor behaviour and ML detection results."
    )

    st.divider()

    temperature_alerts = 0
    vibration_alerts = 0

    if "temperature_anomaly" in filtered_anomaly.columns:

        temperature_alerts = int(
            filtered_anomaly[
                "temperature_anomaly"
            ]
            .fillna(0)
            .sum()
        )

    if "vibration_anomaly" in filtered_anomaly.columns:

        vibration_alerts = int(
            filtered_anomaly[
                "vibration_anomaly"
            ]
            .fillna(0)
            .sum()
        )

    k1, k2, k3 = st.columns(3)

    with k1:

        st.metric(
            "ML ANOMALIES",
            number_format(
                total_anomalies
            )
        )

    with k2:

        st.metric(
            "TEMPERATURE ALERTS",
            number_format(
                temperature_alerts
            )
        )

    with k3:

        st.metric(
            "VIBRATION ALERTS",
            number_format(
                vibration_alerts
            )
        )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        if {
            "risk_score",
            "anomaly_score"
        }.issubset(
            filtered_anomaly.columns
        ):

            sample = filtered_anomaly.copy()

            if len(sample) > 4000:

                sample = sample.sample(
                    4000,
                    random_state=42
                )

            fig = px.scatter(
                sample,
                x="risk_score",
                y="anomaly_score",
                hover_data=[
                    c for c in [
                        "asset_id",
                        "recorded_at",
                        "temperature",
                        "vibration"
                    ]
                    if c in sample.columns
                ]
            )

            fig = make_chart(
                fig,
                "Risk vs ML Anomaly Score",
                430
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with c2:

        if "anomaly_status" in filtered_anomaly.columns:

            status = (
                filtered_anomaly[
                    "anomaly_status"
                ]
                .astype(str)
                .value_counts()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Pie(
                    labels=status.index,
                    values=status.values,
                    hole=0.58,
                    textinfo="label+value"
                )
            )

            fig.update_layout(
                title="Detection Status",
                height=430,
                paper_bgcolor="#ffffff"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.subheader(
        "Recent Detection Events"
    )

    event_columns = [
        c for c in [
            "asset_id",
            "recorded_at",
            "temperature",
            "vibration",
            "pressure",
            "humidity",
            "risk_score",
            "risk_level",
            "anomaly_score",
            "anomaly_status"
        ]
        if c in filtered_anomaly.columns
    ]

    if event_columns:

        events = (
            filtered_anomaly[
                event_columns
            ]
            .sort_values(
                "recorded_at",
                ascending=False
            )
            .head(100)
        )

        st.dataframe(
            events,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇ Download Detection Events",
            events.to_csv(
                index=False
            ).encode("utf-8"),
            "icestream_anomaly_events.csv",
            "text/csv"
        )


# ============================================================
# PAGE 6 - PREDICTIVE MAINTENANCE
# ============================================================

elif page == "Predictive Maintenance":

    st.title(
        "Predictive Maintenance"
    )

    st.write(
        "Prioritize maintenance using asset risk and anomaly exposure."
    )

    st.divider()

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.metric(
            "HIGH PRIORITY",
            number_format(high_risk)
        )

    with k2:

        st.metric(
            "MEDIUM PRIORITY",
            number_format(medium_risk)
        )

    with k3:

        st.metric(
            "LOW PRIORITY",
            number_format(low_risk)
        )

    with k4:

        st.metric(
            "AVERAGE RISK",
            decimal_format(average_risk)
        )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        if "risk_score" in filtered_maintenance.columns:

            fig = go.Figure()

            fig.add_trace(
                go.Histogram(
                    x=filtered_maintenance[
                        "risk_score"
                    ],
                    nbinsx=20,
                    name="Risk"
                )
            )

            fig = make_chart(
                fig,
                "Risk Score Distribution",
                400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with c2:

        if {
            "risk_score",
            "anomaly_count"
        }.issubset(
            filtered_maintenance.columns
        ):

            fig = px.scatter(
                filtered_maintenance,
                x="risk_score",
                y="anomaly_count",
                hover_name=(
                    "asset_id"
                    if "asset_id"
                    in filtered_maintenance.columns
                    else None
                )
            )

            fig = make_chart(
                fig,
                "Risk vs Anomaly Exposure",
                400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.subheader(
        "Maintenance Queue"
    )

    maintenance_columns = [
        c for c in [
            "asset_id",
            "risk_score",
            "risk_level",
            "anomaly_count",
            "anomaly_rate",
            "avg_temperature",
            "max_temperature",
            "avg_vibration",
            "max_vibration",
            "maintenance_recommendation"
        ]
        if c in filtered_maintenance.columns
    ]

    if maintenance_columns:

        queue = (
            filtered_maintenance[
                maintenance_columns
            ]
            .sort_values(
                "risk_score",
                ascending=False
            )
        )

        st.dataframe(
            queue,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇ Download Maintenance Queue",
            queue.to_csv(
                index=False
            ).encode("utf-8"),
            "icestream_maintenance_queue.csv",
            "text/csv"
        )


# ============================================================
# PAGE 7 - DATA HEALTH
# ============================================================

elif page == "Data Health":

    st.title(
        "Data Health & Pipeline Monitoring"
    )

    st.write(
        "Validate data completeness, duplicates and pipeline status."
    )

    st.divider()

    if not pipeline.empty:

        total_rows = pd.to_numeric(
            pipeline.get(
                "rows",
                pd.Series(dtype=float)
            ),
            errors="coerce"
        ).fillna(0).sum()

        total_missing = pd.to_numeric(
            pipeline.get(
                "missing_values",
                pd.Series(dtype=float)
            ),
            errors="coerce"
        ).fillna(0).sum()

        total_duplicates = pd.to_numeric(
            pipeline.get(
                "duplicates",
                pd.Series(dtype=float)
            ),
            errors="coerce"
        ).fillna(0).sum()

        k1, k2, k3, k4 = st.columns(4)

        with k1:

            st.metric(
                "DATASETS CHECKED",
                number_format(
                    len(pipeline)
                )
            )

        with k2:

            st.metric(
                "ROWS PROCESSED",
                number_format(
                    total_rows
                )
            )

        with k3:

            st.metric(
                "MISSING VALUES",
                number_format(
                    total_missing
                )
            )

        with k4:

            st.metric(
                "DUPLICATES",
                number_format(
                    total_duplicates
                )
            )

        st.divider()

        st.subheader(
            "Pipeline Validation"
        )

        st.dataframe(
            pipeline,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Pipeline health report not found."
        )

    # ========================================================
    # REPORT INVENTORY
    # ========================================================

    st.subheader(
        "Report Inventory"
    )

    report_files = [
        "anomaly_detection_results.csv",
        "anomaly_summary.csv",
        "asset_anomaly_summary.csv",
        "asset_risk_analysis.csv",
        "maintenance_risk_scoring.csv",
        "pipeline_health_report.csv",
        "sensor_summary_statistics.csv"
    ]

    inventory = []

    for filename in report_files:

        dataframe = load_csv(
            filename
        )

        file_path = REPORTS_DIR / filename

        inventory.append(
            {
                "Report": filename,
                "Rows": len(dataframe),
                "Columns": len(dataframe.columns),
                "Missing Values": int(
                    dataframe.isna()
                    .sum()
                    .sum()
                ),
                "Duplicates": int(
                    dataframe.duplicated()
                    .sum()
                ),
                "File Status": (
                    "READY"
                    if (
                        file_path.exists()
                        and not dataframe.empty
                    )
                    else "MISSING"
                )
            }
        )

    inventory_df = pd.DataFrame(
        inventory
    )

    st.dataframe(
        inventory_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "❄️ IceStream Operations Intelligence  |  "
    "Fleet Monitoring • ML Anomaly Detection • "
    "Predictive Maintenance • Risk Intelligence • Data Health"
)