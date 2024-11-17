import time
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import kagglehub
import random

import datetime

import json


import os
import json
import pandas as pd
import yfinance as yf

def get_stock_data(ticker, output_file="data/processed/stock_data.json"):
    """Fetch and preprocess stock data from Yahoo Finance and save to a JSON file."""
    try:
        # Fetch stock data
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period="1y")

        # Check for empty data
        if stock_data.empty:
            raise ValueError(f"No stock data available for ticker {ticker}.")

        # Reset index and convert 'Date' to string
        stock_data.reset_index(inplace=True)
        stock_data["Date"] = stock_data["Date"].dt.strftime("%Y-%m-%d")

        # Add derived features
        stock_data["Daily_Return"] = (stock_data["Close"] - stock_data["Open"]) / stock_data["Open"]
        stock_data["7-Day_MA"] = stock_data["Close"].rolling(window=7).mean()
        stock_data["30-Day_MA"] = stock_data["Close"].rolling(window=30).mean()

       
        stock_data.dropna(subset=["7-Day_MA", "30-Day_MA"], inplace=True)

        # Convert DataFrame to JSON-serializable format
        processed_data = stock_data.to_dict(orient="records")

        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save to JSON file
        with open(output_file, "w") as f:
            json.dump(processed_data, f, indent=4)

        print(f"Processed stock data for {ticker} saved to {output_file}")
        return processed_data

    except Exception as e:
        print(f"Error fetching and processing stock data for {ticker}: {e}")
        return None



# Fetch financial news using NewsAPI
def fetch_newsapi_financial_news(api_key):
    """Fetch financial news using NewsAPI and return JSON."""
    url = f"https://newsapi.org/v2/everything?q=finance&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if "articles" not in data:
        raise ValueError("No articles found in the NewsAPI response.")
    
    # Add metadata to the output
    output = {
        "source": "NewsAPI",
        "fetched_at": datetime.datetime.now().isoformat(),
        "articles": data["articles"]  # Directly include the articles list
    }
    return output





# def fetch_kaggle_data(dataset_name, file_name, output_dir="data/raw/"):
    
#     """
#     Use kagglehub to fetch Kaggle datasets.
#     dataset_name: The Kaggle dataset identifier, e.g., 'samira1992/bank-loan-intermediate-dataset'
#     output_dir: Directory to save the downloaded data.
#     """
#     # Ensure output directory exists
#     os.makedirs(output_dir, exist_ok=True)
    
#     # Download dataset with kagglehub
#     try:
#         dataset_path = kagglehub.dataset_download(dataset_name)
#         print(f"Dataset downloaded to cache: {dataset_path}")

#         # Copy the files to the output directory
#         for file_name in os.listdir(dataset_path):
#             file_path = os.path.join(dataset_path, file_name)
#             if os.path.isfile(file_path):
#                 destination = os.path.join(output_dir, file_name)
#                 os.rename(file_path, destination)
#                 print(f"Moved {file_path} to {destination}")

#         return output_dir

#     except Exception as e:
#         print(f"Error fetching dataset {dataset_name}: {e}")
#         return None

  



# def fetch_financial_news():
#     """Scrape financial news from CNBC and return JSON."""
#     url = "https://www.cnbc.com/world/?region=world"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")

#     news_items = []
#     for headline in soup.find_all("a", class_="LatestNews-headline"):
#         title = headline.get_text(strip=True)
#         link = headline.get("href")
#         news_items.append({"title": title, "link": link})

#     output = {
#         "source": "CNBC",
#         "fetched_at": datetime.datetime.now().isoformat(),
#         "articles": news_items
#     }
#     return output


def scrape_investopedia_topic(topic_url):
    """Scrape all articles linked on a given Investopedia topic page."""
    try:
        response = requests.get(topic_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise an error for HTTP issues
    except Exception as e:
        print(f"Error accessing {topic_url}: {e}")
        return {
            "source": "Investopedia",
            "topic_url": topic_url,
            "fetched_at": datetime.datetime.now().isoformat(),
            "articles": []
        }

    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all article links on the topic page
    articles = []
    for a_tag in soup.select("a.mntl-document-card[href]"):
        article_url = a_tag["href"]
        if not article_url.startswith("http"):
            article_url = "https://www.investopedia.com" + article_url  # Ensure full URL
        print(f"Found article URL: {article_url}")  # Debugging output
        
        try:
            # Fetch article content
            article_content = scrape_investopedia_article(article_url)
            articles.append(article_content)
            time.sleep(random.uniform(1, 2))  # Delay to avoid being flagged
        except Exception as e:
            print(f"Error scraping article {article_url}: {e}")
            continue

    return {
        "source": "Investopedia",
        "topic_url": topic_url,
        "fetched_at": datetime.datetime.now().isoformat(),
        "articles": articles
    }


def scrape_investopedia_article(article_url):
    try:
        response = requests.get(article_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except Exception as e:
        print(f"Error accessing article {article_url}: {e}")
        return {"url": article_url, "title": None, "content": None}

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract article title
    title = soup.find("h1").text.strip() if soup.find("h1") else "No Title"

    # Extract article content
    paragraphs = soup.find_all("p")
    content = " ".join([p.text.strip() for p in paragraphs]) if paragraphs else "No Content"

    return {"url": article_url, "title": title, "content": content}





