from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Initialize BERT components for sentiment analysis
tokenizer = BertTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = BertForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment(query):
    """Analyze sentiment of the user query to detect tone."""
    inputs = tokenizer(query, return_tensors="pt")
    outputs = model(**inputs)
    sentiment_class = torch.argmax(outputs.logits, dim=1).item()
    sentiments = ["very negative", "negative", "neutral", "positive", "very positive"]
    return sentiments[sentiment_class]
