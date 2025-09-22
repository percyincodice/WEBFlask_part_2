import os
from dotenv import load_dotenv

class EnvUtil:

    @staticmethod
    def get_env_variable(key, default=None):
        # Cargar .env solo la primera vez que se invoque
        load_dotenv()
        return os.getenv(key, default)