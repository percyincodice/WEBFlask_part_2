from Utils.BcryptPassword import BcryptPassword
from Utils.EncryptDecryptUtil import EncryptDecryptUtil
from Utils.EnvUtil import EnvUtil
from Utils.SecretManagerUtil import SecretManagerUtil
from dataaccess.AuthDA import AuthDA
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
                

            bcryptpepper = EnvUtil.get_env_variable("BCRYPT_PEPPER")
            bcrypcost = int(EnvUtil.get_env_variable("BCRYPT_COST"))
            
            password_hash = BcryptPassword.hash_password(password, bcryptpepper, bcrypcost)

            return UserDA.createUser({
                "username": username,
                "password": password_hash,
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
        
        
    @staticmethod
    def encrypt_test(body):
        try:
            text_to_encrypt = body["data"]
            
            key_kms_name = EnvUtil.get_env_variable("AWS_KMS_KEY")
            key_kms_name_region = EnvUtil.get_env_variable("AWS_KMS_KEY_REGION")
            
            encrypt_data = EncryptDecryptUtil.encrypt(text_to_encrypt, key_kms_name, key_kms_name_region)
            return jsonify(encrypt_data), encrypt_data["codigo_respuesta"]
        
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error encrypt data logic."}), 500
        
        
    @staticmethod
    def decrypt_test(body):
        try:
            text_to_decrypt = body["data"]
            
            key_kms_name = EnvUtil.get_env_variable("AWS_KMS_KEY")
            key_kms_name_region = EnvUtil.get_env_variable("AWS_KMS_KEY_REGION")
            
            decrypt_data = EncryptDecryptUtil.decrypt(text_to_decrypt, key_kms_name, key_kms_name_region)
            return jsonify(decrypt_data), decrypt_data["codigo_respuesta"]
        
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error decrypt data logic."}), 500
        
        
    @staticmethod
    def updatePassword(body, decoded_token):
        try:         

            if body["password_old"] is None or body["password_old"] == "":
                return jsonify({"error": "Old Password is empty."}), 400

            if body["password_new"] is None or body["password_new"] == "":
                return jsonify({"error": "new Password is empty."}), 400
         

          
            secret_name = EnvUtil.get_env_variable("AWS_CONEXION_BD")
            secret_name_region = EnvUtil.get_env_variable("AWS_CONEXION_BD_REGION")
            
            secret = SecretManagerUtil.get_secret(secret_name, secret_name_region)
            
        
            #validar si el usuario y clave antigua si son validas
            (response_login, code_login) = AuthDA.login(decoded_token["username"], body["password_old"])
            
            if code_login == 200:
                bcryptpepper = EnvUtil.get_env_variable("BCRYPT_PEPPER")
                bcrypcost = int(EnvUtil.get_env_variable("BCRYPT_COST"))
                
                password_hash = BcryptPassword.hash_password(body["password_new"], bcryptpepper, bcrypcost)
                
                return UserDA.updatePassword(decoded_token["username"], password_hash, secret)
            
                       
            return response_login, code_login        
            
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error update usera logic."}), 500

    