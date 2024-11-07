import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from config import KAGGLE_API_KEY, KAGGLE_USER

def get_stock_data(ticker, start_date, end_date):
    """Fetch stock data from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    stock_data = stock.history(start=start_date, end=end_date)
    stock_data.to_csv(f"data/raw/{ticker}_stock_data.csv")
    print(f"Stock data for {ticker} saved.")
    return stock_data

def get_jpmorgan_product_data():
    """Scrape product data from JPMorgan Chase's website."""
    url = "https://www.jpmorganchase.com/solutions"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    products = []

    # Example selector - find product titles and descriptions
    for product_section in soup.find_all("section", class_="product"):
        title = product_section.find("h2").get_text(strip=True)
        description = product_section.find("p").get_text(strip=True)
        products.append({"title": title, "description": description})

    df = pd.DataFrame(products)
    df.to_csv("data/raw/jpmorgan_products.csv", index=False)
    print("JPMorgan product data saved.")
    return df

def get_bankofamerica_product_data():
    """Scrape product data from Bank of America's website."""
    url = "https://www.bankofamerica.com/deposits/bank-accounts/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    products = []

    # Example selector - find product titles and descriptions
    for product_section in soup.find_all("div", class_="product-detail"):
        title = product_section.find("h3").get_text(strip=True)
        description = product_section.find("p").get_text(strip=True)
        products.append({"title": title, "description": description})

    df = pd.DataFrame(products)
    df.to_csv("data/raw/bankofamerica_products.csv", index=False)
    print("Bank of America product data saved.")
    return df

def get_hsbc_product_data():
    """Scrape product data from HSBC's website."""
    url = "https://www.us.hsbc.com/checking-accounts/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    products = []

    # Example selector - find product titles and descriptions
    for product_section in soup.find_all("div", class_="product"):
        title = product_section.find("h2").get_text(strip=True)
        description = product_section.find("p").get_text(strip=True)
        products.append({"title": title, "description": description})

    df = pd.DataFrame(products)
    df.to_csv("data/raw/hsbc_products.csv", index=False)
    print("HSBC product data saved.")
    return df

def fetch_kaggle_data(dataset_path, file_name):
    """Download a dataset from Kaggle."""
    kaggle_url = f"https://www.kaggle.com/{dataset_path}/download"
    headers = {"Authorization": f"Bearer {KAGGLE_API_KEY}"}
    
    response = requests.get(kaggle_url, headers=headers)
    if response.status_code == 200:
        with open(f"data/raw/{file_name}", "wb") as f:
            f.write(response.content)
        print(f"Kaggle dataset {file_name} downloaded.")
    else:
        print("Error fetching Kaggle data. Ensure API key is correct.")
