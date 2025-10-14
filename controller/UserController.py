from flask import Blueprint, jsonify, request
from logic.UserLogic import UserLogic
from middleware.ValidationToken import ValidationToken


UserBp = Blueprint("user", __name__)
validation_token = ValidationToken()

@UserBp.route("/api/user", methods=["POST"])
@validation_token.token_required
def createUser(decoded_token):
    try:
        body = request.get_json()
        print('body', body)

        return UserLogic.createUser(body)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500



@UserBp.route("/api/user", methods=["GET"])
@validation_token.token_required
def listUser(decoded_token):
    try:
        
        return UserLogic.listUser()
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500


@UserBp.route("/api/user/<string:user_id>", methods=["GET"])
@validation_token.token_required
def getUserById(decoded_token, user_id):
    try:       

        return UserLogic.getUserById(user_id)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500

@UserBp.route("/api/user/<string:user_id>", methods=["PUT"])
@validation_token.token_required
def updateUserById(decoded_token, user_id):
    try:       
        body = request.get_json()
        return UserLogic.updateUserById(user_id, body)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500
    
@UserBp.route("/api/user/<string:user_id>", methods=["DELETE"])
@validation_token.token_required
def deleteUserById(decoded_token, user_id):
    try:       

        return UserLogic.deleteUserById(user_id)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error delete user.", 500
    

@UserBp.route("/api/user/update-password", methods=["PUT"])
@validation_token.token_required
def updatePassword(decoded_token):
    try:       
        body = request.get_json()
        return UserLogic.updatePassword(body, decoded_token)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500
    
    
@UserBp.route("/api/user/encrypt", methods=["POST"])
def encrypt_test():
    try:
        body = request.get_json()

        return UserLogic.encrypt_test(body)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500
    
@UserBp.route("/api/user/decrypt", methods=["POST"])
def decrypt_test():
    try:
        body = request.get_json()

        return UserLogic.decrypt_test(body)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500