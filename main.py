from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import uuid

app = Flask(__name__)
CORS(app)

# Firebase setup
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "vyralapp",
  "private_key_id": "auto-generated",
  "private_key": "-----BEGIN PRIVATE KEY-----\\naa97f68cebd34cb185259b94b697775d\\n-----END PRIVATE KEY-----\\n",
  "client_email": "firebase-adminsdk@vyralapp.iam.gserviceaccount.com",
  "client_id": "19ddbc337a164687bf3b99119336a6c3",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk"
})

firebase_admin.initialize_app(cred, {
  'databaseURL': 'https://vyralapp-default-rtdb.firebaseio.com/'
})

@app.route('/')
def home():
    return "🔥 Vyral Backend Running!"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_id = str(uuid.uuid4())

    ref = db.reference('/users')
    if ref.child(username).get():
        return jsonify({"status": "error", "message": "User already exists"})

    ref.child(username).set({
        "user_id": user_id,
        "password": password
    })
    return jsonify({"status": "success", "user_id": user_id})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    ref = db.reference('/users')
    user = ref.child(username).get()
    if not user or user['password'] != password:
        return jsonify({"status": "error", "message": "Invalid credentials"})

    return jsonify({"status": "success", "user_id": user['user_id']})

@app.route('/match', methods=['GET'])
def match():
    mode = request.args.get('mode')  # 'public' or 'private'
    uid = request.args.get('uid')

    ref = db.reference(f'/queue/{mode}')
    waiting = ref.get() or {}

    for other_id in waiting:
        if other_id != uid:
            ref.child(other_id).delete()
            return jsonify({"status": "matched", "partner_id": other_id})

    ref.child(uid).set(True)
    return jsonify({"status": "waiting"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
