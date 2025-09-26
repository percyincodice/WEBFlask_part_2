from flask import Blueprint, jsonify, request
from logic.AuthLogic import AuthLogic


AuthBp = Blueprint("AuthBp", __name__)

@AuthBp.route("/api/auth", methods=["POST"])
def login():
    try:
        body = request.get_json()

        return AuthLogic.login(body)
    except Exception as e:
        print("Error login:", e) # cloudwatch aws
        return "Error login.", 500
