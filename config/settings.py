from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGODB_URL = os.getenv("MONGODB_URL")
    DATABASE_NAME = "cashflow_compass"

settings = Settings()