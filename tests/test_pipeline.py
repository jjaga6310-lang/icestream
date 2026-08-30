from pathlib import Path

import pandas as pd


# ============================================================
# IceStream - Automated Pipeline Tests
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

PROCESSED_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"


def test_processed_sensor_data_exists():
    file = PROCESSED_DIR / "sensor_readings.csv"

    assert file.exists(), "Processed sensor data is missing"


def test_processed_sensor_data_is_clean():
    file = PROCESSED_DIR / "sensor_readings.csv"

    df = pd.read_csv(file)

    assert len(df) > 0
    assert df.isna().sum().sum() == 0
    assert df.duplicated().sum() == 0


def test_sensor_features_exist():
    file = PROCESSED_DIR / "sensor_features.csv"

    assert file.exists(), "Sensor features file is missing"


def test_sensor_features_schema():
    file = PROCESSED_DIR / "sensor_features.csv"

    df = pd.read_csv(file)

    required_columns = [
        "asset_id",
        "temperature",
        "vibration",
        "pressure",
        "humidity",
        "fuel_level",
        "risk_score",
        "risk_level",
    ]

    for column in required_columns:
        assert column in df.columns, f"Missing column: {column}"


def test_sensor_features_have_records():
    file = PROCESSED_DIR / "sensor_features.csv"

    df = pd.read_csv(file)

    assert len(df) == 4950


def test_anomaly_results_exist():
    file = REPORTS_DIR / "anomaly_detection_results.csv"

    assert file.exists(), "Anomaly detection results are missing"


def test_maintenance_risk_results_exist():
    file = REPORTS_DIR / "maintenance_risk_scoring.csv"

    assert file.exists(), "Maintenance risk results are missing"


def test_maintenance_risk_schema():
    file = REPORTS_DIR / "maintenance_risk_scoring.csv"

    df = pd.read_csv(file)

    required_columns = [
        "asset_id",
        "risk_score",
        "risk_level",
        "maintenance_recommendation",
    ]

    for column in required_columns:
        assert column in df.columns, f"Missing column: {column}"


def test_pipeline_health_report_exists():
    file = REPORTS_DIR / "pipeline_health_report.csv"

    assert file.exists(), "Pipeline health report is missing"


def test_pipeline_health():
    file = REPORTS_DIR / "pipeline_health_report.csv"

    df = pd.read_csv(file)

    assert len(df) > 0
    assert (df["status"] == "PASSED").all()