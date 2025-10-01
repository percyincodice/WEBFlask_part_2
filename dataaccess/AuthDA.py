from Utils.BcryptPassword import BcryptPassword
from Utils.EnvUtil import EnvUtil
from flask import jsonify
from pymongo import MongoClient
from bson import ObjectId


import jwt
from datetime import datetime, timedelta, timezone

class AuthDA:
    client = MongoClient("mongodb://localhost:27017")
    db = client["apibd_review"]
    collectionUsers= db["users"]
    
    @staticmethod
    def login(username, password):
        try:
            user = AuthDA.collectionUsers.find_one({"username": username})

            if user:      
                bcryptpepper = EnvUtil.get_env_variable("BCRYPT_PEPPER")
                if BcryptPassword.verify_password(user["password"], password, bcryptpepper):                          
                    return jsonify({"username": user["username"], "message": "User logged in successfully"}), 200                
                
                
            return jsonify({"message": "Invalid credentials"}), 404

        except Exception as e:
            print("Error:", e)
            return jsonify({"message": "Error logged in user."}), 500
        
        
    @staticmethod
    def generate_token_autenticacion(
        secret_key_token: str,
        username: str,
        duration_minutes_token: int,
        issuing_token: str,
        audience_token: str,
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