# main.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from api import users, farms, soil_profiles, crops, resources, challenges, finance, chats, logs, alerts
from db.firestore_client import initialize_firestore

app = FastAPI(
    title="Krishi Sakhi POC API",
    version="2.0.0"
)

@app.on_event("startup")
def startup_event():
    initialize_firestore()

# Include all 10 routers
app.include_router(users.router)
app.include_router(farms.router)
app.include_router(soil_profiles.router)
app.include_router(crops.router)
app.include_router(resources.router)
app.include_router(challenges.router)
app.include_router(finance.router)
app.include_router(chats.router_for_farm)
app.include_router(chats.router_for_single_chat)
app.include_router(logs.router)
app.include_router(alerts.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Krishi Sakhi POC API"}