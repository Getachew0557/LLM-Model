import pandas as pd
import xgboost as xgb
from dowhy import CausalModel
import sqlite3

# Load data
conn = sqlite3.connect("data/warehouse.db")
df = pd.read_sql("SELECT * FROM prices", conn)

# Features for pricing
X = df[["demand", "seasonality", "inventory"]]
y = df["price"]

# Train XGBoost
model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100)
model.fit(X, y)
model.save_model("models/xgb_pricing.json")

# Causal inference: Demand → Price effect
causal_model = CausalModel(
    data=df,
    treatment="demand",
    outcome="price",
    common_causes=["seasonality", "inventory"]
)
identified = causal_model.identify_effect()
estimate = causal_model.estimate_effect(identified, method_name="backdoor.linear_regression")
print(f"Causal effect of demand on price: {estimate.value}")  # E.g., 0.15 (elasticity)