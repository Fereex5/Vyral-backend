from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os
import json

app = Flask(__name__)

# Load Firebase credentials from environment variable
firebase_json = os.getenv("FIREBASE_KEY_JSON")
firebase_dict = json.loads(firebase_json)
cred = credentials.Certificate(firebase_dict)

# Initialize Firebase app
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://vyralapp-default-rtdb.firebaseio.com/'
    })

@app.route('/')
def home():
    return jsonify({"message": "Vyral backend is live 🔥"})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    ref = db.reference(f"/users/{username}")
    if ref.get():
        return jsonify({"error": "User already exists"}), 409

    ref.set({"username": username, "password": password})
    return jsonify({"message": "Signup successful ✅"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    ref = db.reference(f"/users/{username}")
    user = ref.get()

    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.get("password") != password:
        return jsonify({"error": "Incorrect password"}), 401

    return jsonify({"message": "Login successful 🎉"}), 200

if __name__ == '__main__':
    app.run()
