import os
import json
from sentence_transformers import SentenceTransformer
import pinecone

# Load JSON data
def load_json(file_path):
    """
    Load JSON data from a file.

    :param file_path: Path to the JSON file.
    :return: Parsed JSON data.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file {file_path}: {e}")
        return None


# Initialize Pinecone
def initialize_pinecone(api_key, environment, index_name, dimension):
    pc = pinecone.Pinecone(api_key=api_key)
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=pinecone.ServerlessSpec(cloud="aws", region=environment),
        )
        print(f"Created Pinecone index: {index_name}")
        # Get index statistics
    
    return pc.Index(index_name)

def insert_stock_data(data, model, index):
    """
    Process stock data (either from a JSON file or preloaded data) and upsert it into Pinecone.

    :param data: Either a file path to the JSON data or a list of dictionaries.
    :param model: The model used to generate embeddings.
    :param index: The Pinecone index to upsert data into.
    """
    try:
        # Load data if a file path is provided
        if isinstance(data, str):  # Check if it's a file path
            with open(data, "r") as f:
                data = json.load(f)  # Load JSON data as a list of dictionaries
            
        # Ensure the data is a list of dictionaries
        if not isinstance(data, list):
            raise ValueError(f"Expected a list of dictionaries, but got {type(data).__name__}")
        
        for record in data:
            # Ensure the record has required fields
            if "Close" in record and "Date" in record:
                try:
                    # Generate embedding
                    vector = model.encode(f"The stock close price is {record['Close']}")

                    # Upsert into Pinecone
                    index.upsert([{
                        "id": record["Date"],  # Use Date as a unique identifier
                        "values": vector,
                        "metadata": {
                            "open": record.get("Open"),
                            "high": record.get("High"),
                            "low": record.get("Low"),
                            "close": record.get("Close"),
                            "volume": record.get("Volume"),
                            "daily_return": record.get("Daily_Return"),
                            "7-day_ma": record.get("7-Day_MA"),
                            "30-day_ma": record.get("30-Day_MA"),
                            "summary": f"The stock closed at {record.get('Close')} on {record.get('Date')}, "
                                       f"with a high of {record.get('High')} and a low of {record.get('Low')}."
                        }
                    }])

                    print(f"Processed record for date: {record['Date']}")
                except Exception as e:
                    print(f"Error processing record {record['Date']}: {e}")
            else:
                print(f"Skipping record due to missing required fields: {record}")
    except FileNotFoundError as fnf_error:
        print(f"File not found: {data}")
    except json.JSONDecodeError as json_error:
        print(f"Error decoding JSON in file {data}: {json_error}")
    except Exception as e:
        print(f"Unexpected error processing {data}: {e}")

# Insert embeddings for cleaned articles
def insert_cleaned_articles(json_data, index, model):
    for article in json_data.get("articles", []):
        if "content" in article and "url" in article:
            # Generate embedding from content
            embedding = model.encode(article["content"]).tolist()
            
            # Build metadata with additional fields
            metadata = {
                "url": article["url"],
                "title": article.get("title"),
                "summary": article.get("summary", ""),
                "content": article.get("content"),
                "keywords": article.get("keywords", []),
                "sentiment": article.get("sentiment"),
                "category": article.get("category")
            }

            # Upsert article into Pinecone
            index.upsert([{
                "id": article["url"],  # Use the URL as a unique ID
                "values": embedding,
                "metadata": metadata
            }])
            print(f"Inserted article: {metadata['title'] or 'No Title'}")


# Insert embeddings for news articles
def insert_news_articles(json_data, index, model):
    for article in json_data.get("articles", []):
        if "title" in article and "url" in article:
            # Generate embedding from the title
            embedding = model.encode(article["title"]).tolist()

            # Build metadata with additional fields
            metadata = {
                "url": article["url"],
                "title": article.get("title"),
                "summary": article.get("summary", ""),
                "keywords": article.get("keywords", []),
                "sentiment": article.get("sentiment"),
                "category": article.get("category")
            }

            # Upsert article into Pinecone
            index.upsert([{
                "id": article["url"],  # Use the URL as a unique ID
                "values": embedding,
                "metadata": metadata
            }])
            print(f"Inserted news article: {metadata['title']}")


def process_json_files(directory, index, model):
    """
    Process all JSON files in a given directory and insert embeddings into Pinecone.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {file_path}")
            try:
                json_data = load_json(file_path)

                # Determine the type of data and process accordingly
                if isinstance(json_data, list) and "Date" in json_data[0]:  # Stock data
                    insert_stock_data(json_data, model, index)
                elif "articles" in json_data and "source" in json_data:  # Articles
                    if "title" in json_data["articles"][0]:  # News articles
                        insert_news_articles(json_data, index, model)
                    elif "content" in json_data["articles"][0]:  # Cleaned articles
                        insert_cleaned_articles(json_data, index, model)
                else:
                    print(f"Unrecognized data format in file: {file_path}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

# Fetch and validate vectors after insertion
def validate_index(index, sample_ids):
    print("Validating data in Pinecone index...")
    results = index.fetch(ids=sample_ids)
    for vector_id, data in results["vectors"].items():
        print(f"ID: {vector_id}")
        print(f"Metadata: {data.get('metadata', 'No metadata found')}")


# Main function
def main():
    # Pinecone configuration
    api_key = "pcsk_3NsehX_3L9RCJNQkBpEginwn9w6JYBS65LDgKrbQ5Jdxe8a1dKyZeV5Pbr116bBYoCsPr5"
    environment = "us-east-1"  
    index_name = "financial-index"
    dimension = 384  # Adjust based on your embedding model

    # Initialize Pinecone and model
    index = initialize_pinecone(api_key, environment, index_name, dimension)
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Adjust based on your embedding model



    # Process all JSON files in the directory
    directory = "data/processed"
    process_json_files(directory, index, model)
    
    # Validate some stock data
    sample_ids = ["2023-11-15", "2023-11-16"]  # Replace with actual dates in your dataset
    validate_index(index, sample_ids)
    
   

if __name__ == "__main__":
    main()

