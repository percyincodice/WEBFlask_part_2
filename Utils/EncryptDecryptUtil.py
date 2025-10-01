import base64
import urllib.parse
import boto3
from botocore.exceptions import ClientError

class EncryptDecryptUtil:
    
    @staticmethod
    def encrypt(plaintext: str, key_id_kms: str, region_name: str) -> dict:       
        try:
            plaintext_encoded = urllib.parse.quote(plaintext)

            client = boto3.client("kms", region_name=region_name)
            
            response = client.encrypt(
                KeyId=key_id_kms,
                Plaintext=plaintext_encoded.encode("utf-8"),
                EncryptionAlgorithm="RSAES_OAEP_SHA_256"
            )

            ciphertext_blob = response["CiphertextBlob"]

            return {
                "codigo_respuesta": 200,
                "mensaje_respuesta": "Datos encriptados",
                "data": base64.b64encode(ciphertext_blob).decode("utf-8")
            }

        except ClientError as e:
            print("Error encrypt:", e)
            return {
                "codigo_respuesta": 500,
                "mensaje_respuesta": f"Error al encriptar los datos: {str(e)}"
            }

    def decrypt(encrypted_data: str, key_id_kms: str, region_name: str) -> dict:        
        try:
            ciphertext_blob = base64.b64decode(encrypted_data)

            client = boto3.client("kms", region_name=region_name)
            
            response = client.decrypt(
                CiphertextBlob=ciphertext_blob,
                KeyId=key_id_kms,
                EncryptionAlgorithm="RSAES_OAEP_SHA_256"
            )

            plaintext = response["Plaintext"].decode("utf-8")
            plaintext_decoded = urllib.parse.unquote(plaintext)

            return {
                "codigo_respuesta": 200,
                "mensaje_respuesta": "Datos desencriptados",
                "data": plaintext_decoded
            }

        except ClientError as e:
            print("Error decrypt:", e)
            return {
                "codigo_respuesta": 500,
                "mensaje_respuesta": f"Error al desencriptar los datos: {str(e)}"
            }
