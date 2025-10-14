from Util.BcryptPasswordUtil import BcryptPasswordUtil
from Util.EncryptDecryptUtil import EncryptDecryptUtil
from Util.EnvUtil import EnvUtil
from Util.SecretManagerUtil import SecretManagerUtil
from dataaccess.AuthDA import AuthDA
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


            BCRYP_PEPPER = EnvUtil.get_env_variable("BCRYP_PEPPER")
            BCRYPT_COST = int(EnvUtil.get_env_variable("BCRYPT_COST"))
            
            password_hash = BcryptPasswordUtil.hash_password(body["password"], BCRYP_PEPPER, BCRYPT_COST)
            
            data_user = {
                "username": body["username"],
                "role": body["role"],
                "password": password_hash                
            }

            return UserDA.createUser(data_user, secret)
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
        
        
        
    @staticmethod
    def updatePassword(body, decoded_token):
        try:
            if body["password_old"] is None or body["password_old"] == "":
                return jsonify({"error": "Old password is empty."}), 400
            
            
            if body["password_new"] is None or body["password_new"] == "":
                return jsonify({"error": "New password is empty."}), 400
            

            secret_name = EnvUtil.get_env_variable("AWS_SECRET_BD")
            secret_name_region = EnvUtil.get_env_variable("AWS_SECRET_BD_REGION")
            
            secret = SecretManagerUtil.get_secret(secret_name, secret_name_region)
            
            username = decoded_token["username"]
            
            (login_response, login_code) = AuthDA.login(username, body["password_old"])
            if login_code == 200:   
                BCRYP_PEPPER = EnvUtil.get_env_variable("BCRYP_PEPPER")
                BCRYPT_COST = int(EnvUtil.get_env_variable("BCRYPT_COST"))
                
                password_hash = BcryptPasswordUtil.hash_password(body["password_new"], BCRYP_PEPPER, BCRYPT_COST)
                
                return UserDA.updatePassword(username, password_hash, secret)
            else:
                return jsonify({"message": "Invalid credentials."}), 400
        
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error update usera logic."}), 500
        
        
    @staticmethod
    def encrypt_test(body):
        try:
            text_to_encrypt = body["data"]            
            
            key_id = EnvUtil.get_env_variable("AWS_KEY_KMS")
            key_id_region = EnvUtil.get_env_variable("AWS_KEY_KMS_REGION")
            
            encrypt = EncryptDecryptUtil.encrypt(text_to_encrypt, key_id, key_id_region)
            
            return jsonify(encrypt), encrypt["codigo_respuesta"]

        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error an encountered."}), 500
        
    @staticmethod
    def decrypt_test(body):
        try:
            text_to_decrypt = body["data"]            
            
            key_id = EnvUtil.get_env_variable("AWS_KEY_KMS")
            key_id_region = EnvUtil.get_env_variable("AWS_KEY_KMS_REGION")
            
            decrypt = EncryptDecryptUtil.decrypt(text_to_decrypt, key_id, key_id_region)
            
            return jsonify(decrypt), decrypt["codigo_respuesta"]

        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error an encountered."}), 500
