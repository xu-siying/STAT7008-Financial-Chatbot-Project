from app.controllers.chat_controller import handle_chat
from flask import Flask, render_template, jsonify, request, session
from flask_session import Session
from redis import Redis
from transformers import GPT2LMHeadModel
from sentence_transformers import SentenceTransformer
from app.chatbot import Chatbot
import pinecone
from flask_sqlalchemy import SQLAlchemy
import logging

# Flask app configuration
app = Flask(__name__)

app.config.from_pyfile("config.py")

app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "chatbot:"
app.config["SESSION_REDIS"] = Redis(host="localhost", port=6379)
Session(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatbot.db"
db = SQLAlchemy(app)

# Initialize Pinecone
pinecone_api_key = "pcsk_3NsehX_3L9RCJNQkBpEginwn9w6JYBS65LDgKrbQ5Jdxe8a1dKyZeV5Pbr116bBYoCsPr5"
index_name = "financial-index"

pinecone_environment = "us-east-1"


# Initialize Pinecone
pc = pinecone.Pinecone(api_key=pinecone_api_key)

# Check if the index exists
if index_name not in pc.list_indexes().names():
    index = pinecone.create_index(
    name=index_name,
    dimension=384,
    metric="cosine",
    spec=pinecone.ServerlessSpec(
        cloud="aws",  # Replace with your cloud provider
        region="us-east-1"  # Replace with your region
    )
)
    print(f"Error: The index '{index_name}' does not exist.")
else:
    # Connect to the existing index
    index = pc.Index(index_name)
    print(f"Connected to existing index: {index_name}")

    # Example: Perform operations with the index
    print(f"Index details: {index.describe_index_stats()}")


# Load models for chatbot
try:
    gpt_generator_model = GPT2LMHeadModel.from_pretrained("gpt2-large")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception as e:
    raise RuntimeError(f"Error loading models: {e}")

# Initialize chatbot
chatbot = Chatbot(
    gpt_model_name="gpt2-large",
    pinecone_index=index,
    embedding_model_name="all-MiniLM-L6-v2"
)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(500))
    bot_response = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# Initialize database
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    """Render the main UI."""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle user chat input and return the chatbot response."""
    return handle_chat(chatbot)

@app.route("/history", methods=["GET"])
def history():
    """Retrieve chat history from the database."""
    history = ChatHistory.query.order_by(ChatHistory.timestamp).all()
    return jsonify([{"user": h.user_message, "bot": h.bot_response, "timestamp": h.timestamp} for h in history])

# # Query example
# @app.route("/query", methods=["POST"])
# def query_index():
#     """Query the Pinecone index."""
#     data = request.json
#     if not data or "vector" not in data:
#         return jsonify({"error": "Invalid request. Provide 'vector' field."}), 400

#     query_vector = data["vector"]
#     try:
#         # Query the index
#         results = index.query(vector=query_vector, top_k=10)
#         logging.basicConfig(level=logging.DEBUG)

#         logging.debug(f"Query vector: {query_vector}")
#         logging.debug(f"Pinecone results: {results}")
#         return jsonify({"results": results})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
    




if __name__ == "__main__":
    app.run(debug=True)
