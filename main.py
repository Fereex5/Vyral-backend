from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "🔥 Vyral Backend Running!"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing data"})

    return jsonify({"status": "success", "message": "Signup simulated!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == "demo_user" and password == "demo_pass":
        return jsonify({"status": "success", "message": "Login success!"})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"})

if __name__ == "__main__":
    app.run()
