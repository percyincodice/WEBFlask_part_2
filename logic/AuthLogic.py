import json
from Utils.EncryptDecryptUtil import EncryptDecryptUtil
from Utils.EnvUtil import EnvUtil
from flask import jsonify
from dataaccess.AuthDA import AuthDA

class AuthLogic:

    @staticmethod
    def login(body):
        try:
            if body["username"] is None or body["username"] == "":
                return jsonify({"error": "Username is empty."}), 400

            if body["password"] is None or body["password"] == "":
                return jsonify({"error": "Password is empty."}), 400

            username = str(body["username"]).strip()
            password = str(body["password"]).strip()

            (response_login, code_login) = AuthDA.login(username, password)
            
            if code_login == 200:
                claims = {
                    "username": username,
                    "rol": "ADMIN"
                }
                token_response = AuthDA.generate_token_autenticacion("ABCDE12345", username, 60, "WEBTOKEN", "WEBTOKEN_CURSO1", claims)     
                
                if token_response["code"] == 200:
                    return jsonify({"token": token_response["token"], "expiresIn": token_response["expiresIn"], "username": username}), token_response["code"]    
                
                return jsonify(token_response), token_response["code"]
            
            return response_login, code_login
        
        
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error an encountered."}), 500
        
        
        
    @staticmethod
    def login_v2(body_encriptado):
        try:
            data_encriptado = body_encriptado["data"]
            
            key_kms_name = EnvUtil.get_env_variable("AWS_KMS_KEY")
            key_kms_name_region = EnvUtil.get_env_variable("AWS_KMS_KEY_REGION")
            
            data_decrypt = EncryptDecryptUtil.decrypt(data_encriptado, key_kms_name, key_kms_name_region)
                        
            body = json.loads(data_decrypt["data"])
            
            if body["username"] is None or body["username"] == "":
                return jsonify({"error": "Username is empty."}), 400

            if body["password"] is None or body["password"] == "":
                return jsonify({"error": "Password is empty."}), 400

            username = str(body["username"]).strip()
            password = str(body["password"]).strip()

            (response_login, code_login) = AuthDA.login(username, password)
            
            if code_login == 200:
                claims = {
                    "username": username,
                    "rol": "ADMIN"
                }
                token_response = AuthDA.generate_token_autenticacion("ABCDE12345", username, 60, "WEBTOKEN", "WEBTOKEN_CURSO1", claims)     
                
                if token_response["code"] == 200:
                    return jsonify({"token": token_response["token"], "expiresIn": token_response["expiresIn"], "username": username}), token_response["code"]    
                
                return jsonify(token_response), token_response["code"]
            
            return response_login, code_login
        
        
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error an encountered."}), 500