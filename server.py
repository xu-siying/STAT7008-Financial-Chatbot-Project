from flask import Flask, render_template, jsonify, request, session
from app.chatbot import Chatbot
from transformers import BertForSequenceClassification, GPT2LMHeadModel

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session management

# Load models for chatbot (ensure you have them available or trained)
bert_retriever_model = BertForSequenceClassification.from_pretrained("bert-base-uncased")
gpt_generator_model = GPT2LMHeadModel.from_pretrained("gpt2")
chatbot = Chatbot(bert_retriever_model, gpt_generator_model)

@app.route("/")
def index():
    """Render the main UI."""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle user chat input and return the chatbot response."""
    data = request.get_json()
    user_input = data.get("message", "").strip()
    
    # Check if this is the user's first message
    is_first_time = "chat_history" not in session
    if is_first_time:
        session["chat_history"] = []
        
    # Get chatbot response
    response = chatbot.process_query(user_input, is_first_time=is_first_time)
    
    
    # Update chat history
    session["chat_history"].append({"user": user_input, "bot": response})
    return jsonify({"reply": response})


if __name__ == "__main__":
    app.run(debug=True)
