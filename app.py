from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
from utils.voice import listen
import os

# Load .env
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from the .env file")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Gemini model
MODEL_NAME = "gemini-3.6-flash"


def get_ai_response(user_message):
    """
    Send the user's message to Gemini
    and return the AI response.
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_message
    )

    if response and response.text:
        return response.text.strip()

    return "Sorry, I could not generate a response."


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Text chat
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "reply": "Invalid request."
            }), 400

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "reply": "Please enter a message."
            }), 400

        print("User:", user_message)

        ai_reply = get_ai_response(user_message)

        print("AI:", ai_reply)

        return jsonify({
            "user": user_message,
            "reply": ai_reply
        })

    except Exception as e:
        print("Chat Error:", e)

        return jsonify({
            "reply": "Sorry, something went wrong while processing your message."
        }), 500


# Voice chat
@app.route("/voice", methods=["GET"])
def voice():
    try:
        print("Starting voice input...")

        user_message = listen()

        if not user_message:
            return jsonify({
                "reply": "I could not understand your voice."
            }), 400

        # Handle voice-recognition messages
        if user_message.startswith("No speech detected"):
            return jsonify({
                "user": user_message,
                "reply": user_message
            }), 400

        if user_message.startswith("Sorry, I couldn't understand"):
            return jsonify({
                "user": user_message,
                "reply": user_message
            }), 400

        if user_message.startswith("Speech Recognition service unavailable"):
            return jsonify({
                "user": user_message,
                "reply": user_message
            }), 500

        print("User said:", user_message)

        # Send voice text to Gemini
        ai_reply = get_ai_response(user_message)

        print("AI:", ai_reply)

        return jsonify({
            "user": user_message,
            "reply": ai_reply
        })

    except Exception as e:
        print("Voice Error:", e)

        return jsonify({
            "reply": "Sorry, there was a problem with voice processing."
        }), 500


# Run Flask server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )