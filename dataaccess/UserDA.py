from flask import jsonify
from pymongo import MongoClient
from bson import ObjectId


class UserDA:
    @staticmethod
    def createUser(body, secret):
        try:
            collectionBDUsers = MongoClient(secret["conexion_bd"])["apibd_review"]["users"]
            
            result = collectionBDUsers.insert_one(body)

            return jsonify({"message": "User created!!!!!!", "id": str(result.inserted_id)}), 201

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in user DA."}), 500

    @staticmethod
    def listUser(secret):
        try:
            collectionBDUsers = MongoClient(secret["conexion_bd"])["apibd_review"]["users"]
            data = list(collectionBDUsers.find())
           
            for user in data:
                user["_id"] = str(user["_id"])                

            return jsonify(data), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in list user."}), 500


    @staticmethod
    def getUserById(user_id, secret):
        try:
            collectionBDUsers = MongoClient(secret["conexion_bd"])["apibd_review"]["users"]
            user = collectionBDUsers.find_one({"_id": ObjectId(user_id)})

            if user:
                user["_id"] = str(user["_id"])   
                return jsonify(user), 200
            else:
                return jsonify({"message": "User not found."}), 404

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in list user."}), 500



    @staticmethod
    def updateUserById(user_id, body, secret):
        try:
            collectionBDUsers = MongoClient(secret["conexion_bd"])["apibd_review"]["users"]
            result = collectionBDUsers.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": body}
            )
            
            if result.matched_count == 0:
                return jsonify({"message": "User not found."}), 400
            
            
            return jsonify({"message": "User updated."}), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in update user."}), 500
        

    @staticmethod
    def deleteUserById(user_id, secret):
        try:
            collectionBDUsers = MongoClient(secret["conexion_bd"])["apibd_review"]["users"]
            result = collectionBDUsers.delete_one(
                {"_id": ObjectId(user_id)}
            )
            
            if result.deleted_count == 0:
                return jsonify({"message": "User not found."}), 400
            
            
            return jsonify({"message": "User deleted."}), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in delete user."}), 500
        
        
    @staticmethod
    def validateDuplicateUsername(username, exclude_id=None, secret=None):
        try:
            
            collectionBDUsers = MongoClient(secret["conexion_bd"])["apibd_review"]["users"]
          
            query = {"username": username}
            
            if exclude_id:
                query["_id"] = {"$ne": ObjectId(exclude_id)}
            
            exists = collectionBDUsers.count_documents(query, limit = 1)
            return exists > 0
        except Exception as e:
            print("Error:", e)
            raise e
        
        
    @staticmethod
    def updatePassword(username, password, secret):
        try:
            collectionBDUsers = MongoClient(secret["conexion_bd"])["apibd_review"]["users"]
            result = collectionBDUsers.update_one(
                {"username": username},
                {"$set": {"password": password}}
            )
            
            if result.matched_count == 0:
                return jsonify({"message": "User not found."}), 400
            
            
            return jsonify({"message": "User updated."}), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error in update user."}), 500