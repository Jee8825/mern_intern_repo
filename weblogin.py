from flask import Flask, request, jsonify, send_from_directory
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
users = db["users"]

# Serve the login page
@app.route("/", methods=["GET"])
def home():
    return send_from_directory(os.getcwd(), "login.html")

# Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"status": "error", "message": "Missing username or password"}), 400

    username = data["username"]
    password = data["password"]

    user = users.find_one({"username": username})

    if user:
        # User exists, verify password
        if check_password_hash(user["password"], password):
            return jsonify({"status": "success", "message": "Logged in successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Wrong password"}), 401
    else:
        # User doesn't exist, create new
        hashed_password = generate_password_hash(password)
        users.insert_one({"username": username, "password": hashed_password})
        return jsonify({"status": "created", "message": "User created successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)