from Util.BcryptPasswordUtil import BcryptPasswordUtil
from Util.EnvUtil import EnvUtil
from flask import jsonify
from pymongo import MongoClient
from bson import ObjectId


import jwt
from datetime import datetime, timedelta, timezone

class AuthDA:
    client = MongoClient("mongodb://localhost:27017")
    db = client["apibd"]
    collectionUsers = db["users"]

    @staticmethod
    def login(username, password):
        try:
            result = AuthDA.collectionUsers.find_one({"username": username})
            
            if result:
                #validar la contraseña
                BCRYP_PEPPER = EnvUtil.get_env_variable("BCRYP_PEPPER")
                if BcryptPasswordUtil.verify_password(result["password"], password, BCRYP_PEPPER):                
                    return jsonify({"message": "user logged in successfully", "username": username}), 200
                

            return jsonify({"message": "Invalid credentials."}), 400

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error logged in user."}), 500
        
        
    @staticmethod
    def generate_token_autenticacion(
        secret_key_token: str,
        username: str,
        duration_minutes_token: int,
        issuing_token: str, #"nombre aplicativo"
        audience_token: str, #"area del departemento"
        claims: dict
    ):
        try:
            # Fecha de expiración
            exp = datetime.now(timezone.utc) + timedelta(minutes=duration_minutes_token)
            print('exp', exp)

            # Payload del token
            payload = {
                "sub": username,          # quién es el sujeto del token
                "iss": issuing_token,      # emisor
                "aud": audience_token,   # audiencia
                "exp": exp,               # fecha de expiración
                **claims                  # claims adicionales (se combinan al diccionario)
            }

            # Generar token con algoritmo HMAC-SHA256
            token = jwt.encode(payload, secret_key_token, algorithm="HS256")

            return {
                "code": 200,
                "message": "Exitoso.",
                "token": token,
                "expiresIn": duration_minutes_token * 60
            }
        except Exception as ex:
            print(f"Error al generar token para el usuario {username}: {str(ex)}")
            return {
                "code": 500,
                "message": "Error interno al intentar generar token."
            }
