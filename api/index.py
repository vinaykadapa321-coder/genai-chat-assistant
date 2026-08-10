from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from environment variables")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-2.5-flash"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"reply": "Invalid request."}), 400

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please enter a message."}), 400

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