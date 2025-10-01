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
    
@AuthBp.route("/api/auth/v2", methods=["POST"])
def login_v2():
    try:
        body = request.get_json()

        return AuthLogic.login_v2(body)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error login.", 500