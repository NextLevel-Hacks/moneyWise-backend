from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGODB_URL = os.getenv("MONGODB_URL")
    DATABASE_NAME = "cashflow_compass"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    JWT_EXPIRY_MINUTES = int(os.getenv("JWT_EXPIRY_MINUTES"))

settings = Settings()