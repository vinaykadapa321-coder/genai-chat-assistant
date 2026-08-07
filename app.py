from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
from utils.voice import listen
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Text Chat
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        user_message = data.get("message")

        if not user_message:
            return jsonify({
                "reply": "Please enter a message."
            })

        response = model.generate_content(user_message)

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        return jsonify({
            "reply": str(e)
        })


# Voice Chat
@app.route("/voice", methods=["GET"])
def voice():

    try:
        user_message = listen()

        response = model.generate_content(user_message)

        return jsonify({
            "user": user_message,
            "reply": response.text
        })

    except Exception as e:
        return jsonify({
            "reply": str(e)
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)