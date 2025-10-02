from flask import jsonify
from pymongo import MongoClient
from bson import ObjectId


class UserDA:
    @staticmethod
    def createUser(body, secret):
        try:
            collectionBD = MongoClient(secret["conexion_bd"])["apibd"]["users"]
            
            result = collectionBD.insert_one(body)

            return jsonify({"message": "User created!!!!!!", "id": str(result.inserted_id)}), 201

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in user DA."}), 500

    @staticmethod
    def listUser(secret):
        try:
            collectionBD = MongoClient(secret["conexion_bd"])["apibd"]["users"]
            data = list(collectionBD.find())
           
            for user in data:
                user["_id"] = str(user["_id"])                

            return jsonify(data), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in list user."}), 500


    @staticmethod
    def getUserById(person_id, secret):
        try:
            collectionBD = MongoClient(secret["conexion_bd"])["apibd"]["users"]
            user = collectionBD.find_one({"_id": ObjectId(person_id)})

            if user:
                user["_id"] = str(user["_id"])   
                return jsonify(user), 200
            else:
                return jsonify({"message": "User not found."}), 404

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in list user."}), 500



    @staticmethod
    def updateUserById(person_id, body, secret):
        try:
            collectionBD = MongoClient(secret["conexion_bd"])["apibd"]["users"]
            result = collectionBD.update_one(
                {"_id": ObjectId(person_id)},
                {"$set": body}
            )
            
            if result.matched_count == 0:
                return jsonify({"message": "User not found."}), 400
            
            
            return jsonify({"message": "User updated."}), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in update user."}), 500
        

    @staticmethod
    def deleteUserById(person_id, secret):
        try:
            collectionBD = MongoClient(secret["conexion_bd"])["apibd"]["users"]
            result = collectionBD.delete_one(
                {"_id": ObjectId(person_id)}
            )
            
            if result.deleted_count == 0:
                return jsonify({"message": "User not found."}), 400
            
            
            return jsonify({"message": "User deleted."}), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in delete user."}), 500
        
        
    @staticmethod
    def validateDuplicateUser(username, exclude_id=None, secret=None):
        try:
            collectionBD = MongoClient(secret["conexion_bd"])["apibd"]["users"]            
            
            query = {"username": username}
            if exclude_id:
                query["_id"] = {"$ne": ObjectId(exclude_id)}
            
            exists = collectionBD.count_documents(query)

            return exists > 0

        except Exception as e:
            print("Error:", e)
            raise e