from flask import request, jsonify, session

def handle_chat(chatbot):
    """Handle user chat input."""
    data = request.get_json()
    user_input = data.get("message", "").strip()
    
     # Check for the initial greeting keyword
    if user_input.lower() == "greetings!":
        response = "Welcome! I’m here to assist with your financial queries."
        return jsonify({"reply": response})

    
    # Process user query
    try:
        response = chatbot.process_query(user_input, is_first_time=False)
    except Exception as e:
        response = f"An error occurred: {str(e)}"

    # Save conversation to session
    session["chat_history"].append({"user": user_input, "bot": response})
    print(response)
    return jsonify({"reply": response})
