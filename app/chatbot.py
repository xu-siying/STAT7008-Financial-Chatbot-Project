# import imp
# from models.keyword_extraction import lda_topic_modeling, tfidf_keyword_extraction, word2vec_embedding
# from models.classification import naive_bayes_classification, bert_classification
# from models.similarity import cosine_similarity_matching, siamese_network_similarity
from transformers import BertForSequenceClassification, BertTokenizer,GPT2LMHeadModel, GPT2Tokenizer
from models.dialogue_prediction import gpt_based_prediction
from models.emotion_detection import detect_emotion
from models.setiment_analysis import analyze_sentiment
# from models.keyword_extraction import extract_keywords
# from models.classification import classify_query
from models.retriever import retrieve_context, fine_tune_bert_retriever
from models.response_generation import generate_response, fine_tune_gpt_generator
from models.model_preprocessing import preprocess_for_gpt
from models.dialogue_prediction import gpt_based_prediction
from models.retriever import retrieve_context 
import random


class Chatbot:
    def __init__(self, bert_retriever_model, gpt_generator_model):
        # Initialize BERT-based retriever
        self.bert_retriever = bert_retriever_model
        
        # Initialize GPT-2 tokenizer and generator for response generation
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2-large")
        self.tokenizer.pad_token = self.tokenizer.eos_token  # Set pad token to eos token if needed
        self.gpt_generator = gpt_generator_model
        self.gpt_generator.config.pad_token_id = self.tokenizer.pad_token_id  # Set pad_token_id in model config
        
        # Load knowledge base
        self.documents = self.load_documents()
        self.context = None

    def load_documents(self):
        """Load documents from a file or database as the knowledge base."""
        return [
            "Investing in stocks can provide high returns over a long period.",
            "Savings accounts provide a secure way to store your funds while earning interest.",
            "Loans provide funds upfront and are repaid over time with interest.",
            # Additional documents from your financial dataset
        ]

    def get_random_welcome_message(self):
        """Return a random welcome message."""
        welcome_messages = [
            "Hello! I'm InvestoBot, your financial assistant. How can I help you today?",
            "Welcome to InvestoBot! I’m here to assist with all your financial queries.",
            "Hi there! I’m InvestoBot, ready to help you with investments, loans, and savings advice."
        ]
        return random.choice(welcome_messages)

    def adjust_tone_based_on_emotion_and_sentiment(self, response, emotion, sentiment):
        """Adjust the chatbot response based on detected emotion and sentiment."""
        if emotion == "happy" or sentiment == "positive":
            return f"{response} 😊 I'm glad to help you with this!"
        elif emotion == "sad" or sentiment == "negative":
            return f"I'm here for you. {response} Let me know if there’s more I can assist you with."
        elif emotion == "angry":
            return f"I understand that this might be frustrating. {response} Let's work together to find a solution."
        elif emotion == "surprise":
            return f"That's an interesting reaction! {response} Is there anything specific you want to know more about?"
        else:
            return response  # Neutral response with no adjustment

    def process_query(self, query, video_frame=None, is_first_time=False):
        """Generate response and handle conversation flow with emotion-based adjustments."""
        
        # Handle first-time user welcome
        if is_first_time:
            self.context = None
            return self.get_random_welcome_message()

        # Step 1: Retrieve relevant context from documents
        context = retrieve_context(query, self.documents, self.bert_retriever, self.tokenizer)

        # Step 2: Generate a response using GPT-2 based on query and retrieved context
        response = generate_response(query, context, self.gpt_generator, self.tokenizer)

        # Step 3: Analyze sentiment based on user input
        sentiment = analyze_sentiment(query)
        
        # Step 4: Detect emotion from video frame if provided and adjust tone
        if video_frame is not None:
            emotion = detect_emotion(video_frame)
            response = self.adjust_tone_based_on_emotion_and_sentiment(response, emotion, sentiment)
            return f"I detected {emotion} in your expression. {response}"

        # Step 5: Conversation Prediction (suggests next topic)
        next_conversation = gpt_based_prediction(query)
        response += f" If you’re interested, we could discuss: {next_conversation}"

        # Return the final response
        return response