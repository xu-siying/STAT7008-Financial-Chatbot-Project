from flask import request, jsonify, session

def handle_chat(chatbot):
    """Handle user chat input."""
    data = request.get_json()
    user_input = data.get("message", "").strip()

    # Check for first-time usage
    is_first_time = "chat_history" not in session
    if is_first_time:
        session["chat_history"] = []

    # Process user query
    try:
        response = chatbot.process_query(user_input, is_first_time=is_first_time)
    except Exception as e:
        response = f"An error occurred: {str(e)}"

    # Save conversation to session
    session["chat_history"].append({"user": user_input, "bot": response})
    return jsonify({"reply": response})
