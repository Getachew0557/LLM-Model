import streamlit as st
import requests

st.title("Marketplace Pricing Oracle")
product = st.text_input("Product Name", "Laptop")
demand = st.slider("Demand", 0, 200, 120)
seasonality = st.selectbox("Seasonality", [0, 1])
inventory = st.slider("Inventory", 0, 100, 50)

if st.button("Get Price"):
    response = requests.post("http://localhost:8000/price", json={
        "name": product, "demand": demand, "seasonality": seasonality, "inventory": inventory
    }).json()
    st.write(f"**Recommended Price**: ${response['price']:.2f}")
    st.write(f"**Why?**: {response['explanation']}")