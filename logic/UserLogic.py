from Utils.EnvUtil import EnvUtil
from Utils.SecretManagerUtil import SecretManagerUtil
from flask import jsonify
from dataaccess.UserDA import UserDA

class UserLogic:

    @staticmethod
    def createUser(body):
        try:
            if body["username"] is None or body["username"] == "":
                return jsonify({"error": "Username is empty."}), 400

            if body["password"] is None or body["password"] == "":
                return jsonify({"error": "Password is empty."}), 400

            if body["role"] is None or body["role"] == "":
                return jsonify({"error": "Role is empty"}), 400
            
            if body["role"] not in ["ADMIN", "SUPERVISOR", "ASISTENTE"]:
                return jsonify({"error": "Role is not allowed"}), 400


            username = str(body["username"]).strip()
            password = str(body["password"]).strip()
            role = str(body["role"]).strip()
            
            secret_name = EnvUtil.get_env_variable("AWS_CONEXION_BD")
            secret_name_region = EnvUtil.get_env_variable("AWS_CONEXION_BD_REGION")
            
            secret = SecretManagerUtil.get_secret(secret_name, secret_name_region)

            if UserDA.validateDuplicateUsername(username=username, secret=secret):
                return jsonify({"error": "username is registered"}), 400
                

            return UserDA.createUser({
                "username": username,
                "password": password,
                "role": role,
            }, secret)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error an encountered."}), 500

    @staticmethod
    def listUser():
        try:
            secret_name = EnvUtil.get_env_variable("AWS_CONEXION_BD")
            secret_name_region = EnvUtil.get_env_variable("AWS_CONEXION_BD_REGION")
            
            secret = SecretManagerUtil.get_secret(secret_name, secret_name_region)
            return UserDA.listUser(secret)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error list user logic."}), 500

    @staticmethod
    def getUserById(user_id):
        try:
            secret_name = EnvUtil.get_env_variable("AWS_CONEXION_BD")
            secret_name_region = EnvUtil.get_env_variable("AWS_CONEXION_BD_REGION")
            
            secret = SecretManagerUtil.get_secret(secret_name, secret_name_region)
            return UserDA.getUserById(user_id, secret)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error get detail user logic."}), 500

    @staticmethod
    def updateUserById(user_id, body):
        try:
            if body["username"] is None or body["username"] == "":
                return jsonify({"error": "Username is empty."}), 400

            if body["password"] is None or body["password"] == "":
                return jsonify({"error": "Password is empty."}), 400

            if body["role"] is None or body["role"] == "":
                return jsonify({"error": "Role is empty"}), 400
            
            if body["role"] not in ["ADMIN", "SUPERVISOR", "ASISTENTE"]:
                return jsonify({"error": "Role is not allowed"}), 400


            username = str(body["username"]).strip()
            password = str(body["password"]).strip()
            role = str(body["role"]).strip()

            secret_name = EnvUtil.get_env_variable("AWS_CONEXION_BD")
            secret_name_region = EnvUtil.get_env_variable("AWS_CONEXION_BD_REGION")
            
            secret = SecretManagerUtil.get_secret(secret_name, secret_name_region)
            
            if UserDA.validateDuplicateUsername(username, user_id, secret):
                return jsonify({"error": "username is registered"}), 400            
            
            return UserDA.updateUserById(user_id, {
                "username": username,
                "password": password,
                "role": role,
            }, secret)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error update usera logic."}), 500
        
    @staticmethod
    def deleteUserById(user_id):
        try:
            secret_name = EnvUtil.get_env_variable("AWS_CONEXION_BD")
            secret_name_region = EnvUtil.get_env_variable("AWS_CONEXION_BD_REGION")
            
            secret = SecretManagerUtil.get_secret(secret_name, secret_name_region)
            return UserDA.deleteUserById(user_id, secret)
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error delete user logic."}), 500