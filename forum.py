from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["chat_database"]

@app.route("/")
def index():
    messages = list(db.messages.find({}))
    return render_template("index.html", messages=messages)

@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.form.get("message")
    db.messages.insert_one({"message": message})
    return "Message sent successfully!"

if __name__ == "__main__":
    app.run(debug=True)
