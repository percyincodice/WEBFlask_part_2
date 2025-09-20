from flask import Blueprint, jsonify, request
from logic.AuthLogic import AuthLogic

AuthBp = Blueprint("auth", __name__)

@AuthBp.route("/api/auth", methods=["POST"])
def login():
    try:
        body = request.get_json()

        return AuthLogic.login(body)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error login.", 500