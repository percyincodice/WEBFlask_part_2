import jwt
from jwt import InvalidTokenError, ExpiredSignatureError, InvalidAudienceError, InvalidIssuerError
from flask import jsonify, request
from functools import wraps  

class ValidationToken:
    def token_required(self, f):
        @wraps(f)  
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                print('Token no proporcionado')
                return jsonify({'error': 'Token no proporcionado'}), 401

            token = token.split(" ")[1] if " " in token else token
            (code_validation, claims_validations) = self.validar_token_jwt(token, "ABCDE12345", "WEBTOKEN", "WEBTOKEN_CURSO1")

            if code_validation != True:
                print('Token inválido o con error')
                return jsonify({"message": "Token no valido"}), 401

            return f(*args, **kwargs, decoded_token=claims_validations)

        return decorated
    

    def validar_token_jwt(self, token: str, secret_key_token: str, valid_issuer: str, valid_audience: str):
        """
        Valida un token JWT y devuelve (True, claims) si es válido, 
        o (False, {}) si no lo es.
        """
        try:
            # Decodifica y valida el token
            claims = jwt.decode(
                token,
                secret_key_token,
                algorithms=["HS256"],
                audience=valid_audience,
                issuer=valid_issuer
            )
            
            print('claims decoded', claims)

            # Si todo está bien, retorna los claims
            return True, claims

        except ExpiredSignatureError:
            print("Error: El token ha expirado")
            return False, {}

        except InvalidAudienceError:
            print("Error: La audiencia no es válida")
            return False, {}

        except InvalidIssuerError:
            print("Error: El emisor no es válido")
            return False, {}

        except InvalidTokenError as ex:
            print(f"Error: Token inválido -> {str(ex)}")
            return False, {}
