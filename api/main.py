from fastapi import FastAPI, Depends
from config.database import connect_db, close_db
from api.dependencies import get_database

app = FastAPI(title="CashFlow Compass")

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    connect_db()

@app.on_event("shutdown")
async def shutdown_event():
    close_db()

# Test route with MongoDB
@app.get("/")
async def root(db=Depends(get_database)):
    # Test MongoDB connection
    db.command("ping")
    return {"message": "Welcome to CashFlow Compass! MongoDB is connected."}