from flask import Flask, render_template, request, jsonify
import os
import random
import json
import time
import re
from collections import defaultdict

app = Flask(__name__)

class WittyAI:
    def __init__(self):
        self.name = "Witty"
        self.conversation_history = []
        self.knowledge_base = {
            "greetings": [
                "Hello there!", "Hi! How can I help you today?", 
                "Hey! Nice to meet you.", "Greetings! How can I assist you?",
                "Hi there! How are you doing today?"
            ],
            "farewells": [
                "Goodbye! Have a nice day!", "See you later!", 
                "Bye! Come back anytime.", "Take care!", 
                "Until next time!"
            ],
            "thanks": [
                "You're welcome!", "Happy to help!", 
                "No problem at all!", "My pleasure!",
                "Anytime! That's what I'm here for."
            ],
            "about_me": [
                "I'm Witty, an AI chatbot created in December 2023.",
                "I'm a Python-based AI assistant designed to have conversations.",
                "I'm Witty! I was developed as a project to simulate human conversation.",
                "I'm an artificial intelligence chatbot built to engage in dialogue."
            ],
            "jokes": [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "What do you call a fake noodle? An impasta!",
                "I told my wife she was drawing her eyebrows too high. She looked surprised."
            ],
            "default": [
                "Interesting. Tell me more about that.",
                "I see. What else is on your mind?",
                "That's fascinating. Could you elaborate?",
                "I'm still learning, but that sounds intriguing.",
                "Tell me more about your thoughts on this."
            ],
            "how_works": [
                "I use natural language understanding to process your messages and generate appropriate responses.",
                "I analyze patterns in your text and match them to my pre-trained knowledge base.",
                "I was built using Python and NLP techniques to understand and respond to human language."
            ],
            "purpose": [
                "I was designed to simulate human conversation and provide helpful responses to your queries.",
                "My purpose is to engage in dialogue and assist users with information and conversation.",
                "I exist to provide a conversational AI experience that feels natural and helpful."
            ],
            "who_made": [
                "I was developed as a project in December 2023 using Python.",
                "I was created as an AI chatbot project to demonstrate conversational capabilities.",
                "My creators built me as part of an exploration into conversational AI technology."
            ]
        }
        
        # Patterns for matching user input
        self.patterns = {
            "greetings": r"(hello|hi|hey|howdy|greetings|good morning|good afternoon|good evening)",
            "farewells": r"(bye|goodbye|see you|farewell|exit|quit)",
            "thanks": r"(thank you|thanks|appreciate it)",
            "about_me": r"(who are you|what are you|your name|about yourself|tell me about you)",
            "jokes": r"(joke|funny|make me laugh|tell me something funny)",
            "how_are_you": r"(how are you|how you doing|how is it going)",
            "how_works": r"(how do you work|how were you made|how were you built|how do you function)",
            "purpose": r"(what is your purpose|why were you created|what is your goal|what are you for)",
            "who_made": r"(who made you|who created you|who built you|who developed you)"
        }
        
        # Learning data structure
        self.learned_responses = defaultdict(list)
        self.load_learned_data()
    
    def load_learned_data(self):
        try:
            if os.path.exists("learned_data.json"):
                with open("learned_data.json", "r") as file:
                    loaded_data = json.load(file)
                    self.learned_responses = defaultdict(list, loaded_data)
        except Exception as e:
            print(f"Error loading learned data: {e}")
            # If there's an error, just start with empty data
            self.learned_responses = defaultdict(list)
    
    def save_learned_data(self):
        try:
            with open("learned_data.json", "w") as file:
                json.dump(dict(self.learned_responses), file)
        except Exception as e:
            print(f"Error saving learned data: {e}")
    
    def learn_from_interaction(self, user_input, response):
        """Simple learning mechanism to remember interactions"""
        # Extract keywords from user input
        words = re.findall(r'\w+', user_input.lower())
        for word in words:
            if len(word) > 3 and word not in ['what', 'when', 'where', 'which', 'this', 'that', 'there', 'their', 'about']:
                if response not in self.learned_responses[word]:
                    self.learned_responses[word].append(response)
        
        # Periodically save learned data
        if random.random() < 0.2:  # 20% chance to save on each interaction
            self.save_learned_data()
    
    def get_response(self, user_input):
        """Generate a response based on the user input"""
        if not user_input or user_input.strip() == "":
            return "Please say something so we can chat!"
            
        # Add to conversation history
        self.conversation_history.append(("user", user_input))
        
        # Convert to lowercase for pattern matching
        user_input_lower = user_input.lower()
        
        # Check for pattern matches
        for category, pattern in self.patterns.items():
            if re.search(pattern, user_input_lower):
                response = random.choice(self.knowledge_base[category])
                self.learn_from_interaction(user_input, response)
                self.conversation_history.append(("bot", response))
                return response
        
        # Special case for "how are you"
        if re.search(self.patterns["how_are_you"], user_input_lower):
            response = "I'm doing well, thank you for asking! How about you?"
            self.conversation_history.append(("bot", response))
            return response
        
        # Check learned responses
        relevant_responses = []
        words = re.findall(r'\w+', user_input_lower)
        for word in words:
            if len(word) > 3:
                relevant_responses.extend(self.learned_responses[word])
        
        if relevant_responses:
            response = random.choice(relevant_responses)
            self.conversation_history.append(("bot", response))
            return response
        
        # Default response if no match is found
        response = random.choice(self.knowledge_base["default"])
        self.conversation_history.append(("bot", response))
        return response

# Initialize chatbot
chatbot = WittyAI()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response")
def get_bot_response():
    user_input = request.args.get('msg')
    
    # Add a slight delay to simulate thinking
    time.sleep(0.5)
    
    # Get chatbot response
    response = chatbot.get_response(user_input)
    return response

if __name__ == "__main__":
    # Create templates directory if it doesn't exist
    os.makedirs("templates", exist_ok=True)
    
    # Create a basic HTML template if it doesn't exist
    if not os.path.exists("templates/index.html"):
        with open("templates/index.html", "w") as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Witty AI Chatbot</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .chat-container {
            width: 90%;
            max-width: 700px;
            height: 80vh;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            background-color: white;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        .chat-header {
            background: linear-gradient(135deg, #6e48aa, #9d50bb);
            color: white;
            padding: 18px;
            text-align: center;
            font-size: 22px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        .chat-box {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            background-color: #f9f9f9;
        }
        .user-msg, .bot-msg {
            max-width: 80%;
            margin-bottom: 15px;
            padding: 12px 18px;
            border-radius: 20px;
            position: relative;
            word-wrap: break-word;
            animation: fadeIn 0.3s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .user-msg {
            background-color: #e9f5ff;
            color: #333;
            align-self: flex-end;
            border-bottom-right-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .bot-msg {
            background-color: #f0e6ff;
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .chat-input {
            display: flex;
            padding: 15px;
            background-color: white;
            border-top: 1px solid #eaeaea;
        }
        #userInput {
            flex: 1;
            padding: 14px 18px;
            border: 1px solid #e0e0e0;
            border-radius: 25px;
            outline: none;
            font-size: 16px;
            transition: border 0.3s;
        }
        #userInput:focus {
            border: 1px solid #9d50bb;
            box-shadow: 0 0 5px rgba(157, 80, 187, 0.3);
        }
        .send-btn {
            background: linear-gradient(135deg, #6e48aa, #9d50bb);
            color: white;
            border: none;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            margin-left: 12px;
            cursor: pointer;
            font-size: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .typing-indicator {
            display: none;
            align-self: flex-start;
            background-color: #f0e6ff;
            padding: 12px 18px;
            border-radius: 20px;
            border-bottom-left-radius: 5px;
            margin-bottom: 15px;
        }
        .typing-indicator span {
            height: 8px;
            width: 8px;
            background-color: #9d50bb;
            display: inline-block;
            border-radius: 50%;
            margin-right: 5px;
            animation: typing 1s infinite;
        }
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typing {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            Witty AI Chatbot
        </div>
        <div class="chat-box" id="chatBox">
            <div class="bot-msg">Hello! I'm Witty, your AI assistant. How can I help you today?</div>
            <div class="typing-indicator" id="typingIndicator">
                <span></span><span></span><span></span>
            </div>
        </div>
        <div class="chat-input">
            <input type="text" id="userInput" placeholder="Type your message..." autocomplete="off">
            <button class="send-btn" onclick="sendMessage()">➤</button>
        </div>
    </div>

    <script>
        function getBotResponse() {
            var userText = document.getElementById("userInput").value;
            var userHtml = '<div class="user-msg">' + userText + '</div>';
            
            document.getElementById("chatBox").innerHTML += userHtml;
            document.getElementById("userInput").value = "";
            
            // Scroll chat to bottom
            var chatBox = document.getElementById("chatBox");
            chatBox.scrollTop = chatBox.scrollHeight;
            
            // Show typing indicator
            var typingIndicator = document.getElementById("typingIndicator");
            typingIndicator.style.display = "block";
            chatBox.scrollTop = chatBox.scrollHeight;
            
            // Get response from server with a slight delay to show typing effect
            setTimeout(function() {
                fetch("/get_response?msg=" + encodeURIComponent(userText))
                    .then(response => response.text())
                    .then(data => {
                        // Hide typing indicator
                        typingIndicator.style.display = "none";
                        
                        var botHtml = '<div class="bot-msg">' + data + '</div>';
                        document.getElementById("chatBox").innerHTML += botHtml;
                        chatBox.scrollTop = chatBox.scrollHeight;
                    });
            }, 1000); // 1 second delay
        }
        
        function sendMessage() {
            if (document.getElementById("userInput").value.trim() !== "") {
                getBotResponse();
            }
        }
        
        // Send message when Enter key is pressed
        document.getElementById("userInput").addEventListener("keyup", function(event) {
            if (event.keyCode === 13) {
                event.preventDefault();
                if (this.value.trim() !== "") {
                    getBotResponse();
                }
            }
        });
        
        // Focus on input when page loads
        window.onload = function() {
            document.getElementById("userInput").focus();
        };
    </script>
</body>
</html>
            """)
    
    print("Starting Witty AI Chatbot...")
    print("Open your web browser and navigate to http://127.0.0.1:5000/ to interact with the chatbot.")
    app.run(debug=True)
