from flask import Blueprint, jsonify, request
from logic.PersonLogic import PersonLogic


PersonBp = Blueprint("person", __name__)

@PersonBp.route("/api/person", methods=["POST"])
def createPerson():
    try:
        body = request.get_json()
        print('body', body)

        return PersonLogic.createPerson(body)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500

@PersonBp.route("/api/person", methods=["GET"])
def listPerson():
    try:       

        return PersonLogic.listPerson()
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500


@PersonBp.route("/api/person/<string:person_id>", methods=["GET"])
def getPersonById(person_id):
    try:       

        return PersonLogic.getPersonById(person_id)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500

@PersonBp.route("/api/person/<string:person_id>", methods=["PUT"])
def updatePersonById(person_id):
    try:       
        body = request.get_json()
        return PersonLogic.updatePersonById(person_id, body)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error.", 500
    
@PersonBp.route("/api/person/<string:person_id>", methods=["DELETE"])
def deletePersonById(person_id):
    try:       

        return PersonLogic.deletePersonById(person_id)
    except Exception as e:
        print("Error:", e) # cloudwatch aws
        return "Error delete person.", 500