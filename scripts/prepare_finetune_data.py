# scripts/prepare_finetune_data.py
import pandas as pd
from datasets import Dataset

# Synthetic examples
data = [
    {"prompt": "Why increase laptop price in Q4?", "response": "Due to 20% demand surge and low inventory, elasticity suggests a 15% price hike aligns with competitor trends."},
    {"prompt": "Why lower phone price?", "response": "High inventory and 10% competitor price drop indicate oversupply; elasticity supports a 5% reduction."}
] * 500  # Scale to 1K
dataset = Dataset.from_pandas(pd.DataFrame(data))
dataset.save_to_disk("data/finetune_dataset")