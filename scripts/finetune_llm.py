# scripts/finetune_llm.py
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_from_disk

# Load model/tokenizer
model_name = "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

# Load dataset
dataset = load_from_disk("data/finetune_dataset")

# Tokenize
def tokenize(examples):
    return tokenizer(examples["prompt"], text_target=examples["response"], truncation=True, padding="max_length", max_length=128)

tokenized_dataset = dataset.map(tokenize, batched=True)

# Training args
training_args = TrainingArguments(
    output_dir="models/finetuned_mistral",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_strategy="epoch",
    evaluation_strategy="epoch",
    load_best_model_at_end=True,
    fp16=True  # Mixed precision for speed
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer
)

trainer.train()
trainer.save_model("models/finetuned_mistral")