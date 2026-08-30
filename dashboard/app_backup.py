import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="IceStream | Operations Intelligence",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS = BASE_DIR / "reports"

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=60)
def load_data():

    def load_csv(filename):
        path = REPORTS / filename

        if not path.exists():
            return pd.DataFrame()

        try:
            return pd.read_csv(path)
        except Exception:
            return pd.DataFrame()

    return {
        "anomaly": load_csv("anomaly_detection_results.csv"),
        "maintenance": load_csv("maintenance_risk_scoring.csv"),
        "pipeline": load_csv("pipeline_health_report.csv"),
        "anomaly_summary": load_csv("anomaly_summary.csv"),
        "asset_anomaly": load_csv("asset_anomaly_summary.csv"),
        "asset_risk": load_csv("asset_risk_analysis.csv"),
        "sensor_summary": load_csv("sensor_summary_statistics.csv")
    }


data = load_data()

anomaly = data["anomaly"].copy()
maintenance = data["maintenance"].copy()
pipeline = data["pipeline"].copy()

# ============================================================
# CLEAN DATA
# ============================================================

if not anomaly.empty:

    if "recorded_at" in anomaly.columns:
        anomaly["recorded_at"] = pd.to_datetime(
            anomaly["recorded_at"],
            errors="coerce"
        )

    numeric_columns = [
        "temperature",
        "vibration",
        "pressure",
        "humidity",
        "fuel_level",
        "risk_score",
        "anomaly_score",
        "ml_anomaly",
        "temperature_anomaly",
        "vibration_anomaly"
    ]

    for col in numeric_columns:
        if col in anomaly.columns:
            anomaly[col] = pd.to_numeric(
                anomaly[col],
                errors="coerce"
            )


if not maintenance.empty:

    numeric_columns = [
        "risk_score",
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
        "anomaly_rate"
    ]

    for col in numeric_columns:
        if col in maintenance.columns:
            maintenance[col] = pd.to_numeric(
                maintenance[col],
                errors="coerce"
            )

# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   MAIN APPLICATION
   ========================================================== */

.stApp {
    background: #f4f7fb;
}

.block-container {
    max-width: 1550px;
    padding-top: 1.25rem;
    padding-bottom: 2rem;
}

/* ==========================================================
   MAIN HEADINGS
   ========================================================== */

h1 {
    color: #0f172a !important;
    font-weight: 900 !important;
    letter-spacing: -0.8px !important;
}

h2 {
    color: #1d4ed8 !important;
    font-weight: 850 !important;
}

h3 {
    color: #2563eb !important;
    font-weight: 800 !important;
}

/* ==========================================================
   SECTION HEADINGS
   ========================================================== */

.section-title {
    color: #2563eb !important;
    font-size: 1.03rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.55px !important;
    border-left: 5px solid #2563eb;
    padding-left: 11px;
    margin-top: 14px;
    margin-bottom: 12px;
    line-height: 1.3;
}

/* ==========================================================
   SIDEBAR
   ========================================================== */

[data-testid="stSidebar"] {
    background: #0f172a !important;
}

[data-testid="stSidebar"] > div {
    background: #0f172a !important;
}

[data-testid="stSidebar"] * {
    color: #ffffff;
}

/* ==========================================================
   BRAND
   ========================================================== */

.brand-title {
    color: #ffffff !important;
    font-size: 1.55rem;
    font-weight: 900;
    letter-spacing: -0.5px;
    margin-top: 2px;
    margin-bottom: 0;
}

.brand-subtitle {
    color: #93c5fd !important;
    font-size: 0.63rem;
    font-weight: 800;
    letter-spacing: 1.7px;
    margin-top: 3px;
}

/* ==========================================================
   SIDEBAR FILTER HEADING
   ========================================================== */

.filter-title {
    color: #60a5fa !important;
    font-size: 0.80rem !important;
    font-weight: 900 !important;
    letter-spacing: 1px !important;
    margin-bottom: 12px !important;
}

/* ==========================================================
   SIDEBAR LABELS
   ========================================================== */

[data-testid="stSidebar"] label {
    color: #ffffff !important;
    font-weight: 750 !important;
}

[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    color: #ffffff !important;
}

[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #ffffff !important;
}

/* ==========================================================
   SIDEBAR SELECT BOX
   ========================================================== */

[data-testid="stSidebar"] [data-baseweb="select"] {
    background: #1e293b !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #ffffff !important;
}

[data-testid="stSidebar"] [data-baseweb="select"]:hover {
    border-color: #60a5fa !important;
}

/* ==========================================================
   SIDEBAR MULTISELECT TAGS
   ========================================================== */

[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: #2563eb !important;
}

[data-testid="stSidebar"] [data-baseweb="tag"] * {
    color: #ffffff !important;
}

/* ==========================================================
   OBSERVATION PERIOD
   ========================================================== */

.observation-title {
    color: #60a5fa !important;
    font-size: 0.82rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.8px !important;
    margin-top: 12px !important;
    margin-bottom: 9px !important;
    text-transform: uppercase;
}

/* Date container */

[data-testid="stSidebar"] [data-testid="stDateInput"] {
    width: 100% !important;
}

/* Date text */

[data-testid="stSidebar"] [data-testid="stDateInput"] input {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background: #1e293b !important;
    border: 1px solid #60a5fa !important;
    border-radius: 9px !important;
    font-size: 0.82rem !important;
    font-weight: 800 !important;
    padding: 8px 10px !important;
    opacity: 1 !important;
}

/* Date hover */

[data-testid="stSidebar"] [data-testid="stDateInput"] input:hover {
    background: #263449 !important;
    border-color: #93c5fd !important;
}

/* Date focus */

[data-testid="stSidebar"] [data-testid="stDateInput"] input:focus {
    border-color: #60a5fa !important;
    box-shadow: 0 0 0 2px rgba(96,165,250,0.25) !important;
}

/* Date calendar icon */

[data-testid="stSidebar"] [data-testid="stDateInput"] button {
    color: #60a5fa !important;
}

/* ==========================================================
   SYSTEM HEALTH
   ========================================================== */

.health-title {
    color: #60a5fa !important;
    font-size: 0.80rem;
    font-weight: 900;
    letter-spacing: 1px;
    margin-top: 5px;
    margin-bottom: 13px;
}

.health-card {
    width: 100%;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 9px;
    padding: 10px 12px;
    margin-bottom: 8px;
}

.health-card:hover {
    background: #263449;
    border-color: #475569;
}

.health-name {
    color: #ffffff !important;
    font-size: 0.77rem;
    font-weight: 700;
    white-space: nowrap;
}

.health-ready {
    color: #4ade80 !important;
    font-size: 0.67rem;
    font-weight: 900;
    letter-spacing: 0.7px;
}

.health-check {
    color: #fbbf24 !important;
    font-size: 0.67rem;
    font-weight: 900;
    letter-spacing: 0.7px;
}

.health-dot-ready {
    color: #22c55e !important;
}

.health-dot-check {
    color: #f59e0b !important;
}

/* ==========================================================
   KPI CARDS
   ========================================================== */

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
    padding: 16px 18px;
    min-height: 105px;
    box-shadow: 0 3px 10px rgba(15,23,42,0.045);
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 0.70rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.35px !important;
}

[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-size: 1.55rem !important;
    font-weight: 900 !important;
}

/* ==========================================================
   PLOTLY CHART CONTAINERS
   ========================================================== */

[data-testid="stPlotlyChart"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
    padding: 4px;
    box-shadow: 0 3px 10px rgba(15,23,42,0.04);
}

/* ==========================================================
   DATAFRAME
   ========================================================== */

[data-testid="stDataFrame"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
    overflow: hidden;
}

/* ==========================================================
   BUTTONS
   ========================================================== */

.stDownloadButton button {
    border-radius: 8px !important;
    font-weight: 750 !important;
}

/* ==========================================================
   DIVIDERS
   ========================================================== */

hr {
    border: none;
    border-top: 1px solid #dbe3ed;
    margin: 1.15rem 0;
}

/* ==========================================================
   ALERT BOXES
   ========================================================== */

[data-testid="stAlert"] {
    border-radius: 10px;
}

/* ==========================================================
   DATE PICKER POPUP
   ========================================================== */

[data-baseweb="calendar"] {
    background: #ffffff !important;
}

[data-baseweb="calendar"] * {
    color: #111827 !important;
}

</style>
""",
    unsafe_allow_html=True
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def fmt_number(value):
    try:
        return f"{int(value):,}"
    except Exception:
        return "0"


def fmt_decimal(value):
    try:
        return f"{float(value):.1f}"
    except Exception:
        return "0.0"


def fmt_percent(value):
    try:
        return f"{float(value):.1f}%"
    except Exception:
        return "0.0%"


def style_chart(fig, title, height=390):

    fig.update_layout(
        title=dict(
            text=title,
            x=0.02,
            xanchor="left",
            font=dict(
                size=16,
                color="#0f172a"
            )
        ),
        height=height,
        margin=dict(
            l=25,
            r=25,
            t=60,
            b=25
        ),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(
            family="Arial",
            color="#334155"
        ),
        legend=dict(
            orientation="h",
            y=1.02,
            x=0
        )
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#e2e8f0"
    )

    fig.update_yaxes(
        gridcolor="#edf1f5",
        zeroline=False
    )

    return fig


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="brand-title">❄️ IceStream</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-subtitle">OPERATIONS INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Command Center",
            "Asset Intelligence",
            "Anomaly Detection",
            "Maintenance",
            "Data Health"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        """
        <div class="filter-title">
            FILTERS
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # ASSET FILTER
    # --------------------------------------------------------

    if "asset_id" in anomaly.columns:

        assets = sorted(
            anomaly["asset_id"]
            .dropna()
            .astype(str)
            .unique()
        )

    else:

        assets = []

    selected_assets = st.multiselect(
        "Assets",
        assets,
        placeholder="All assets"
    )

    # --------------------------------------------------------
    # RISK FILTER
    # --------------------------------------------------------

    if "risk_level" in maintenance.columns:

        risks = sorted(
            maintenance["risk_level"]
            .dropna()
            .astype(str)
            .str.upper()
            .unique()
        )

    else:

        risks = []

    selected_risks = st.multiselect(
        "Risk Level",
        risks,
        placeholder="All risk levels"
    )

    # --------------------------------------------------------
    # OBSERVATION PERIOD
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="observation-title">
            📅 Observation Period
        </div>
        """,
        unsafe_allow_html=True
    )

    date_selection = None

    if "recorded_at" in anomaly.columns:

        valid_dates = anomaly[
            "recorded_at"
        ].dropna()

        if not valid_dates.empty:

            minimum_date = valid_dates.min().date()
            maximum_date = valid_dates.max().date()

            date_selection = st.date_input(
                "Select date range",
                value=(
                    minimum_date,
                    maximum_date
                ),
                min_value=minimum_date,
                max_value=maximum_date,
                label_visibility="collapsed"
            )

    st.divider()

    # ========================================================
    # SYSTEM HEALTH
    # ========================================================

    st.markdown(
        '<div class="health-title">SYSTEM HEALTH</div>',
        unsafe_allow_html=True
    )

    analytics_ready = (
        not data["sensor_summary"].empty
        or not anomaly.empty
    )

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

    systems = [
        ("Analytics Engine", analytics_ready),
        ("ML Detection", ml_ready),
        ("Maintenance Engine", maintenance_ready),
        ("Data Pipeline", pipeline_ready)
    ]

    for name, ready in systems:

        if ready:

            st.markdown(
                f"""
                <div class="health-card">
                    <div class="health-name">
                        <span class="health-dot-ready">●</span>
                        &nbsp;{name}
                    </div>
                    <div class="health-ready">
                        READY
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="health-card">
                    <div class="health-name">
                        <span class="health-dot-check">●</span>
                        &nbsp;{name}
                    </div>
                    <div class="health-check">
                        CHECK
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_anomaly = anomaly.copy()
filtered_maintenance = maintenance.copy()

if selected_assets:

    if "asset_id" in filtered_anomaly.columns:

        filtered_anomaly = filtered_anomaly[
            filtered_anomaly["asset_id"]
            .astype(str)
            .isin(selected_assets)
        ]

    if "asset_id" in filtered_maintenance.columns:

        filtered_maintenance = filtered_maintenance[
            filtered_maintenance["asset_id"]
            .astype(str)
            .isin(selected_assets)
        ]


if selected_risks:

    if "risk_level" in filtered_maintenance.columns:

        filtered_maintenance = filtered_maintenance[
            filtered_maintenance["risk_level"]
            .astype(str)
            .str.upper()
            .isin(selected_risks)
        ]


if (
    date_selection
    and isinstance(date_selection, tuple)
    and len(date_selection) == 2
    and "recorded_at" in filtered_anomaly.columns
):

    start_date = pd.Timestamp(
        date_selection[0]
    )

    end_date = (
        pd.Timestamp(
            date_selection[1]
        )
        + pd.Timedelta(days=1)
    )

    filtered_anomaly = filtered_anomaly[
        (
            filtered_anomaly["recorded_at"]
            >= start_date
        )
        &
        (
            filtered_anomaly["recorded_at"]
            < end_date
        )
    ]

# ============================================================
# KPI CALCULATIONS
# ============================================================

if "asset_id" in filtered_anomaly.columns:

    asset_count = filtered_anomaly[
        "asset_id"
    ].nunique()

else:

    asset_count = len(
        filtered_maintenance
    )


record_count = len(
    filtered_anomaly
)


if "ml_anomaly" in filtered_anomaly.columns:

    anomaly_count = int(
        filtered_anomaly[
            "ml_anomaly"
        ]
        .fillna(0)
        .sum()
    )

else:

    anomaly_count = 0


if record_count > 0:

    anomaly_rate = (
        anomaly_count / record_count
    ) * 100

else:

    anomaly_rate = 0


if "risk_score" in filtered_maintenance.columns:

    fleet_risk = (
        filtered_maintenance[
            "risk_score"
        ]
        .mean()
    )

else:

    fleet_risk = 0


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
        (risk_values == "HIGH").sum()
    )

    medium_risk = int(
        (risk_values == "MEDIUM").sum()
    )

    low_risk = int(
        (risk_values == "LOW").sum()
    )

# ============================================================
# COMMAND CENTER
# ============================================================

if page == "Command Center":

    st.title(
        "Operations Command Center"
    )

    st.caption(
        "Real-time operational intelligence across assets, anomalies and maintenance risk."
    )

    st.divider()

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.metric(
            "MONITORED ASSETS",
            fmt_number(asset_count)
        )

    with k2:
        st.metric(
            "SENSOR OBSERVATIONS",
            fmt_number(record_count)
        )

    with k3:
        st.metric(
            "ANOMALIES",
            fmt_number(anomaly_count)
        )

    with k4:
        st.metric(
            "ANOMALY RATE",
            fmt_percent(anomaly_rate)
        )

    with k5:
        st.metric(
            "FLEET RISK",
            fmt_decimal(fleet_risk)
        )

    st.divider()

    left, right = st.columns(
        [1.6, 1],
        gap="large"
    )

    # ========================================================
    # ANOMALY ACTIVITY
    # ========================================================

    with left:

        st.markdown(
            '<div class="section-title">ANOMALY ACTIVITY</div>',
            unsafe_allow_html=True
        )

        if {
            "recorded_at",
            "ml_anomaly"
        }.issubset(
            filtered_anomaly.columns
        ):

            daily_data = filtered_anomaly.copy()

            daily_data["date_only"] = (
                daily_data[
                    "recorded_at"
                ].dt.date
            )

            daily = (
                daily_data
                .groupby(
                    "date_only"
                )["ml_anomaly"]
                .sum()
                .reset_index()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=daily["date_only"],
                    y=daily["ml_anomaly"],
                    mode="lines+markers",
                    fill="tozeroy",
                    line=dict(width=2),
                    marker=dict(size=5),
                    name="Anomalies"
                )
            )

            fig = style_chart(
                fig,
                "Daily anomaly volume",
                390
            )

            fig.update_yaxes(
                title="Events"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Anomaly trend data unavailable."
            )

    # ========================================================
    # RISK PROFILE
    # ========================================================

    with right:

        st.markdown(
            '<div class="section-title">FLEET RISK PROFILE</div>',
            unsafe_allow_html=True
        )

        risk_df = pd.DataFrame(
            {
                "Risk": [
                    "High",
                    "Medium",
                    "Low"
                ],
                "Assets": [
                    high_risk,
                    medium_risk,
                    low_risk
                ]
            }
        )

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=risk_df["Risk"],
                    values=risk_df["Assets"],
                    hole=0.62,
                    textinfo="label+value"
                )
            ]
        )

        fig.update_layout(
            title=dict(
                text="Asset risk distribution",
                x=0.02,
                font=dict(
                    size=16,
                    color="#0f172a"
                )
            ),
            height=390,
            margin=dict(
                l=10,
                r=10,
                t=60,
                b=10
            ),
            paper_bgcolor="#ffffff",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ========================================================
    # PRIORITY ASSETS
    # ========================================================

    st.markdown(
        '<div class="section-title">PRIORITY ASSETS</div>',
        unsafe_allow_html=True
    )

    if {
        "asset_id",
        "risk_score"
    }.issubset(
        filtered_maintenance.columns
    ):

        priority = (
            filtered_maintenance
            .sort_values(
                "risk_score",
                ascending=False
            )
            .head(10)
        )

        columns = [
            c
            for c in [
                "asset_id",
                "risk_score",
                "risk_level",
                "anomaly_count",
                "anomaly_rate",
                "maintenance_recommendation"
            ]
            if c in priority.columns
        ]

        priority_view = priority[
            columns
        ].copy()

        st.dataframe(
            priority_view,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Asset risk data unavailable."
        )

    # ========================================================
    # ALERTS
    # ========================================================

    st.markdown(
        '<div class="section-title">OPERATIONAL ALERTS</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:

        if high_risk > 0:
            st.warning(
                f"{high_risk} high-risk asset(s) require attention."
            )
        else:
            st.success(
                "No high-risk assets detected."
            )

    with b:

        if anomaly_rate >= 10:
            st.error(
                f"Anomaly exposure is {anomaly_rate:.1f}%."
            )
        elif anomaly_rate > 0:
            st.info(
                f"Anomaly exposure is {anomaly_rate:.1f}%."
            )
        else:
            st.success(
                "No anomaly exposure detected."
            )

    with c:

        if fleet_risk >= 70:
            st.error(
                f"Fleet risk is elevated: {fleet_risk:.1f}"
            )
        elif fleet_risk >= 40:
            st.warning(
                f"Fleet risk is moderate: {fleet_risk:.1f}"
            )
        else:
            st.success(
                f"Fleet risk is controlled: {fleet_risk:.1f}"
            )

# ============================================================
# ASSET INTELLIGENCE
# ============================================================

elif page == "Asset Intelligence":

    st.title(
        "Asset Intelligence"
    )

    st.caption(
        "Asset-level risk comparison and operational health."
    )

    st.markdown(
        '<div class="section-title">ASSET RISK ANALYSIS</div>',
        unsafe_allow_html=True
    )

    if {
        "asset_id",
        "risk_score"
    }.issubset(
        filtered_maintenance.columns
    ):

        chart_data = (
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
            .head(15)
            .sort_values(
                "risk_score"
            )
        )

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=chart_data[
                    "risk_score"
                ],
                y=chart_data[
                    "asset_id"
                ],
                orientation="h",
                text=chart_data[
                    "risk_score"
                ].round(1),
                textposition="outside"
            )
        )

        fig = style_chart(
            fig,
            "Highest-risk assets",
            520
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown(
        '<div class="section-title">ASSET REGISTER</div>',
        unsafe_allow_html=True
    )

    if not filtered_maintenance.empty:

        columns = [
            c
            for c in [
                "asset_id",
                "risk_score",
                "risk_level",
                "avg_temperature",
                "max_temperature",
                "avg_vibration",
                "max_vibration",
                "anomaly_count",
                "anomaly_rate"
            ]
            if c in filtered_maintenance.columns
        ]

        table = filtered_maintenance[
            columns
        ].sort_values(
            "risk_score",
            ascending=False
        )

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# ANOMALY DETECTION
# ============================================================

elif page == "Anomaly Detection":

    st.title(
        "Anomaly Detection"
    )

    st.caption(
        "Machine-learning anomaly signals and sensor-level investigation."
    )

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

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "ML ANOMALIES",
            fmt_number(anomaly_count)
        )

    with c2:
        st.metric(
            "TEMPERATURE ALERTS",
            fmt_number(temperature_alerts)
        )

    with c3:
        st.metric(
            "VIBRATION ALERTS",
            fmt_number(vibration_alerts)
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        if {
            "risk_score",
            "anomaly_score"
        }.issubset(
            filtered_anomaly.columns
        ):

            sample_size = min(
                len(filtered_anomaly),
                3000
            )

            if sample_size > 0:

                sample = filtered_anomaly.sample(
                    sample_size,
                    random_state=42
                )

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=sample["risk_score"],
                        y=sample["anomaly_score"],
                        mode="markers",
                        marker=dict(
                            size=6,
                            opacity=0.55
                        ),
                        text=(
                            sample["asset_id"]
                            if "asset_id"
                            in sample.columns
                            else None
                        ),
                        hovertemplate=(
                            "Risk: %{x:.2f}<br>"
                            "Anomaly: %{y:.2f}<br>"
                            "Asset: %{text}"
                            "<extra></extra>"
                        )
                    )
                )

                fig = style_chart(
                    fig,
                    "Risk score vs anomaly score",
                    420
                )

                fig.update_xaxes(
                    title="Risk score"
                )

                fig.update_yaxes(
                    title="Anomaly score"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

    with right:

        if "anomaly_status" in filtered_anomaly.columns:

            counts = (
                filtered_anomaly[
                    "anomaly_status"
                ]
                .astype(str)
                .value_counts()
            )

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=counts.index,
                        values=counts.values,
                        hole=0.58
                    )
                ]
            )

            fig.update_layout(
                title=dict(
                    text="Detection status",
                    x=0.02,
                    font=dict(
                        size=16,
                        color="#0f172a"
                    )
                ),
                height=420,
                margin=dict(
                    l=10,
                    r=10,
                    t=60,
                    b=10
                ),
                paper_bgcolor="#ffffff"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.markdown(
        '<div class="section-title">RECENT DETECTION EVENTS</div>',
        unsafe_allow_html=True
    )

    columns = [
        c
        for c in [
            "asset_id",
            "recorded_at",
            "temperature",
            "vibration",
            "pressure",
            "risk_score",
            "risk_level",
            "anomaly_score",
            "anomaly_status"
        ]
        if c in filtered_anomaly.columns
    ]

    if columns:

        recent = (
            filtered_anomaly[
                columns
            ]
            .sort_values(
                "recorded_at",
                ascending=False
            )
            .head(50)
        )

        st.dataframe(
            recent,
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# MAINTENANCE
# ============================================================

elif page == "Maintenance":

    st.title(
        "Predictive Maintenance"
    )

    st.caption(
        "Prioritize maintenance using asset risk and anomaly exposure."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "HIGH PRIORITY",
            fmt_number(high_risk)
        )

    with c2:
        st.metric(
            "MEDIUM PRIORITY",
            fmt_number(medium_risk)
        )

    with c3:
        st.metric(
            "LOW PRIORITY",
            fmt_number(low_risk)
        )

    with c4:
        st.metric(
            "AVERAGE RISK",
            fmt_decimal(fleet_risk)
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        if "risk_score" in filtered_maintenance.columns:

            fig = go.Figure()

            fig.add_trace(
                go.Histogram(
                    x=filtered_maintenance[
                        "risk_score"
                    ],
                    nbinsx=20
                )
            )

            fig = style_chart(
                fig,
                "Risk score distribution",
                390
            )

            fig.update_xaxes(
                title="Risk score"
            )

            fig.update_yaxes(
                title="Assets"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with right:

        if {
            "risk_score",
            "anomaly_count"
        }.issubset(
            filtered_maintenance.columns
        ):

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=filtered_maintenance[
                        "risk_score"
                    ],
                    y=filtered_maintenance[
                        "anomaly_count"
                    ],
                    mode="markers",
                    marker=dict(
                        size=10,
                        opacity=0.7
                    ),
                    text=(
                        filtered_maintenance[
                            "asset_id"
                        ]
                        if "asset_id"
                        in filtered_maintenance.columns
                        else None
                    ),
                    hovertemplate=(
                        "Asset: %{text}<br>"
                        "Risk: %{x:.1f}<br>"
                        "Anomalies: %{y}"
                        "<extra></extra>"
                    )
                )
            )

            fig = style_chart(
                fig,
                "Risk vs anomaly exposure",
                390
            )

            fig.update_xaxes(
                title="Risk score"
            )

            fig.update_yaxes(
                title="Anomaly count"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.markdown(
        '<div class="section-title">MAINTENANCE QUEUE</div>',
        unsafe_allow_html=True
    )

    columns = [
        c
        for c in [
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

    queue = (
        filtered_maintenance[
            columns
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
        "Download Maintenance Queue",
        data=queue.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="icestream_maintenance_queue.csv",
        mime="text/csv"
    )

# ============================================================
# DATA HEALTH
# ============================================================

elif page == "Data Health":

    st.title(
        "Data Health"
    )

    st.caption(
        "Monitor data quality, pipeline status and report availability."
    )

    if not pipeline.empty:

        rows = pd.to_numeric(
            pipeline.get(
                "rows",
                pd.Series(dtype=float)
            ),
            errors="coerce"
        ).fillna(0).sum()

        missing = pd.to_numeric(
            pipeline.get(
                "missing_values",
                pd.Series(dtype=float)
            ),
            errors="coerce"
        ).fillna(0).sum()

        duplicates = pd.to_numeric(
            pipeline.get(
                "duplicates",
                pd.Series(dtype=float)
            ),
            errors="coerce"
        ).fillna(0).sum()

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "DATASETS CHECKED",
                fmt_number(len(pipeline))
            )

        with c2:
            st.metric(
                "ROWS PROCESSED",
                fmt_number(rows)
            )

        with c3:
            st.metric(
                "MISSING VALUES",
                fmt_number(missing)
            )

        with c4:
            st.metric(
                "DUPLICATES",
                fmt_number(duplicates)
            )

        st.divider()

        st.markdown(
            '<div class="section-title">PIPELINE VALIDATION</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            pipeline,
            use_container_width=True,
            hide_index=True
        )

    st.markdown(
        '<div class="section-title">REPORT INVENTORY</div>',
        unsafe_allow_html=True
    )

    inventory = []

    for report_name, dataframe in data.items():

        inventory.append(
            {
                "Report": report_name,
                "Rows": len(dataframe),
                "Columns": len(dataframe.columns),
                "Missing": int(
                    dataframe.isna()
                    .sum()
                    .sum()
                ),
                "Duplicates": int(
                    dataframe.duplicated()
                    .sum()
                ),
                "Status": (
                    "Healthy"
                    if not dataframe.empty
                    else "Missing"
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
    "IceStream • Operations Intelligence Platform • "
    "Anomaly Detection • Predictive Maintenance • Data Quality"
)