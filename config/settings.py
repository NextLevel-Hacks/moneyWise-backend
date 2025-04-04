from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGODB_URL = os.getenv("MONGODB_URL")
    DATABASE_NAME = "cashflow_compass"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    JWT_EXPIRY_MINUTES = int(os.getenv("JWT_EXPIRY_MINUTES"))
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") 
    RESET_TOKEN_EXPIRY_MINUTES = 30 

settings = Settings()