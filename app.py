from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
from utils.voice import listen
import os


# Load environment variables
load_dotenv()


# Create Flask application
app = Flask(__name__)


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from the .env file")


# Create Gemini client
client = genai.Client(api_key=api_key)


# Gemini model
MODEL_NAME = "gemini-3.6-flash"


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Text Chat
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "reply": "Invalid request."
            }), 400

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "reply": "Please enter a message."
            }), 400

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_message
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        print("Chat Error:", e)

        return jsonify({
            "reply": f"Error: {str(e)}"
        }), 500


# Voice Chat
@app.route("/voice", methods=["GET"])
def voice():
    try:
        user_message = listen()

        if not user_message:
            return jsonify({
                "reply": "I could not understand your voice."
            }), 400

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_message
        )

        return jsonify({
            "user": user_message,
            "reply": response.text
        })

    except Exception as e:
        print("Voice Error:", e)

        return jsonify({
            "reply": f"Error: {str(e)}"
        }), 500


# Run Flask application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )