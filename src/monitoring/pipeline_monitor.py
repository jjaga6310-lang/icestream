from pathlib import Path
from datetime import datetime

import pandas as pd


# ============================================================
# IceStream - Pipeline Monitoring & Data Observability
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
QUARANTINE_DIR = DATA_DIR / "quarantine"

REPORT_DIR = BASE_DIR / "reports"

OUTPUT_FILE = REPORT_DIR / "pipeline_health_report.csv"


def check_file(file_path):
    """Check whether a required file exists and is readable."""

    if not file_path.exists():
        return {
            "status": "FAILED",
            "rows": 0,
            "missing_values": 0,
            "duplicates": 0,
            "file_size_kb": 0,
        }

    try:
        df = pd.read_csv(file_path)

        return {
            "status": "PASSED",
            "rows": len(df),
            "missing_values": int(df.isna().sum().sum()),
            "duplicates": int(df.duplicated().sum()),
            "file_size_kb": round(
                file_path.stat().st_size / 1024,
                2,
            ),
        }

    except Exception:
        return {
            "status": "FAILED",
            "rows": 0,
            "missing_values": 0,
            "duplicates": 0,
            "file_size_kb": 0,
        }


def build_checks():
    """Define pipeline datasets to monitor."""

    return [
        ("raw", "assets.csv", RAW_DIR / "assets.csv"),
        ("raw", "inventory.csv", RAW_DIR / "inventory.csv"),
        (
            "raw",
            "maintenance_records.csv",
            RAW_DIR / "maintenance_records.csv",
        ),
        (
            "raw",
            "sensor_readings.csv",
            RAW_DIR / "sensor_readings.csv",
        ),
        ("raw", "shipments.csv", RAW_DIR / "shipments.csv"),
        (
            "processed",
            "assets.csv",
            PROCESSED_DIR / "assets.csv",
        ),
        (
            "processed",
            "inventory.csv",
            PROCESSED_DIR / "inventory.csv",
        ),
        (
            "processed",
            "maintenance_records.csv",
            PROCESSED_DIR / "maintenance_records.csv",
        ),
        (
            "processed",
            "sensor_readings.csv",
            PROCESSED_DIR / "sensor_readings.csv",
        ),
        (
            "processed",
            "shipments.csv",
            PROCESSED_DIR / "shipments.csv",
        ),
        (
            "processed",
            "sensor_features.csv",
            PROCESSED_DIR / "sensor_features.csv",
        ),
        (
            "quarantine",
            "sensor_readings.csv",
            QUARANTINE_DIR / "sensor_readings.csv",
        ),
    ]


def run_monitoring():
    """Run all pipeline health checks."""

    records = []

    for layer, filename, file_path in build_checks():

        result = check_file(file_path)

        records.append(
            {
                "checked_at": datetime.now().isoformat(
                    timespec="seconds"
                ),
                "layer": layer,
                "dataset": filename,
                "status": result["status"],
                "rows": result["rows"],
                "missing_values": result[
                    "missing_values"
                ],
                "duplicates": result["duplicates"],
                "file_size_kb": result[
                    "file_size_kb"
                ],
            }
        )

    return pd.DataFrame(records)


def main():

    print("\n" + "=" * 65)
    print("          ICESTREAM PIPELINE MONITOR")
    print("=" * 65)

    report = run_monitoring()

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    report.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    passed = (
        report["status"] == "PASSED"
    ).sum()

    failed = (
        report["status"] == "FAILED"
    ).sum()

    total = len(report)

    print(f"\nDatasets checked: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    print("\nPipeline health:")

    if failed == 0:
        print("STATUS: HEALTHY")
    else:
        print("STATUS: DEGRADED")

    print("\nDataset checks:")

    print(
        report[
            [
                "layer",
                "dataset",
                "status",
                "rows",
                "missing_values",
                "duplicates",
            ]
        ].to_string(index=False)
    )

    print(
        f"\nHealth report saved to:\n{OUTPUT_FILE}"
    )

    print(
        "\nPipeline monitoring completed successfully."
    )


if __name__ == "__main__":
    main()