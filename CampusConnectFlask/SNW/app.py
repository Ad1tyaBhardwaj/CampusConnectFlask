from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = "your-secret-key"
socketio = SocketIO(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["Users"]
user_collection = db["data"]
db1 = client["chat_database"]


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        # Get the user data from the form
        username = request.form.get("username")
        password = request.form.get("password")

        # Store the user data in the MongoDB database
        user_collection.insert_one({
            "username": username,
            "password": password
        })
        return "User data saved successfully!"

    return render_template("signup.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if the username and password exist in the users collection
        username = request.form.get("username")
        password = request.form.get("password")
        user = user_collection.find_one({"username": username, "password": password})
        if user:
            # If the user exists, store the username in session and redirect to the index page
            session['username'] = username
            return redirect(url_for("index"))
        else:
            # If the user does not exist, return False
            return "False"
    else:
        # If the request method is GET, render the login page
        return render_template("login.html")

@app.route("/index")
def index():
    if 'username' not in session:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for("login"))

    messages = db1.messages.find()
    return render_template("index.html", messages=messages)

    
@socketio.on('message')
def handle_message(message):
    db1.messages.insert_one({"username": session['username'], "message" : message})
    print(f'received message from {session["username"]}: ' + message)
    # Broadcast the message to all clients
    socketio.emit('message', message, broadcast=True)

connected_users = 0

@socketio.on('connect')
def handle_connect():
    global connected_users
    connected_users += 1
    emit('user_count', connected_users, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    global connected_users
    connected_users -= 1
    emit('user_count', connected_users, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
