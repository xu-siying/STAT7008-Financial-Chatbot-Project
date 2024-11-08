from transformers import GPT2Tokenizer, GPT2LMHeadModel
from sentence_transformers import SentenceTransformer
from models.dialogue_prediction import gpt_based_prediction
from models.emotion_detection import detect_emotion
from models.setiment_analysis import analyze_sentiment
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import random

class Chatbot:
    def __init__(self, bert_retriever_model, gpt_generator_model, knowledge_base_path="data_pipeline/data/processed/financial_embeddings.csv"):
        # Initialize BERT-based retriever for context retrieval
        self.bert_retriever = bert_retriever_model
        
        # Initialize GPT-2 tokenizer and generator for response generation
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2-large")
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.gpt_generator = gpt_generator_model
        self.gpt_generator.config.pad_token_id = self.tokenizer.pad_token_id
        
        # Initialize the embedding model (Sentence-BERT)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load the knowledge base with precomputed embeddings
        self.knowledge_base = self.load_knowledge_base(knowledge_base_path)

    def load_knowledge_base(self, path):
        """Load the embedded knowledge base."""
        knowledge_base =  pd.read_csv(path)
        return knowledge_base

    def get_random_welcome_message(self):
        """Return a random welcome message."""
        welcome_messages = [
            "Hello! I'm InvestoBot, your financial assistant. How can I help you today?",
            "Welcome to InvestoBot! I’m here to assist with all your financial queries.",
            "Hi there! I’m InvestoBot, ready to help you with investments, loans, and savings advice."
        ]
        return random.choice(welcome_messages)

    def retrieve_relevant_product_info(self, query):
        """Generate embeddings for descriptions on-the-fly and retrieve the most relevant product info."""
        # Generate embedding for the query
        query_embedding = self.embedding_model.encode(query).reshape(1, -1)
    
        # Fill NaN values in descriptions with empty strings and then encode
        self.knowledge_base['description'] = self.knowledge_base['description'].fillna('')
        description_embeddings = self.knowledge_base['description'].apply(lambda desc: self.embedding_model.encode(desc)).tolist()
    
        # Stack description embeddings into an array for cosine similarity calculation
        description_embeddings = np.vstack(description_embeddings)
    
        # Calculate cosine similarity between the query and each description
        similarities = cosine_similarity(query_embedding, description_embeddings).flatten()
        best_match_index = np.argmax(similarities)
    
        # Retrieve the best match title and description
        best_match_row = self.knowledge_base.iloc[best_match_index]
        title = best_match_row['title'] if 'title' in self.knowledge_base.columns else 'Unknown Title'
        description = best_match_row['description']
    
        return title, description


    def adjust_tone_based_on_emotion_and_sentiment(self, response, emotion, sentiment):
        """Adjust the chatbot response based on detected emotion and sentiment."""
        if emotion == "happy" or sentiment == "positive":
            return f"{response} 😊 I'm glad to help you with this!"
        elif emotion == "sad" or sentiment == "negative":
            return f"I'm here for you. {response} Let me know if there’s more I can assist you with."
        elif emotion == "angry":
            return f"I understand that this might be frustrating. {response} Let's work together to find a solution."
        elif emotion == "surprise":
            return f"That's excellent! {response} Is there anything specific you want to know more about?"
        else:
            return response  # Neutral response with no adjustment

    def generate_response(self, query, context):
        """Generate response using GPT-2 with the provided context."""
        input_text = f"{context} {query}"
        inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
        
        response_ids = self.gpt_generator.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=100,
            do_sample=True,
            temperature=0.2,
            top_p=0.9,
            repetition_penalty=1.2,
            eos_token_id=self.tokenizer.pad_token_id,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        response = self.tokenizer.decode(response_ids[0], skip_special_tokens=True)
        return response

    def process_query(self, query, video_frame=None, is_first_time=False):
        """Generate response and handle conversation flow with emotion-based adjustments."""
        
        # Handle first-time user welcome
        if is_first_time:
            return self.get_random_welcome_message()

        # Retrieve context from the most relevant product info
        title, description = self.retrieve_relevant_product_info(query)
        context = f"{title}: {description}"
        
        # Generate response using GPT-2 with the context
        response = self.generate_response(query, context)
        
        # Placeholder for sentiment and emotion detection (expand as needed)
        sentiment = analyze_sentiment(query)
        if video_frame is not None:
            emotion = detect_emotion(video_frame)
            response = self.adjust_tone_based_on_emotion_and_sentiment(response, emotion, sentiment)
        
        # Optional: Suggest follow-up topics or related info based on query
        next_conversation = gpt_based_prediction(query)
        response += f" If you’re interested, we could discuss: {next_conversation}"

        return response
