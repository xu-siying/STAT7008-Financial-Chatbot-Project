import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import kagglehub

def get_stock_data(ticker, start_date, end_date):
    """Fetch stock data from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    stock_data = stock.history(start=start_date, end=end_date)
    stock_data.to_csv(f"data/raw/{ticker}_stock_data.csv")
    print(f"Stock data for {ticker} saved.")
    return stock_data

def fetch_newsapi_financial_news(api_key):
    """Fetch latest finance-related news using NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q=finance&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    articles = [{"title": article["title"], "description": article["description"], "url": article["url"]} for article in data["articles"]]
    df = pd.DataFrame(articles)
    df.to_csv("data/raw/newsapi_finance_news.csv", index=False)
    print("NewsAPI financial news saved.")
    return df

def fetch_kaggle_data(dataset_name, file_name):
    """Download a dataset from Kaggle."""
   
    cache_path = kagglehub.dataset_download(dataset_name)
    
    # Copy downloaded files to the target directory
    source_file = os.path.join(cache_path, file_name)
    target_file = os.path.join("data/raw", file_name)
    if os.path.exists(source_file):
        os.rename(source_file, target_file)
        print(f"Kaggle dataset {file_name} moved to: {target_file}")
    else:
        print(f"Error: {file_name} not found in {cache_path}.")
    
    
    return target_file

def fetch_financial_news():
    """Scrape financial news headlines from CNBC."""
    url = "https://www.cnbc.com/world/?region=world"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    news_items = []
    for headline in soup.find_all("a", class_="LatestNews-headline"):
        title = headline.get_text(strip=True)
        link = headline.get("href")
        news_items.append({"title": title, "link": link})
    df = pd.DataFrame(news_items)
    df.to_csv("data/raw/financial_news.csv", index=False)
    print("Financial news data saved.")
    return df



