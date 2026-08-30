from pathlib import Path

import pandas as pd


# ============================================================
# IceStream - Maintenance Risk Scoring
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

SENSOR_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "sensor_features.csv"
)

ANOMALY_FILE = (
    BASE_DIR
    / "reports"
    / "anomaly_detection_results.csv"
)

OUTPUT_DIR = BASE_DIR / "reports"

OUTPUT_FILE = (
    OUTPUT_DIR
    / "maintenance_risk_scoring.csv"
)


def load_data():
    """Load sensor and machine-learning anomaly data."""

    sensor = pd.read_csv(SENSOR_FILE)
    anomaly = pd.read_csv(ANOMALY_FILE)

    print(f"Sensor records: {len(sensor):,}")
    print(f"Anomaly records: {len(anomaly):,}")

    return sensor, anomaly


def build_asset_features(sensor, anomaly):
    """Create asset-level maintenance risk features."""

    sensor_summary = (
        sensor.groupby("asset_id")
        .agg(
            avg_temperature=("temperature", "mean"),
            max_temperature=("temperature", "max"),
            avg_vibration=("vibration", "mean"),
            max_vibration=("vibration", "max"),
            avg_pressure=("pressure", "mean"),
            avg_humidity=("humidity", "mean"),
            avg_fuel_level=("fuel_level", "mean"),
            sensor_records=("asset_id", "size"),
        )
        .reset_index()
    )

    anomaly_summary = (
        anomaly.groupby("asset_id")
        .agg(
            anomaly_count=("ml_anomaly", "sum"),
            average_anomaly_score=(
                "anomaly_score",
                "mean",
            ),
        )
        .reset_index()
    )

    result = sensor_summary.merge(
        anomaly_summary,
        on="asset_id",
        how="left",
    )

    result["anomaly_count"] = (
        result["anomaly_count"].fillna(0)
    )

    result["average_anomaly_score"] = (
        result["average_anomaly_score"].fillna(0)
    )

    result["anomaly_rate"] = (
        result["anomaly_count"]
        / result["sensor_records"]
        * 100
    )

    return result


def calculate_risk_score(df):
    """
    Calculate a transparent maintenance risk score.

    Components:
        Anomaly rate       -> 40 points
        Maximum vibration  -> 25 points
        Maximum temperature-> 20 points
        Average vibration  -> 15 points

    Total score: 0-100
    """

    df = df.copy()

    # Normalize anomaly rate
    df["anomaly_component"] = (
        df["anomaly_rate"]
        .clip(0, 10)
        / 10
        * 40
    )

    # Normalize maximum vibration
    df["vibration_component"] = (
        df["max_vibration"]
        .clip(0, 10)
        / 10
        * 25
    )

    # Normalize maximum temperature
    df["temperature_component"] = (
        df["max_temperature"]
        .clip(0, 20)
        / 20
        * 20
    )

    # Normalize average vibration
    df["avg_vibration_component"] = (
        df["avg_vibration"]
        .clip(0, 5)
        / 5
        * 15
    )

    df["risk_score"] = (
        df["anomaly_component"]
        + df["vibration_component"]
        + df["temperature_component"]
        + df["avg_vibration_component"]
    ).round(2)

    def classify(score):

        if score >= 70:
            return "HIGH"

        if score >= 40:
            return "MEDIUM"

        return "LOW"

    df["risk_level"] = (
        df["risk_score"]
        .apply(classify)
    )

    return df


def create_recommendation(df):
    """Create maintenance recommendations."""

    def recommendation(row):

        if row["risk_level"] == "HIGH":
            return "Immediate inspection recommended"

        if row["risk_level"] == "MEDIUM":
            return "Schedule preventive inspection"

        return "Continue routine monitoring"

    df["maintenance_recommendation"] = (
        df.apply(
            recommendation,
            axis=1,
        )
    )

    return df


def main():

    print("\n" + "=" * 65)
    print("          ICESTREAM MAINTENANCE RISK SCORING")
    print("=" * 65)

    sensor, anomaly = load_data()

    df = build_asset_features(
        sensor,
        anomaly,
    )

    df = calculate_risk_score(df)

    df = create_recommendation(df)

    df = df.sort_values(
        "risk_score",
        ascending=False,
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\nMaintenance risk distribution:")

    print(
        df["risk_level"].value_counts()
    )

    print("\nTop 10 maintenance priorities:")

    print(
        df[
            [
                "asset_id",
                "risk_score",
                "risk_level",
                "anomaly_rate",
                "max_vibration",
                "max_temperature",
                "maintenance_recommendation",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print(
        f"\nResults saved to:\n{OUTPUT_FILE}"
    )

    print(
        "\nMaintenance risk scoring completed successfully."
    )


if __name__ == "__main__":
    main()