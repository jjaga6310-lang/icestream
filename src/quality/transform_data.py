from pathlib import Path
import pandas as pd


# ============================================================
# IceStream - Data Transformation Pipeline
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "sensor_readings.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "sensor_features.csv"
)


def load_data():
    """Load validated sensor data."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print(f"Loaded records: {len(df):,}")

    return df


def transform_data(df):
    """Create analytics-ready sensor features."""

    df = df.copy()

    # Convert timestamp
    df["recorded_at"] = pd.to_datetime(
        df["recorded_at"],
        errors="coerce"
    )

    # Sort by asset and timestamp
    df = df.sort_values(
        ["asset_id", "recorded_at"]
    ).reset_index(drop=True)

    # Time-based features
    df["date"] = df["recorded_at"].dt.date
    df["hour"] = df["recorded_at"].dt.hour
    df["day_of_week"] = (
        df["recorded_at"].dt.dayofweek
    )

    # Temperature rolling average
    df["temperature_rolling_avg"] = (
        df.groupby("asset_id")["temperature"]
        .transform(
            lambda x: x.rolling(
                window=5,
                min_periods=1
            ).mean()
        )
    )

    # Vibration rolling average
    df["vibration_rolling_avg"] = (
        df.groupby("asset_id")["vibration"]
        .transform(
            lambda x: x.rolling(
                window=5,
                min_periods=1
            ).mean()
        )
    )

    # Temperature deviation
    df["temperature_deviation"] = (
        df["temperature"]
        - df["temperature_rolling_avg"]
    )

    # Vibration deviation
    df["vibration_deviation"] = (
        df["vibration"]
        - df["vibration_rolling_avg"]
    )

    # Simple temperature anomaly flag
    df["temperature_anomaly"] = (
        df["temperature_deviation"].abs()
        > 5
    )

    # Simple vibration anomaly flag
    df["vibration_anomaly"] = (
        df["vibration_deviation"].abs()
        > 0.5
    )

    # Overall risk score
    df["risk_score"] = (
        df["temperature_anomaly"].astype(int)
        + df["vibration_anomaly"].astype(int)
    )

    # Risk category
    df["risk_level"] = df["risk_score"].map(
        {
            0: "LOW",
            1: "MEDIUM",
            2: "HIGH"
        }
    )

    return df


def save_data(df):
    """Save transformed dataset."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"Transformed dataset saved to:\n"
        f"{OUTPUT_FILE}"
    )


def main():

    print("\n" + "=" * 65)
    print("       ICESTREAM DATA TRANSFORMATION")
    print("=" * 65)

    df = load_data()

    transformed_df = transform_data(df)

    save_data(transformed_df)

    print(
        f"\nOutput records: "
        f"{len(transformed_df):,}"
    )

    print(
        f"Output columns: "
        f"{len(transformed_df.columns)}"
    )

    print("\nRisk distribution:")

    print(
        transformed_df["risk_level"]
        .value_counts()
    )

    print("\nTransformation completed successfully.")


if __name__ == "__main__":
    main()