from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

users = {}

EMAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

def validate_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password)
    )

@app.route("/")
def home():
    return "Flask Backend Running Successfully!"

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not re.fullmatch(EMAIL_REGEX, email):
        return jsonify({"message": "Invalid email format"}), 400

    if not validate_password(password):
        return jsonify({
            "message": "Password must be 8+ chars, include upper, lower & number"
        }), 400

    if email in users:
        return jsonify({"message": "User already exists"}), 400

    users[email] = generate_password_hash(password)

    return jsonify({"message": "Signup successful!"}), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email not in users:
        return jsonify({"message": "User not found"}), 400

    if not check_password_hash(users[email], password):
        return jsonify({"message": "Incorrect password"}), 400

    return jsonify({"message": "Login successful!"}), 200

if __name__ == "__main__":
    app.run(debug=True)