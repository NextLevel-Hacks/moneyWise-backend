from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from config.database import connect_db, close_db
from api.dependencies import get_database
from api.routers import auth, classify 

app = FastAPI(title="CashFlow Compass")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


app.include_router(auth.router, prefix="/api")
app.include_router(classify.router, prefix="/api")
# app.include_router(recommend.router, prefix="/api")
# app.include_router(actions.router, prefix="/api")
# app.include_router(risk.router, prefix="/api")
# app.include_router(notifications.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    connect_db()

@app.on_event("shutdown")
async def shutdown_event():
    close_db()

@app.get("/")
async def root(db=Depends(get_database)):
    db.command("ping")
    return {"message": "Welcome to CashFlow Compass! MongoDB is connected."}