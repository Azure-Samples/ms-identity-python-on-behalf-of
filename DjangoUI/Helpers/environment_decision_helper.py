import os 
from dotenv import load_dotenv
from pathlib import Path

class EnvironmentDecisionHelper:
    
    def __init__(self):
        raise RuntimeError('Call set_environment_django_settings instead')
    
    @staticmethod
    def set_environment_django_settings():
        if os.environ.get("ENVIRONMENT").lower() == "development":
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UI.development_settings')
            env_path = Path('.') / 'development.env'
            load_dotenv(env_path)
        elif os.environ.get("ENVIRONMENT").lower() == "production":
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UI.production_settings')
            env_path = Path('.') / 'production.env'     
            load_dotenv(env_path)
        else:
            raise Exception("No ENVIRONMENT variable set")