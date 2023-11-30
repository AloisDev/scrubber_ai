import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")
GOOGLE_ADDRESS_VALIDATION_URL = os.getenv("GOOGLE_ADDRESS_VALIDATION_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
