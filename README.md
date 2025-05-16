# Witty AI Chatbot

A conversational AI chatbot developed using Python and Flask that simulates human conversation through pattern matching and simple learning.

## Project Overview

Witty is an chatbot designed to simulate human conversation. It provides responses to user queries and engages in dialogue based on predefined conversational patterns. 

## Features

- **Natural language understanding** through pattern matching and keyword extraction
- **Web-based user interface** with an attractive, responsive design
- **Pattern matching system** for recognizing common conversational topics
- **Real-time interaction** with typing indicators and smooth animations
- **Persistent memory** through JSON-based storage of learned responses

## Technical Implementation

- **Backend**: Python with Flask web framework for the server
- **AI Engine**: Custom-built pattern matching system with regex and keyword extraction
- **Storage**: JSON-based persistence for storing learned responses
- **Frontend**: Modern HTML5/CSS3/JavaScript interface with responsive design
- **Conversation Logic**: Rule-based system with fallback mechanisms for unknown queries

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/witty-ai-chatbot.git
   cd witty-ai-chatbot
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python Wit.py
   ```

4. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## How It Works

1. **Pattern Recognition**: The chatbot analyzes user input using regular expressions to identify common patterns (greetings, questions about identity, etc.)
2. **Response Selection**: Based on the pattern match, it selects an appropriate response from its knowledge base
3. **Learning Mechanism**: It extracts keywords from user inputs and associates them with responses for future reference
4. **Persistence**: Periodically saves learned associations to a JSON file for future sessions

## Chatbot Capabilities

- Answering questions about itself and its purpose
- Engaging in basic small talk (greetings, farewells, etc.)
- Telling jokes and responding to expressions of gratitude
