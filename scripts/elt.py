import pandas as pd
import sqlite3
from datetime import datetime

# Load scraped data
df = pd.read_json("data/competitor_prices.json")

# Add features: Seasonality (Q4 flag), demand proxy (fake for demo), inventory
df["seasonality"] = df["timestamp"].apply(lambda x: 1 if x.month >= 10 else 0)
df["demand"] = df["price"].apply(lambda x: x * 0.1 + 100)  # Synthetic demand
df["inventory"] = 50  # Static for demo; replace with real data

# Save to SQLite (warehouse)
conn = sqlite3.connect("data/warehouse.db")
df.to_sql("prices", conn, if_exists="replace", index=False)