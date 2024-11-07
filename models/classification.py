from sklearn.naive_bayes import MultinomialNB
from transformers import BertTokenizer, BertForSequenceClassification
import torch

def naive_bayes_classification(X_train, y_train):
    model = MultinomialNB()
    model.fit(X_train, y_train)
    return model

def bert_classification(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    return outputs
