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
                token_response = AuthDA.generate_token_autenticacion("ABCDE12345", username, 0.4, "WEBTOKEN", "WEBTOKEN_CURSO1", claims)     
                
                if token_response["code"] == 200:
                    return jsonify({"token": token_response["token"], "expiresIn": token_response["expiresIn"], "username": username}), token_response["code"]    
                
                return jsonify(token_response), token_response["code"]
            
            return response_login, code_login
        
        
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error an encountered."}), 500