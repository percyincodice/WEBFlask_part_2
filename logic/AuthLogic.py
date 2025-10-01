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
                return jsonify({"error": "Passowrd is empty."}), 400

            username = str(body["username"]).strip()
            password = str(body["password"]).strip()

            (login_response, login_code) = AuthDA.login(username, password)
            
            if login_code == 200:
                claims = {
                    "username": username,
                    "rol": "ADMIN"                    
                }
                token_response = AuthDA.generate_token_autenticacion("ABCDE12345", username, 60, "APIWEB", "APIWEB", claims)
                
                if token_response["code"] == 200:
                    return jsonify({"token": token_response["token"], "expiresIn":  token_response["expiresIn"], "username": username}), 200        
                
                return jsonify(token_response), token_response["code"]
            
            
            return login_response, login_code
            
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error an encountered."}), 500
        
        
    @staticmethod
    def login_v2(bodyv2):
        try:
            key_id_kms = EnvUtil.get_env_variable("AWS_KEY_ID_KMS")
            key_id_kms_region = EnvUtil.get_env_variable("AWS_KEY_ID_KMS_REGION")
            
            print('bodyv2["data"]', bodyv2["data"])
            
            data_decrypt = EncryptDecryptUtil.decrypt(bodyv2["data"], key_id_kms, key_id_kms_region)
            
            print('data_decrypt', data_decrypt)
            
            body = json.loads(data_decrypt["data"])            
            
            if body["username"] is None or body["username"] == "":
                return jsonify({"error": "Username is empty."}), 400

            if body["password"] is None or body["password"] == "":
                return jsonify({"error": "Passowrd is empty."}), 400

            username = str(body["username"]).strip()
            password = str(body["password"]).strip()

            (login_response, login_code) = AuthDA.login(username, password)
            
            if login_code == 200:
                claims = {
                    "username": username,
                    "rol": "ADMIN"                    
                }
                token_response = AuthDA.generate_token_autenticacion("ABCDE12345", username, 60, "APIWEB", "APIWEB", claims)
                
                if token_response["code"] == 200:
                    return jsonify({"token": token_response["token"], "expiresIn":  token_response["expiresIn"], "username": username}), 200        
                
                return jsonify(token_response), token_response["code"]
            
            
            return login_response, login_code
            
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error an encountered."}), 500