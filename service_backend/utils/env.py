import os
from dotenv import load_dotenv

env_file_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_file_path)

def get_env_variable(name_env: str) -> str:
    value = os.getenv(name_env)
    if not value:
        raise Exception(f"Missing required environment variable: {name_env}")
    return value.strip('"').strip("'")
