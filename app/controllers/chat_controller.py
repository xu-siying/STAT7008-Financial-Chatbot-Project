# chat_controller.py

from flask import request, jsonify, session
from app.chatbot import Chatbot

chatbot = Chatbot()

def handle_chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    # Check if this is the user's first time or if they have no chat history
    is_first_time = "chat_history" not in session
    if is_first_time:
        # Initialize chat history for new user
        session["chat_history"] = []

    # Generate response using Chatbot, passing is_first_time flag
    response = chatbot.process_query(user_input, is_first_time=is_first_time)

    # Append conversation to chat history and save to session
    session["chat_history"].append({"user": user_input, "bot": response})
    return jsonify({"reply": response})
