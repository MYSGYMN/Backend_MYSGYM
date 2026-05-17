import os
from dotenv import load_dotenv

env_file = os.getenv('ENV_FILE', '.env')
load_dotenv(env_file)


def build_database_uri():
    database_url = os.getenv('DATABASE_URL', '').strip()
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        if database_url.startswith('postgresql://'):
            return database_url.replace('postgresql://', 'postgresql+psycopg://', 1)
        return database_url

    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'root_password')
    db_name = os.getenv('DB_NAME', 'gimnasio')

    return f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

class Config:
    SQLALCHEMY_DATABASE_URI = build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
