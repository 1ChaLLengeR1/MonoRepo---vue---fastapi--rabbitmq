from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from main_backend.utils.env import get_env_variable

host = get_env_variable("DB_HOST_2")
port = get_env_variable("DB_PORT_2")
user = get_env_variable("DB_USER_2")
password = get_env_variable("DB_PASSWORD_2")
dbName = get_env_variable("DB_DBNAME_2")

if not all([host, port, user, password, dbName]):
    raise ValueError("One or more database environment variables are missing.")

data_base_url = f"postgresql://{user}:{password}@{host}:{port}/{dbName}"
engine = create_engine(data_base_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
