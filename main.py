from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
CORS(app)

# Initialize Firebase
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://vyralapp-default-rtdb.firebaseio.com/'
})

@app.route('/')
def home():
    return "🔥 Vyral Backend + Firebase is Live!"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Missing username or password'})

    ref = db.reference('/users')
    if ref.child(username).get():
        return jsonify({'status': 'error', 'message': 'User already exists'})

    ref.child(username).set({'password': password})
    return jsonify({'status': 'success', 'message': 'User created'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    ref = db.reference('/users')
    user = ref.child(username).get()

    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'})
    if user['password'] != password:
        return jsonify({'status': 'error', 'message': 'Wrong password'})

    return jsonify({'status': 'success', 'message': 'Login successful'})

if __name__ == '__main__':
    app.run()
