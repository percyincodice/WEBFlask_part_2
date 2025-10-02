from Util.EnvUtil import EnvUtil
from Util.SecretManagerUtil import SecretManagerUtil
from flask import jsonify
from dataaccess.UserDA import UserDA

class UserLogic:

    @staticmethod
    def createUser(body):
        try:
            if body["username"] is None or body["username"] == "":
                return jsonify({"error": "username is empty."}), 400

            if body["password"] is None or body["password"] == "":
                return jsonify({"error": "Lastname is empty."}), 400

            if body["role"] is None or body["role"] == "":
                return jsonify({"error": "Role is empty."}), 400
            
            if body["role"] not in ["ADMIN", "SUPERVISOR", "ASISTENTE"]:
                return jsonify({"error": "Role is not allowed."}), 400
            
            
            secret_name = EnvUtil.get_env_variable("AWS_SECRET_BD")
            secret_name_region = EnvUtil.get_env_variable("AWS_SECRET_BD_REGION")
            
            secret = SecretManagerUtil.get_secret(secret_name, secret_name_region)            

            if UserDA.validateDuplicateUser(username=body["username"], secret=secret):
                return jsonify({"error": "user exists."}), 400

            return UserDA.createUser(body, secret)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error an encountered."}), 500

    @staticmethod
    def listUser():
        try:
            secret_name = EnvUtil.get_env_variable("AWS_SECRET_BD")
            secret_name_region = EnvUtil.get_env_variable("AWS_SECRET_BD_REGION")
            
            secret = SecretManagerUtil.get_secret(secret_name, secret_name_region)  
            return UserDA.listUser(secret)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error list user logic."}), 500

    @staticmethod
    def getUserById(user_id):
        try:
            secret_name = EnvUtil.get_env_variable("AWS_SECRET_BD")
            secret_name_region = EnvUtil.get_env_variable("AWS_SECRET_BD_REGION")
            
            secret = SecretManagerUtil.get_secret(secret_name, secret_name_region)
            return UserDA.getUserById(user_id, secret)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error get detail user logic."}), 500

    @staticmethod
    def updateUserById(user_id, body):
        try:
            if body["username"] is None or body["username"] == "":
                return jsonify({"error": "username is empty."}), 400

            if body["password"] is None or body["password"] == "":
                return jsonify({"error": "Lastname is empty."}), 400

            if body["role"] is None or body["role"] == "":
                return jsonify({"error": "Role is empty."}), 400
            
            if body["role"] not in ["ADMIN", "SUPERVISOR", "ASISTENTE"]:
                return jsonify({"error": "Role is not allowed."}), 400
            
            secret_name = EnvUtil.get_env_variable("AWS_SECRET_BD")
            secret_name_region = EnvUtil.get_env_variable("AWS_SECRET_BD_REGION")
            
            secret = SecretManagerUtil.get_secret(secret_name, secret_name_region)
            if UserDA.validateDuplicateUser(username=body["username"], exclude_id=user_id, secret=secret):
                return jsonify({"error": "user exists."}), 400


            return UserDA.updateUserById(user_id, body, secret)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error update usera logic."}), 500
        
    @staticmethod
    def deleteUserById(user_id):
        try:
            secret_name = EnvUtil.get_env_variable("AWS_SECRET_BD")
            secret_name_region = EnvUtil.get_env_variable("AWS_SECRET_BD_REGION")
            
            secret = SecretManagerUtil.get_secret(secret_name, secret_name_region)
            return UserDA.deleteUserById(user_id, secret)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error delete user logic."}), 500