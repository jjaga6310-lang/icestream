from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# IceStream - Exploratory Data Analysis
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "sensor_features.csv"
)

REPORT_DIR = BASE_DIR / "reports"
CHART_DIR = REPORT_DIR / "charts"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    """Load transformed sensor data."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print(f"Records loaded: {len(df):,}")
    print(f"Columns loaded: {len(df.columns)}")

    return df


def generate_summary(df):
    """Generate statistical summary."""

    summary = df.describe(
        include="all"
    ).transpose()

    summary.to_csv(
        REPORT_DIR / "sensor_summary_statistics.csv"
    )

    print("\nSummary statistics saved.")


def analyze_risk(df):
    """Analyze risk distribution."""

    risk_counts = (
        df["risk_level"]
        .value_counts()
        .sort_index()
    )

    print("\nRisk distribution:")
    print(risk_counts)

    plt.figure(figsize=(8, 5))

    risk_counts.plot(
        kind="bar"
    )

    plt.title("IceStream Risk Distribution")
    plt.xlabel("Risk Level")
    plt.ylabel("Number of Records")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "risk_distribution.png",
        dpi=150
    )

    plt.close()


def analyze_temperature(df):
    """Analyze temperature."""

    print("\nTemperature statistics:")

    print(
        df["temperature"].describe()
    )

    plt.figure(figsize=(8, 5))

    df["temperature"].hist(
        bins=30
    )

    plt.title(
        "Temperature Distribution"
    )
    plt.xlabel("Temperature")
    plt.ylabel("Frequency")
    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "temperature_distribution.png",
        dpi=150
    )

    plt.close()


def analyze_vibration(df):
    """Analyze vibration."""

    print("\nVibration statistics:")

    print(
        df["vibration"].describe()
    )

    plt.figure(figsize=(8, 5))

    df["vibration"].hist(
        bins=30
    )

    plt.title(
        "Vibration Distribution"
    )
    plt.xlabel("Vibration")
    plt.ylabel("Frequency")
    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "vibration_distribution.png",
        dpi=150
    )

    plt.close()


def analyze_assets(df):
    """Identify assets with the highest risk."""

    asset_risk = (
        df.groupby("asset_id")
        .agg(
            total_records=("asset_id", "size"),
            high_risk_records=(
                "risk_level",
                lambda x: (x == "HIGH").sum()
            ),
            medium_risk_records=(
                "risk_level",
                lambda x: (x == "MEDIUM").sum()
            ),
            avg_temperature=(
                "temperature",
                "mean"
            ),
            avg_vibration=(
                "vibration",
                "mean"
            )
        )
        .reset_index()
    )

    asset_risk["high_risk_percentage"] = (
        asset_risk["high_risk_records"]
        / asset_risk["total_records"]
        * 100
    )

    asset_risk = asset_risk.sort_values(
        "high_risk_percentage",
        ascending=False
    )

    asset_risk.to_csv(
        REPORT_DIR / "asset_risk_analysis.csv",
        index=False
    )

    print("\nTop 10 high-risk assets:")

    print(
        asset_risk.head(10).to_string(
            index=False
        )
    )


def analyze_anomalies(df):
    """Analyze detected sensor anomalies."""

    temperature_anomalies = (
        df["temperature_anomaly"].sum()
    )

    vibration_anomalies = (
        df["vibration_anomaly"].sum()
    )

    print("\nAnomaly summary:")

    print(
        f"Temperature anomalies: "
        f"{temperature_anomalies:,}"
    )

    print(
        f"Vibration anomalies: "
        f"{vibration_anomalies:,}"
    )

    anomaly_summary = pd.DataFrame(
        {
            "anomaly_type": [
                "temperature",
                "vibration"
            ],
            "count": [
                temperature_anomalies,
                vibration_anomalies
            ]
        }
    )

    anomaly_summary.to_csv(
        REPORT_DIR / "anomaly_summary.csv",
        index=False
    )


def main():

    print("\n" + "=" * 65)
    print("          ICESTREAM EXPLORATORY DATA ANALYSIS")
    print("=" * 65)

    df = load_data()

    generate_summary(df)

    analyze_risk(df)

    analyze_temperature(df)

    analyze_vibration(df)

    analyze_assets(df)

    analyze_anomalies(df)

    print("\n" + "=" * 65)
    print("EDA completed successfully.")
    print("=" * 65)


if __name__ == "__main__":
    main()