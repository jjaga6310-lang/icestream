from pathlib import Path
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ============================================================
# IceStream - Realistic Source Data Generator
# ============================================================

SEED = 42

random.seed(SEED)
np.random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 1. Assets
# ============================================================

locations = [
    "Chennai",
    "Bangalore",
    "Hyderabad",
    "Mumbai",
    "Pune",
    "Delhi",
    "Kolkata",
]

asset_types = [
    "Refrigerated Truck",
    "Cold Storage",
    "Delivery Van",
]

assets = []

for i in range(1, 21):
    assets.append({
        "asset_id": f"AST-{i:04d}",
        "asset_name": f"IceStream Asset {i:04d}",
        "asset_type": random.choice(asset_types),
        "location": random.choice(locations),
        "status": random.choices(
            ["ACTIVE", "MAINTENANCE", "INACTIVE"],
            weights=[85, 10, 5]
        )[0],
        "created_at": datetime.now() - timedelta(
            days=random.randint(30, 1000)
        ),
    })

assets_df = pd.DataFrame(assets)


# ============================================================
# 2. Sensor Readings
# ============================================================

sensor_rows = []

start_time = datetime.now() - timedelta(days=30)

asset_ids = assets_df["asset_id"].tolist()

for _ in range(5000):

    timestamp = start_time + timedelta(
        minutes=random.randint(0, 30 * 24 * 60)
    )

    temperature = np.random.normal(4.5, 1.5)
    vibration = abs(np.random.normal(2.5, 0.8))
    pressure = np.random.normal(101.3, 2.0)
    humidity = np.clip(np.random.normal(65, 10), 20, 100)
    fuel_level = np.clip(np.random.normal(65, 18), 5, 100)

    # Temperature anomaly
    if random.random() < 0.04:
        temperature += random.choice([-8, 8, 12])

    # Vibration anomaly
    if random.random() < 0.03:
        vibration += random.uniform(3, 7)

    sensor_rows.append({
        "asset_id": random.choice(asset_ids),
        "recorded_at": timestamp,
        "temperature": round(temperature, 2),
        "vibration": round(vibration, 2),
        "pressure": round(pressure, 2),
        "humidity": round(humidity, 2),
        "fuel_level": round(fuel_level, 2),
    })

sensor_df = pd.DataFrame(sensor_rows)


# ============================================================
# 3. Inventory
# ============================================================

products = [
    "Frozen Food",
    "Ice Cream",
    "Seafood",
    "Dairy",
    "Pharmaceutical Cold Chain",
]

inventory_rows = []

for i in range(1, 101):

    inventory_rows.append({
        "asset_id": random.choice(asset_ids),
        "product_id": f"PROD-{i:04d}",
        "quantity": random.randint(0, 1000),
        "reorder_level": random.randint(100, 300),
        "warehouse_location": random.choice(locations),
        "updated_at": datetime.now(),
    })

inventory_df = pd.DataFrame(inventory_rows)


# ============================================================
# 4. Shipments
# ============================================================

shipment_rows = []

for i in range(1, 501):

    scheduled = start_time + timedelta(
        hours=random.randint(0, 30 * 24)
    )

    delay = max(
        0,
        int(np.random.normal(25, 40))
    )

    actual_delivery = scheduled + timedelta(
        minutes=delay
    )

    shipment_rows.append({
        "shipment_id": f"SHP-{i:05d}",
        "asset_id": random.choice(asset_ids),
        "scheduled_time": scheduled,
        "actual_delivery_time": actual_delivery,
        "delay_minutes": delay,
        "origin": random.choice(locations),
        "destination": random.choice(locations),
        "status": (
            "delivered"
            if delay < 90
            else "delayed"
        ),
    })

shipments_df = pd.DataFrame(shipment_rows)


# ============================================================
# 5. Maintenance Records
# ============================================================

maintenance_types = [
    "Preventive",
    "Corrective",
    "Inspection",
    "Emergency",
]

maintenance_rows = []

for _ in range(200):

    maintenance_rows.append({
        "asset_id": random.choice(asset_ids),
        "maintenance_type": random.choice(
            maintenance_types
        ),
        "maintenance_date": start_time + timedelta(
            days=random.randint(0, 30)
        ),
        "technician": f"TECH-{random.randint(1, 20):03d}",
        "cost": round(
            random.uniform(100, 5000),
            2
        ),
        "description": (
            "Routine IceStream equipment maintenance"
        ),
        "status": random.choice([
            "completed",
            "scheduled"
        ]),
    })

maintenance_df = pd.DataFrame(
    maintenance_rows
)


# ============================================================
# 6. Intentional Data Quality Problems
# ============================================================

# Missing temperature values
missing_indexes = sensor_df.sample(
    frac=0.01,
    random_state=SEED
).index

sensor_df.loc[
    missing_indexes,
    "temperature"
] = np.nan


# Duplicate records
duplicates = sensor_df.sample(
    10,
    random_state=SEED
)

sensor_df = pd.concat(
    [sensor_df, duplicates],
    ignore_index=True
)


# ============================================================
# 7. Save CSV files
# ============================================================

datasets = {
    "assets.csv": assets_df,
    "sensor_readings.csv": sensor_df,
    "inventory.csv": inventory_df,
    "shipments.csv": shipments_df,
    "maintenance_records.csv": maintenance_df,
}

print("\nGenerating IceStream datasets...\n")

for filename, dataframe in datasets.items():

    path = RAW_DIR / filename

    dataframe.to_csv(
        path,
        index=False
    )

    print(
        f"✓ {filename:<25} "
        f"{len(dataframe):>6,} rows"
    )

print("\nDataset generation completed.")
print(f"Location: {RAW_DIR}")
