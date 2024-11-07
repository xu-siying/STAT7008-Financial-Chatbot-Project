from flask import Flask
from app.controllers.chat_controller import handle_chat
from app.controllers.emotion_controller import analyze_emotion
from app.controllers.analytics_controller import get_dashboard_data

app = Flask(__name__)

@app.route("/api/chat", methods=["POST"])
def chat():
    return handle_chat()

@app.route("/api/emotion", methods=["POST"])
def emotion():
    return analyze_emotion()

@app.route("/api/analytics", methods=["GET"])
def analytics():
    return get_dashboard_data()

if __name__ == "__main__":
    app.run(debug=True)
