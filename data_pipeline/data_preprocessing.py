import re
import nltk

# Download the punkt tokenizer locally
nltk.download()

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
from sklearn.preprocessing import StandardScaler
import json
import os
import sys
import datetime

# Add the project root directory to the Python path for import models.function into data preprocessing
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from models.classification import categorize_article
from models.keyword_extraction import extract_keywords
from models.normalization import normalize_text
from models.setiment_analysis import analyze_sentiment_content
from models.summarize import summarize_content


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\W', ' ', text)
    words = text.split()
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords.words("english")]
    return ' '.join(words)

def preprocess_categorical_data(data, columns):
    data[columns] = data[columns].fillna("Other")
    for col in columns:
        freq = data[col].value_counts(normalize=True)
        rare_categories = freq[freq < 0.05].index
        data[col] = data[col].replace(rare_categories, "Other")
    data = pd.get_dummies(data, columns=columns)
    return data

def preprocess_numerical_data(data):
    data.fillna(data.mean(), inplace=True)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    return pd.DataFrame(scaled_data, columns=data.columns)

def preprocess_time_series(data):
    data.index = pd.to_datetime(data.index)
    data = data.fillna(method='ffill')
    return data



def process_articles_data(raw_dir, processed_dir):
    os.makedirs(processed_dir, exist_ok=True)

    for raw_file in os.listdir(raw_dir):
        if raw_file.endswith("_articles.json") or raw_file.endswith("_news.json"):
            raw_file_path = os.path.join(raw_dir, raw_file)
            processed_file_path = os.path.join(processed_dir, raw_file)

            with open(raw_file_path, "r") as f:
                data = json.load(f)

            cleaned_articles = []

            for article in data.get("articles", []):
                if not article.get("title") or not article.get("content"):
                    continue

                # Normalize content
                normalized_content = normalize_text(article["content"])

                # Extract keywords
                keywords = extract_keywords(normalized_content, top_n=5)

                # Analyze sentiment
                sentiment = analyze_sentiment_content(article["content"])

                # Categorize article
                category = categorize_article(normalized_content)

                # Summarize content
                summary = summarize_content(article["content"], num_sentences=2)

                cleaned_article = {
                    "url": article["url"],
                    "title": article["title"].strip(),
                    "content": normalized_content,
                    "keywords": keywords,
                    "sentiment": sentiment,
                    "category": category,
                    "summary": summary,
                }

                cleaned_articles.append(cleaned_article)

            # Save processed data
            if raw_file.endswith("_news.json"):
                processed_data = {
                    "source": data["source"],
                    "fetched_at": data["fetched_at"],
                    "articles": cleaned_articles,
                }
            
            else:
                processed_data = {
                    "source": data["source"],
                    "topic_url": data["topic_url"],
                    "fetched_at": data["fetched_at"],
                    "articles": cleaned_articles,
                }

            with open(processed_file_path, "w") as f:
                json.dump(processed_data, f, indent=4)

            print(f"Processed file saved to {processed_file_path}")
        
