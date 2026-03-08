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
        if user_message in doc["title"].lower():
            return jsonify({"reply": doc["content"]})
    return jsonify({"reply": "Sorry, I don't know the answer."})

if __name__=="__main__":
    app.run(debug=True)