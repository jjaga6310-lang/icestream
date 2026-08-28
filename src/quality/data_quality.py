from pathlib import Path
import pandas as pd


# ============================================================
# IceStream - Row-Level Data Quality Pipeline
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
QUARANTINE_DIR = BASE_DIR / "data" / "quarantine"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Sensor validation
# ============================================================

def validate_sensor_readings(df):
    """
    Validate sensor records at row level.

    A record is invalid when:
    - asset_id is missing
    - recorded_at is missing
    - temperature is missing
    - vibration is negative
    - humidity is outside 0-100
    - fuel_level is outside 0-100
    """

    df = df.copy()

    # Convert numeric columns safely
    numeric_columns = [
        "temperature",
        "vibration",
        "pressure",
        "humidity",
        "fuel_level",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Individual validation rules
    missing_asset = df["asset_id"].isna()

    missing_timestamp = df["recorded_at"].isna()

    missing_temperature = df["temperature"].isna()

    invalid_vibration = df["vibration"] < 0

    invalid_humidity = (
        (df["humidity"] < 0)
        | (df["humidity"] > 100)
    )

    invalid_fuel = (
        (df["fuel_level"] < 0)
        | (df["fuel_level"] > 100)
    )

    # Detect complete duplicate records
    duplicate_record = df.duplicated(
        keep="first"
    )

    # Combine validation rules
    invalid = (
        missing_asset
        | missing_timestamp
        | missing_temperature
        | invalid_vibration
        | invalid_humidity
        | invalid_fuel
        | duplicate_record
    )

    valid_df = df.loc[
        ~invalid
    ].copy()

    quarantine_df = df.loc[
        invalid
    ].copy()

    # Add reason for quarantine
    reasons = []

    for index in quarantine_df.index:

        row = quarantine_df.loc[index]
        row_reasons = []

        if pd.isna(row["asset_id"]):
            row_reasons.append("missing_asset_id")

        if pd.isna(row["recorded_at"]):
            row_reasons.append("missing_timestamp")

        if pd.isna(row["temperature"]):
            row_reasons.append("missing_temperature")

        if pd.notna(row["vibration"]) and row["vibration"] < 0:
            row_reasons.append("negative_vibration")

        if (
            pd.notna(row["humidity"])
            and (
                row["humidity"] < 0
                or row["humidity"] > 100
            )
        ):
            row_reasons.append("invalid_humidity")

        if (
            pd.notna(row["fuel_level"])
            and (
                row["fuel_level"] < 0
                or row["fuel_level"] > 100
            )
        ):
            row_reasons.append("invalid_fuel_level")

        if duplicate_record.loc[index]:
            row_reasons.append("duplicate_record")

        reasons.append(
            "|".join(row_reasons)
        )

    quarantine_df["quarantine_reason"] = reasons

    return valid_df, quarantine_df


# ============================================================
# Generic dataset validation
# ============================================================

def validate_required_columns(
    df,
    required_columns
):
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    return missing_columns


# ============================================================
# Process sensor dataset
# ============================================================

def process_sensor_data():

    filename = "sensor_readings.csv"

    source_path = RAW_DIR / filename

    if not source_path.exists():
        print(
            f"ERROR: {source_path} not found."
        )
        return

    df = pd.read_csv(
        source_path
    )

    required_columns = [
        "asset_id",
        "recorded_at",
        "temperature",
        "vibration",
        "pressure",
        "humidity",
        "fuel_level",
    ]

    missing_columns = validate_required_columns(
        df,
        required_columns
    )

    if missing_columns:
        print(
            "ERROR: Missing columns:"
        )

        for column in missing_columns:
            print(f"  - {column}")

        return

    print("\n" + "=" * 65)
    print("IceStream Sensor Data Quality")
    print("=" * 65)

    print(
        f"Raw records: {len(df):,}"
    )

    valid_df, quarantine_df = (
        validate_sensor_readings(df)
    )

    # Save valid records
    processed_path = (
        PROCESSED_DIR / filename
    )

    valid_df.to_csv(
        processed_path,
        index=False
    )

    # Save invalid records
    quarantine_path = (
        QUARANTINE_DIR / filename
    )

    quarantine_df.to_csv(
        quarantine_path,
        index=False
    )

    # Quality statistics
    total_rows = len(df)
    valid_rows = len(valid_df)
    invalid_rows = len(quarantine_df)

    quality_percentage = (
        valid_rows / total_rows * 100
        if total_rows > 0
        else 0
    )

    print(
        f"Valid records: {valid_rows:,}"
    )

    print(
        f"Quarantined records: {invalid_rows:,}"
    )

    print(
        f"Data quality score: "
        f"{quality_percentage:.2f}%"
    )

    print(
        f"\nProcessed file:"
        f"\n  {processed_path}"
    )

    print(
        f"\nQuarantine file:"
        f"\n  {quarantine_path}"
    )

    # Save quality report
    report = pd.DataFrame([
        {
            "dataset": filename,
            "total_rows": total_rows,
            "valid_rows": valid_rows,
            "invalid_rows": invalid_rows,
            "quality_score_percent": round(
                quality_percentage,
                2
            ),
            "status": (
                "PASSED"
                if invalid_rows == 0
                else "PASSED_WITH_QUARANTINE"
            ),
        }
    ])

    report_path = (
        PROCESSED_DIR / "quality_report.csv"
    )

    report.to_csv(
        report_path,
        index=False
    )

    print(
        f"\nQuality report:"
        f"\n  {report_path}"
    )

    print("\n" + "=" * 65)
    print(
        "Sensor quality validation completed."
    )
    print("=" * 65)


# ============================================================
# Main
# ============================================================

def main():

    print("\n")
    print("=" * 65)
    print("        ICESTREAM DATA QUALITY PIPELINE")
    print("=" * 65)

    process_sensor_data()

    print("\nPipeline finished.")


if __name__ == "__main__":
    main()