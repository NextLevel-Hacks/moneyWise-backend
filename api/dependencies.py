from fastapi import Depends
from config.database import get_db

def get_database():
    db = get_db()
    try:
        yield db
    finally:
        pass  # We'll close it manually in main.py if needed