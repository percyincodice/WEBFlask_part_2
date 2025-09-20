from flask import jsonify
from dataaccess.PersonDA import PersonDA

class PersonLogic:

    @staticmethod
    def createPerson(body):
        try:
            if body["name"] is None or body["name"] == "":
                return jsonify({"error": "Name is empty."}), 400

            if body["lastname"] is None or body["lastname"] == "":
                return jsonify({"error": "Lastname is empty."}), 400

            if body["age"] is None or body["age"] < 0:
                return jsonify({"error": "Age is an error."}), 400


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
    def updatePersonById(person_id, body):
        try:
            if body["name"] is None or body["name"] == "":
                return jsonify({"error": "Name is empty."}), 400

            if body["lastname"] is None or body["lastname"] == "":
                return jsonify({"error": "Lastname is empty."}), 400

            if body["age"] is None or body["age"] < 0:
                return jsonify({"error": "Age is an error."}), 400


            return PersonDA.updatePersonById(person_id, body)
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