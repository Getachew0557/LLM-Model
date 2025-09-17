import sqlite3
import pandas as pd

# Export data for Superset
conn = sqlite3.connect("data/warehouse.db")
df = pd.read_sql("SELECT * FROM prices", conn)

# Add LLM explanations (run RAG for sample products)
explanations = []
for product in df["name"].unique()[:5]:
    result = qa_chain({"query": f"Why adjust price for {product}?"})
    explanations.append({"product": product, "explanation": result["result"]})
df_exp = pd.DataFrame(explanations)
df_exp.to_sql("explanations", conn, if_exists="replace")

# Manual step: In Superset UI (localhost:8088)
# 1. Add SQLite DB: data/warehouse.db
# 2. Create charts: Line (price vs. time), Table (explanations), Heatmap (elasticity)