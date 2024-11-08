import pandas as pd
from sentence_transformers import SentenceTransformer
import os

def load_data(file_paths):
    """Load data from given file paths, checking for 'description' column in each file."""
    combined_data = []
    for file_path in file_paths:
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
            if 'description' in data.columns:
                combined_data.extend(data['description'].fillna('').tolist())
            elif 'title' in data.columns:
                # Fall back to 'title' if 'description' is not available
                combined_data.extend(data['title'].fillna('').tolist())
                print(f"Note: Using 'title' column instead of 'description' in {file_path}")
            else:
                print(f"Warning: Neither 'description' nor 'title' found in {file_path}")
        else:
            print(f"File not found: {file_path}")
    return combined_data

def embed_and_save_products(model_name="all-MiniLM-L6-v2", output_path="data/processed/financial_embeddings.csv"):
    """Create embeddings for financial products and news data."""
    model = SentenceTransformer(model_name)
    
    # Load data files
    file_paths = [
        "data/processed/financial_news.csv",
        "data/processed/newsapi_finance_news.csv",
        "data/raw/symbols_valid_meta.csv",
        "data/raw/consumer_complaints.csv",
        "data/raw/Bank_Personal_Loan_Modelling.csv",
        "data/raw/investing_program_prediction_data.csv"
    ]
    
    descriptions = load_data(file_paths)
    
    # Generate embeddings
    if descriptions:
        print("Generating embeddings for descriptions...")
        embeddings = model.encode(descriptions, show_progress_bar=True)
        
        # Save embeddings
        embeddings_df = pd.DataFrame(embeddings)
        embeddings_df['description'] = descriptions
        embeddings_df.to_csv(output_path, index=False)
        print(f"Embeddings saved to {output_path}")
    else:
        print("No data available for embedding.")

if __name__ == "__main__":
    embed_and_save_products()
