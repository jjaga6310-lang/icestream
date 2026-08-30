from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest


# ============================================================
# IceStream - Advanced Anomaly Detection
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "sensor_features.csv"
)

OUTPUT_DIR = BASE_DIR / "reports"

OUTPUT_FILE = (
    OUTPUT_DIR
    / "anomaly_detection_results.csv"
)


def load_data():
    """Load transformed sensor data."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print(f"Records loaded: {len(df):,}")

    return df


def detect_anomalies(df):
    """Detect unusual sensor behavior using Isolation Forest."""

    features = [
        "temperature",
        "vibration",
        "pressure",
        "humidity",
        "fuel_level",
    ]

    model_data = df[features].copy()

    # Handle any unexpected missing values.
    model_data = model_data.fillna(
        model_data.median()
    )

    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42,
        n_jobs=-1,
    )

    predictions = model.fit_predict(
        model_data
    )

    scores = model.decision_function(
        model_data
    )

    df = df.copy()

    # Isolation Forest:
    #  1  = normal
    # -1  = anomaly

    df["ml_anomaly"] = (
        predictions == -1
    )

    df["anomaly_score"] = scores

    df["anomaly_status"] = df[
        "ml_anomaly"
    ].map(
        {
            True: "ANOMALOUS",
            False: "NORMAL",
        }
    )

    return df


def create_asset_summary(df):
    """Create asset-level anomaly summary."""

    summary = (
        df.groupby("asset_id")
        .agg(
            total_records=("asset_id", "size"),
            anomalous_records=(
                "ml_anomaly",
                "sum",
            ),
            average_anomaly_score=(
                "anomaly_score",
                "mean",
            ),
        )
        .reset_index()
    )

    summary["anomaly_percentage"] = (
        summary["anomalous_records"]
        / summary["total_records"]
        * 100
    )

    summary = summary.sort_values(
        "anomaly_percentage",
        ascending=False,
    )

    return summary


def main():

    print("\n" + "=" * 65)
    print("       ICESTREAM ADVANCED ANOMALY DETECTION")
    print("=" * 65)

    df = load_data()

    result = detect_anomalies(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    summary = create_asset_summary(
        result
    )

    summary.to_csv(
        OUTPUT_DIR
        / "asset_anomaly_summary.csv",
        index=False,
    )

    anomaly_count = result[
        "ml_anomaly"
    ].sum()

    normal_count = (
        len(result) - anomaly_count
    )

    print(
        f"\nNormal records: "
        f"{normal_count:,}"
    )

    print(
        f"Anomalous records: "
        f"{anomaly_count:,}"
    )

    print(
        f"Anomaly rate: "
        f"{anomaly_count / len(result) * 100:.2f}%"
    )

    print("\nTop 10 anomalous assets:")

    print(
        summary.head(10).to_string(
            index=False
        )
    )

    print(
        f"\nResults saved to:\n"
        f"{OUTPUT_FILE}"
    )

    print("\nAnomaly detection completed successfully.")


if __name__ == "__main__":
    main()