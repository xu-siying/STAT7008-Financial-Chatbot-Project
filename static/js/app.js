// app.js

document.addEventListener("DOMContentLoaded", function() {
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const sendButton = document.getElementById("sendButton");
   
    document.getElementById("user-input").addEventListener("input", function () {
        this.style.height = "auto"; // Reset height to calculate new height
        if (this.scrollHeight > 80) {
            this.style.height = "80px"; // Limit to maximum height
        }   else {
            this.style.height = this.scrollHeight + "px"; // Adjust to content height
        }
    });;

    
   // Automatically send greeting message when the chatbot is loaded
   addBotMessage("Hello! I'm your financial assistant. How can I help you today?");

   // Handle sending chat messages
   sendButton.addEventListener("click", () => {
        const message = userInput.value.trim();
        if (message) {
            addUserMessage(message);
            sendMessageToChatbot(message);
            userInput.value = ""; // Clear input field
    }
});

    // Handle 'Enter' key for sending messages
    userInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendButton.click();
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
        const userMessageContainer = document.createElement("div");
        userMessageContainer.className = "user-message-container";

        const userLabel = document.createElement("div");
        userLabel.className = "user-label";
        userLabel.textContent = "You";

        const userMessage = document.createElement("div");
        userMessage.className = "user-message";
        userMessage.textContent = message;

        userMessageContainer.appendChild(userLabel);
        userMessageContainer.appendChild(userMessage);
        chatBox.appendChild(userMessageContainer);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Handle send button click
    sendButton.addEventListener("click", function () {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message
        addUserMessage(message);

        // Clear the input field
        userInput.value = "";

        // Send user message to the chatbot
        sendMessageToChatbot(message);
    });

    // Handle 'Enter' key for sending messages
    userInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendButton.click();
        }
    });




    // Function to add bot message to chat
    function addBotMessage(message) {
        const chatBox = document.getElementById("chat-box");
        const botMessageContainer = document.createElement("div");
        botMessageContainer.className = "bot-message-container";

        const botLabel = document.createElement("div");
        botLabel.className = "bot-label";
        botLabel.textContent = "Bot";

        const botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.innerHTML = DOMPurify.sanitize(message);

        botMessageContainer.appendChild(botLabel);
        botMessageContainer.appendChild(botMessage);
        chatBox.appendChild(botMessageContainer);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    

    // Function to send user message to the chatbot server
    async function sendMessageToChatbot(message) {

        const botMessageContainer = document.createElement("div");
        botMessageContainer.className = "bot-message-container";

        const botLabel = document.createElement("div");
        botLabel.className = "bot-label";
        botLabel.textContent = "Bot";

        const loadingSpinner = document.createElement("div");
        loadingSpinner.className = "spinner";
        loadingSpinner.innerHTML = `<span></span><span></span><span></span>`;

        botMessageContainer.appendChild(botLabel);
        botMessageContainer.appendChild(loadingSpinner);
        chatBox.appendChild(botMessageContainer);
        chatBox.scrollTop = chatBox.scrollHeight;

        

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message })
            });

            console.log("Response status:", response.status);
            // Remove spinner when the response is received
            botMessageContainer.removeChild(loadingSpinner);

            if (response.ok) {
                const data = await response.json();
                console.log("Server response data:", data);
    
                // Safely remove the spinner if it exists
                const botMessage = document.createElement("div");
                botMessage.className = "bot-message";
                botMessage.innerHTML = DOMPurify.sanitize(data.reply);
                botMessageContainer.appendChild(botMessage);
     
                //addChatbotMessage(data.reply);
            } else {
                botMessageContainer.appendChild(document.createTextNode("Error: Could not get a response from the bot."));
               
            }
        } catch (error) {
            console.error("Error:", error);
            botMessageContainer.removeChild(loadingSpinner);
            botMessageContainer.appendChild(document.createTextNode("Error connecting to the server."));
        }
    }
});

