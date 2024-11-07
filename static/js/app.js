// app.js

document.addEventListener("DOMContentLoaded", function() {
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const sendButton = document.getElementById("sendButton");
    const emotionButton = document.getElementById("emotionButton");
    const emotionContainer = document.getElementById("emotion-container");
    const video = document.getElementById("video");
    const captureButton = document.getElementById("captureButton");
    let stream;

    // Start emotion detection
    emotionButton.addEventListener("click", async () => {
        emotionContainer.style.display = "flex";
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    });

    // Capture emotion when button is clicked
    captureButton.addEventListener("click", () => {
        captureEmotion();
    });

    // Function to capture emotion
    async function captureEmotion() {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL("image/png");

        try {
            const response = await fetch("/api/emotion", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ image: imageData })
            });

            if (response.ok) {
                const data = await response.json();
                addChatbotMessage("Detected emotion: " + data.emotion);
            } else {
                addChatbotMessage("Could not detect emotion. Try again.");
            }
        } catch (error) {
            console.error("Error:", error);
            addChatbotMessage("Error connecting to the server.");
        }
    }

    // Handle sending chat messages
    sendButton.addEventListener("click", () => {
        const message = userInput.value.trim();
        if (message) {
            addUserMessage(message);
            sendMessageToChatbot(message);
            userInput.value = "";
        }
    });

    // Additional functions (addUserMessage, addChatbotMessage, sendMessageToChatbot) here...
    // Handle 'Enter' key for sending messages
    userInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            sendButton.click();
        }
    });

    // Function to add user message to chat
    function addUserMessage(message) {
        const userMessage = document.createElement("div");
        userMessage.className = "user-message";
        userMessage.textContent = "You: " + message;
        chatBox.appendChild(userMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Function to add chatbot message to chat
    function addChatbotMessage(message) {
        const botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.textContent = "Bot: " + message;
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Function to send user message to the chatbot server
    async function sendMessageToChatbot(message) {
        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message })
            });

            if (response.ok) {
                const data = await response.json();
                addChatbotMessage(data.reply);
            } else {
                addChatbotMessage("Error: Could not get a response from the bot.");
            }
        } catch (error) {
            console.error("Error:", error);
            addChatbotMessage("Error connecting to the server.");
        }
    }
});

