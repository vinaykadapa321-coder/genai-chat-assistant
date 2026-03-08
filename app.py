from flask import Flask, render_template, request, jsonify
import json 

app = Flask(__name__)

with open("docs.json") as f:
    documents = json.load(f)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message= request.json["message"].lower()

    for doc in documents:
        if doc["title"].lower() in user_message:
            return jsonify({"reply": doc["content"]})
    return jsonify({"reply": "Sorry, I don't know the answer."})
import os
if __name__=="__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)