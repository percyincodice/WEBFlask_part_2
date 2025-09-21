from flask import Blueprint, jsonify, request
from logic.PersonLogic import PersonLogic
from middleware.ValidationToken import ValidationToken


PersonBp = Blueprint("person", __name__)
validation_token = ValidationToken()

@PersonBp.route("/api/person", methods=["POST"])
@validation_token.token_required
def createPerson(decoded_token):
    try:
        body = request.get_json()
        print('body', body)

        return PersonLogic.createPerson(body)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500



@PersonBp.route("/api/person", methods=["GET"])
@validation_token.token_required
def listPerson(decoded_token=None):
    try:       
        print('decoded_token', decoded_token)
        return PersonLogic.listPerson()
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500


@PersonBp.route("/api/person/<string:person_id>", methods=["GET"])
@validation_token.token_required
def getPersonById(decoded_token, person_id):
    try:       

        return PersonLogic.getPersonById(person_id)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500

@PersonBp.route("/api/person/<string:person_id>", methods=["PUT"])
@validation_token.token_required
def updatePersonById(decoded_token, person_id):
    try:       
        body = request.get_json()
        return PersonLogic.updatePersonById(person_id, body)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500
    
@PersonBp.route("/api/person/<string:person_id>", methods=["DELETE"])
@validation_token.token_required
def deletePersonById(decoded_token, person_id):
    try:       

        return PersonLogic.deletePersonById(person_id)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error delete person.", 500