# retriever.py

from transformers import BertForSequenceClassification, Trainer, TrainingArguments, BertTokenizer
import torch

def fine_tune_bert_retriever(train_data, labels):
    """Fine-tunes BERT model for retrieving relevant answers based on similarity."""
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
        train_dataset=train_data,
        eval_dataset=labels,
    )

    trainer.train()
    return model


def retrieve_context(query, documents, retriever_model, tokenizer):
    # Tokenize the query
    query_inputs = tokenizer(query, return_tensors="pt", truncation=True, padding=True)

    similarity_scores = []
    for doc in documents:
        # Tokenize each document
        doc_inputs = tokenizer(doc, return_tensors="pt", truncation=True, padding=True)

        # Use the model to compute similarity score (e.g., logits)
        with torch.no_grad():  # Disable gradients for inference
            logits = retriever_model(**query_inputs).logits  # Remove labels if logits are sufficient

        # Select the first element, average, or max as the similarity score if there are multiple logits
        similarity_score = logits[0].item() if logits.numel() == 1 else logits[0].max().item()
        similarity_scores.append(similarity_score)

    # Find the document with the highest similarity score
    best_match_index = torch.argmax(torch.tensor(similarity_scores))
    return documents[best_match_index]