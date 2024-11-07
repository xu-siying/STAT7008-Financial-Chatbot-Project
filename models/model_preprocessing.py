# Preprocess data for fine-tuning
from transformers import BertTokenizer, GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, BertForSequenceClassification

# Tokenizer initialization
bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
gpt_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def preprocess_data(data):
    """Tokenize and prepare data for model training."""
    bert_inputs = [bert_tokenizer(text, return_tensors="pt") for text in data["questions"]]
    gpt_inputs = [gpt_tokenizer(text, return_tensors="pt") for text in data["answers"]]
    return bert_inputs, gpt_inputs

def preprocess_for_gpt(data):
    """Preprocess data for GPT by tokenizing questions and answers."""
    tokenized_data = [gpt_tokenizer(text, padding="max_length", truncation=True, return_tensors="pt") for text in data]
    return tokenized_data

def clean_text(text):
    """Remove unwanted characters, stop words, and other noise from text."""
    # Simple example for demonstration purposes
    text = text.lower()
    text = text.replace("\n", " ").replace("\r", "")
    # Further cleaning steps can be added here
    return text


def fine_tune_bert_retriever(data, labels):
    """Fine-tune BERT for retrieving relevant answers based on similarity."""
    model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=8,
        num_train_epochs=3,
        logging_dir="./logs",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=data,
        eval_dataset=labels,
    )

    trainer.train()
    return model



def fine_tune_gpt_generator(data):
    """Fine-tune GPT to generate responses based on retrieved context."""
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    training_args = TrainingArguments(
        output_dir="./gpt_results",
        per_device_train_batch_size=4,
        num_train_epochs=3,
        logging_dir="./gpt_logs",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=data,
    )

    trainer.train()
    return model
