from flask import jsonify
from pymongo import MongoClient
from bson import ObjectId
import json
import os
import uuid

class PersonDA:
    client = MongoClient("mongodb://localhost:27017")
    db = client["apibd"]
    collectionPersona = db["personas"]

    @staticmethod
    def createPerson(body):
        try:
            result = PersonDA.collectionPersona.insert_one(body)

            return jsonify({"message": "Person created!!!!!!", "id": str(result.inserted_id)}), 201

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in person DA."}), 500

    @staticmethod
    def listPerson():
        try:
            data = list(PersonDA.collectionPersona.find())
           
            for person in data:
                person["_id"] = str(person["_id"])                

            return jsonify(data), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in list person."}), 500


    @staticmethod
    def getPersonById(person_id):
        try:
            person = PersonDA.collectionPersona.find_one({"_id": ObjectId(person_id)})

            if person:
                person["_id"] = str(person["_id"])   
                return jsonify(person), 200
            else:
                return jsonify({"message": "Person not found."}), 404

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in list person."}), 500



    @staticmethod
    def updatePersonById(person_id, body):
        try:
            result = PersonDA.collectionPersona.update_one(
                {"_id": ObjectId(person_id)},
                {"$set": body}
            )
            
            if result.matched_count == 0:
                return jsonify({"message": "Person not found."}), 400
            
            
            return jsonify({"message": "Person updated."}), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in update person."}), 500
        

    @staticmethod
    def deletePersonById(person_id):
        try:
            result = PersonDA.collectionPersona.delete_one(
                {"_id": ObjectId(person_id)}
            )
            
            if result.deleted_count == 0:
                return jsonify({"message": "Person not found."}), 400
            
            
            return jsonify({"message": "Person deleted."}), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in delete person."}), 500