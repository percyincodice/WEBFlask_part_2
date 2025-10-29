from flask import jsonify
from dataaccess.PersonDA import PersonDA
import datetime

class PersonLogic:

    @staticmethod
    def createPerson(body, decoded_token):
        try:
            if body["name"] is None or body["name"] == "":
                return jsonify({"error": "Name is empty."}), 400

            if body["lastname"] is None or body["lastname"] == "":
                return jsonify({"error": "Lastname is empty."}), 400

            if body["age"] is None or body["age"] < 0:
                return jsonify({"error": "Age is an error."}), 400

            # Fecha en formato UTC (zona 0)
            utc_now = datetime.datetime.utcnow()

            body["createdAt"] = utc_now
            body["modifiedAt"] = utc_now
            body["createdUser"] = decoded_token["username"]
            body["modifiedUser"] = decoded_token["username"]

            return PersonDA.createPerson(body)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error an encountered."}), 500

    @staticmethod
    def listPerson():
        try:
            return PersonDA.listPerson()
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error list person logic."}), 500

    @staticmethod
    def getPersonById(person_id):
        try:
            return PersonDA.getPersonById(person_id)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error get detail person logic."}), 500

    @staticmethod
    def updatePersonById(person_id, body, decoded_token):
        try:
            if body["name"] is None or body["name"] == "":
                return jsonify({"error": "Name is empty."}), 400

            if body["lastname"] is None or body["lastname"] == "":
                return jsonify({"error": "Lastname is empty."}), 400

            if body["age"] is None or body["age"] < 0:
                return jsonify({"error": "Age is an error."}), 400


            return PersonDA.updatePersonById(person_id, body, decoded_token)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error update persona logic."}), 500
        
    @staticmethod
    def deletePersonById(person_id):
        try:
            return PersonDA.deletePersonById(person_id)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error delete person logic."}), 500