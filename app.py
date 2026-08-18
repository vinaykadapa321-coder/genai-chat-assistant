from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Flask application
app = Flask(__name__)

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Gemini model
MODEL_NAME = "gemini-2.5-flash"


def get_ai_response(user_message):
    """Send user message to Gemini and return AI response."""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_message
    )

    if response and response.text:
        return response.text.strip()

    return "Sorry, I could not generate a response."


# --------------------------------
# Home page
# --------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------
# Text Chat API
# --------------------------------

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


# --------------------------------
# Health Check
# --------------------------------

@app.route("/health")
def health():

    return jsonify({
        "status": "running",
        "message": "GenAI Chat Assistant is working"
    })


# --------------------------------
# Run Flask
# --------------------------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )