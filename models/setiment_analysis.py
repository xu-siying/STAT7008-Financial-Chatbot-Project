from transformers import BertTokenizer, BertForSequenceClassification
import torch
from textblob import TextBlob

# Initialize BERT components for sentiment analysis
tokenizer = BertTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = BertForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment_query(query):
    """Analyze sentiment of the user query to detect tone."""
    inputs = tokenizer(query, return_tensors="pt")
    outputs = model(**inputs)
    sentiment_class = torch.argmax(outputs.logits, dim=1).item()
    sentiments = ["very negative", "negative", "neutral", "positive", "very positive"]
    return sentiments[sentiment_class]




def analyze_sentiment_content(content):
    """
    Perform sentiment analysis on the content.
    
    content: Text content of the article.
    Returns: Sentiment polarity (negative < 0, neutral = 0, positive > 0)
    """
    blob = TextBlob(content)
    sentiment = blob.sentiment.polarity
    return "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral"

