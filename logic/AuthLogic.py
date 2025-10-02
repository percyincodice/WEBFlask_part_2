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

            (login_response, login_code) = AuthDA.login(username, password)
            if login_code == 200:                
                claims = {
                    "username": username,
                    "rol": "ADMIN"
                }
                token_response = AuthDA.generate_token_autenticacion("ABCDE12345", username, 60, "WEBAPI", "WEBAPI",
                                                                     claims)
                if token_response["code"] == 200:
                    return jsonify({"token": token_response["token"], "username": username, 
                                    "expiresIn": token_response["expiresIn"]}), 200
                
                
                return jsonify(token_response), token_response["code"]
                
            return login_response, login_code

        
        
        except Exception as e:
            print("Error: ", e)
            return jsonify({"message": "Error an encountered."}), 500