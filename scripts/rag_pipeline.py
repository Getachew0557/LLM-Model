# scripts/rag_pipeline.py
from langchain import HuggingFacePipeline
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
import pandas as pd
import sqlite3

# Load ML outputs and scraped data
conn = sqlite3.connect("data/warehouse.db")
docs = pd.read_sql("SELECT * FROM prices", conn).to_dict("records")  # Convert to text docs

# Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
texts = [f"Product: {d['name']}, Price: {d['price']}, Demand: {d['demand']}, Seasonality: {d['seasonality']}" for d in docs]
vectorstore = FAISS.from_texts(texts, embeddings)

# Load fine-tuned LLM
llm = HuggingFacePipeline.from_model_id(
    model_id="models/finetuned_mistral",
    task="text-generation",
    pipeline_kwargs={"max_length": 150}
)

# RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Example query
result = qa_chain({"query": "Why increase laptop price in Q4?"})
print(result["result"])  # E.g., "Due to 20% demand surge and low inventory, elasticity suggests..."