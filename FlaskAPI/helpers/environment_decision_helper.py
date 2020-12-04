import os 
from dotenv import load_dotenv
from pathlib import Path

class EnvironmentDecisionHelper:
    
    def __init__(self):
        raise RuntimeError('Call set_environment_flask_settings instead')

    @staticmethod
    def set_environment_flask_settings():
        if os.environ.get("FLASK_ENV").lower() == "development":
            env_path = Path('.') / 'development.env'
            load_dotenv(env_path)
        elif os.environ.get("FLASK_ENV").lower() == "production":
            env_path = Path('.') / 'production.env'     
            load_dotenv(env_path)
        else:
            raise Exception("No FLASK_ENV variable set")
