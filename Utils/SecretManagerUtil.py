import boto3
import json

class SecretManagerUtil:

    @staticmethod
    def get_secret(secret_name, region_name):
        try:
            client = boto3.client("secretsmanager", region_name=region_name)

            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )

            secret = get_secret_value_response["SecretString"]
            return json.loads(secret)

        except Exception as e:
            print("Error fetching secret:", e)
            raise e
