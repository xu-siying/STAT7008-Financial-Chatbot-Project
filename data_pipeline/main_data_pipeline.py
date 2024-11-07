from data_pipeline.data_fetch import (
    get_stock_data,
    get_jpmorgan_product_data,
    get_bankofamerica_product_data,
    get_hsbc_product_data,
    fetch_kaggle_data
)
from data_pipeline.data_preprocessing import preprocess_text
import os
import pandas as pd

def main():
    # Fetch and process stock data
    ticker = "AAPL"
    stock_data_path = f"data/raw/{ticker}_stock_data.csv"
    if not os.path.exists(stock_data_path):
        stock_data = get_stock_data(ticker, "2022-01-01", "2022-12-31")
    else:
        stock_data = pd.read_csv(stock_data_path)

    # Fetch and process JPMorgan products
    jpmorgan_data_path = "data/raw/jpmorgan_products.csv"
    if not os.path.exists(jpmorgan_data_path):
        jpmorgan_products = get_jpmorgan_product_data()
    else:
        jpmorgan_products = pd.read_csv(jpmorgan_data_path)
    jpmorgan_products['description'] = jpmorgan_products['description'].apply(preprocess_text)

    # Fetch and process Bank of America products
    boa_data_path = "data/raw/bankofamerica_products.csv"
    if not os.path.exists(boa_data_path):
        boa_products = get_bankofamerica_product_data()
    else:
        boa_products = pd.read_csv(boa_data_path)
    boa_products['description'] = boa_products['description'].apply(preprocess_text)

    # Fetch and process HSBC products
    hsbc_data_path = "data/raw/hsbc_products.csv"
    if not os.path.exists(hsbc_data_path):
        hsbc_products = get_hsbc_product_data()
    else:
        hsbc_products = pd.read_csv(hsbc_data_path)
    hsbc_products['description'] = hsbc_products['description'].apply(preprocess_text)

    # Fetch and process Kaggle financial data
    kaggle_data_path = "data/raw/finance_data.csv"
    if not os.path.exists(kaggle_data_path):
        fetch_kaggle_data("nitindatta/finance-data", "finance_data.csv")
    kaggle_data = pd.read_csv(kaggle_data_path)

    # Save processed data
    jpmorgan_products.to_csv("data/processed/jpmorgan_products.csv", index=False)
    boa_products.to_csv("data/processed/bankofamerica_products.csv", index=False)
    hsbc_products.to_csv("data/processed/hsbc_products.csv", index=False)
    kaggle_data.to_csv("data/processed/processed_kaggle_data.csv", index=False)

if __name__ == "__main__":
    main()
