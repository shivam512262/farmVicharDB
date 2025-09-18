import firebase_admin
from firebase_admin import firestore

db = None

def initialize_firestore():
    global db
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    db = firestore.client()
    print("✅ Firestore initialized successfully.")

def get_db():
    return db