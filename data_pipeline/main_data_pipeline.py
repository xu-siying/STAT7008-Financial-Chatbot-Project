# main_data_pipeline.py
from data_fetch import (
    get_stock_data,
    fetch_newsapi_financial_news,
    fetch_kaggle_data,
    fetch_financial_news,
)
from data_preprocessing import preprocess_text
from embedding import embed_and_save_products
import os
import pandas as pd

def main():
    # Set up directories
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # Fetch stock data for a given ticker
    ticker = "AAPL"
    stock_data_path = f"data/raw/{ticker}_stock_data.csv"
    if not os.path.exists(stock_data_path):
        get_stock_data(ticker, "2022-01-01", "2022-12-31")

    # Fetch additional Kaggle datasets
    kaggle_datasets = {
        "samira1992/bank-loan-intermediate-dataset": "Bank_Personal_Loan_Modelling.csv",
        "snassimr/data-for-investing-type-prediction": "investing_program_prediction_data.csv",
        "jacksoncrow/stock-market-dataset": "symbols_valid_meta.csv",
        "kaggle/us-consumer-finance-complaints": "consumer_complaints.csv"
    }
    for dataset, file_name in kaggle_datasets.items():
        fetch_kaggle_data(dataset, file_name)

    # Fetch financial news and preprocess titles
    financial_news_path = "data/raw/financial_news.csv"
    if not os.path.exists(financial_news_path):
        financial_news = fetch_financial_news()
    else:
        financial_news = pd.read_csv(financial_news_path)
    financial_news['title'] = financial_news['title'].apply(preprocess_text)
    financial_news.to_csv("data/processed/financial_news.csv", index=False)

    # Fetch NewsAPI financial news
    news_api_key = "c5aedc0ebd604efba2247e958a96ff8b"  # replace with your key
    if news_api_key:
        newsapi_df = fetch_newsapi_financial_news(news_api_key)
        newsapi_df['title'] = newsapi_df['title'].apply(preprocess_text)
        newsapi_df.to_csv("data/processed/newsapi_finance_news.csv", index=False)

    # Generate embeddings for processed product descriptions and news
    embed_and_save_products()
    print("Data fetching, processing, and embedding complete.")

if __name__ == "__main__":
    main()
