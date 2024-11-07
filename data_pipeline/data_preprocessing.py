import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
from sklearn.preprocessing import StandardScaler

nltk.download("stopwords")
nltk.download("wordnet")

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

