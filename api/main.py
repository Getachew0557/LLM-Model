from fastapi import FastAPI
import xgboost as xgb
from langchain.chains import RetrievalQA
import pandas as pd

app = FastAPI()

# Load models
xgb_model = xgb.XGBRegressor()
xgb_model.load_model("models/xgb_pricing.json")
qa_chain = ...  # Load from rag_pipeline.py

@app.post("/price")
async def predict_price(product_data: dict):
    # Predict price
    features = pd.DataFrame([product_data])  # E.g., {"demand": 120, "seasonality": 1, "inventory": 50}
    price = xgb_model.predict(features)[0]
    
    # Explain with RAG
    explanation = qa_chain({"query": f"Why set price to {price} for {product_data['name']}?"})["result"]
    
    return {"price": float(price), "explanation": explanation}