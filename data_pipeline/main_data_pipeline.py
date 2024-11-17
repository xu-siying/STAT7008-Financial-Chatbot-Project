
from genericpath import exists
from data_fetch import (
    get_stock_data,
    fetch_newsapi_financial_news,

    scrape_investopedia_topic
)
from data_preprocessing import preprocess_text, process_articles_data
import os
import json


def save_to_json(data, file_path):
    """Save data to a JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {file_path}")


def main():
    # Set up directories
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # Fetch stock data for a given ticker and save as JSON
    ticker = "AAPL"
    stock_data_path = f"data/processed/{ticker}_stock_data.json"
    if not os.path.exists(stock_data_path):
        stock_data = get_stock_data(ticker,stock_data_path)
        save_to_json(stock_data, stock_data_path)
    
    

    # # Fetch additional Kaggle datasets and save as JSON
    # kaggle_datasets = {
    #     "samira1992/bank-loan-intermediate-dataset": "Bank_Personal_Loan_Modelling.csv",
    #     "snassimr/data-for-investing-type-prediction": "investing_program_prediction_data.csv",
    #     "jacksoncrow/stock-market-dataset": "symbols_valid_meta.csv",
    #     "kaggle/us-consumer-finance-complaints": "consumer_complaints.csv"
    # }
    
    # output_dir = "data/processed"
    # for dataset, file_name in kaggle_datasets.items():
    #     print(f"Fetching dataset: {dataset}")
    #     fetch_kaggle_data(dataset, output_dir)

    # Fetch financial news from CNBC and preprocess titles
    # financial_news_path = "data/raw/financial_news.json"
    # if not os.path.exists(financial_news_path):
    #     financial_news = fetch_financial_news()
    #     save_to_json(financial_news, financial_news_path)
    # else:
    #     with open(financial_news_path, "r") as f:
    #         financial_news = json.load(f)
    # # Preprocess titles
    # for item in financial_news["articles"]:
    #     item["title"] = preprocess_text(item["title"])
    # save_to_json(financial_news, "data/processed/financial_news.json")

    # Fetch NewsAPI financial news and preprocess titles
    news_api_key = "c5aedc0ebd604efba2247e958a96ff8b"
    newsapi_path = "data/raw/newsapi_financial_news.json"
    if news_api_key and not os.path.exists(newsapi_path):
        newsapi_data = fetch_newsapi_financial_news(news_api_key)
        for item in newsapi_data["articles"]:
            item["title"] = preprocess_text(item["title"])
        save_to_json(newsapi_data, "data/raw/newsapi_financial_news.json")

    # Scrape Investopedia articles and save as JSON
    investopedia_topics = [
        "https://www.investopedia.com/investing-4427685",
        "https://www.investopedia.com/stocks-4427785",
        "https://www.investopedia.com/bonds-4689778",
        "https://www.investopedia.com/budgeting-and-savings-4427755",
        "https://www.investopedia.com/personal-loans-4689729",
        "https://www.investopedia.com/student-loans-4689727",
        "https://www.investopedia.com/savings-accounts-4689728",
        "https://www.investopedia.com/cryptocurrency-4427699",
        "https://www.investopedia.com/etfs-4427784",
        "https://www.investopedia.com/financial-technology-and-automated-investing-4689759" 
    ]
    for topic_url in investopedia_topics:
        topic_name = topic_url.split("/")[-1].split("-")[0]
        investopedia_path = f"data/raw/{topic_name}_articles.json"
        
        print(f"Checking file: {investopedia_path}")
        if os.path.exists(investopedia_path):
            print(f"Topic already fetched: {topic_name}. Skipping.")
            continue
           
        articles = scrape_investopedia_topic(topic_url)
        save_to_json(articles, investopedia_path)

    # Directories for raw and processed data
    raw_investopedia_dir = "data/raw/"
    processed_investopedia_dir = "data/processed/"

    # Process Investopedia data
    process_articles_data(raw_investopedia_dir, processed_investopedia_dir)

    # # Generate embeddings for processed product descriptions and news
    # embed_and_save_products()
    # print("Data fetching, processing, and embedding complete.")


if __name__ == "__main__":
    main()
