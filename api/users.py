# api/users.py
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List, Dict, Any 
from typing import List
from schemas import user as user_schema
from db.firestore_client import get_db
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime, timezone

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/register", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def register_user(user_in: user_schema.UserCreate, db: Client = Depends(get_db)):
    """
    Registers a new user by hashing their password and saving it to the database.
    """
    users_ref = db.collection('users').where(filter=FieldFilter('phone', '==', user_in.phone)).limit(1).stream()
    if any(users_ref):
        raise HTTPException(status_code=409, detail="User with this phone number already exists.")
    
    # Hash the plain-text password using bcrypt
    hashed_password = bcrypt.hashpw(user_in.password.encode('utf-8'), bcrypt.gensalt())
    
    user_data = user_in.model_dump(exclude={"password"})
    user_data['hashed_password'] = hashed_password.decode('utf-8') # Store the hash
    user_data['createdAt'] = datetime.now(timezone.utc)
    user_data['lastLogin'] = datetime.now(timezone.utc)

    _ , user_ref = db.collection('users').add(user_data)
    created_doc = user_ref.get()
    return user_schema.User(id=created_doc.id, **created_doc.to_dict())


@router.post("/login", response_model=user_schema.User)
def login_user(login_data: user_schema.UserLogin, db: Client = Depends(get_db)):
    """
    Logs a user in by verifying their password against the stored hash.
    Returns the user's data upon success.
    """
    users_stream = db.collection('users').where(filter=FieldFilter('phone', '==', login_data.phone)).limit(1).stream()
    user_doc = next(users_stream, None)
    
    # Check if user exists
    if not user_doc:
        raise HTTPException(status_code=404, detail="User with this phone number not found")
    
    user_data = user_doc.to_dict()
    stored_hash = user_data.get("hashed_password", "").encode('utf-8')

    # Securely check the provided password against the stored hash
    if not bcrypt.checkpw(login_data.password.encode('utf-8'), stored_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # If password is correct, update lastLogin timestamp and return user data
    user_doc.reference.update({"lastLogin": datetime.now(timezone.utc)})
    
    # Refetch the document to include the updated lastLogin time in the response
    updated_doc = user_doc.reference.get()
    
    return user_schema.User(id=updated_doc.id, **updated_doc.to_dict())


# --- Other User Management Endpoints ---

@router.get("/", response_model=List[user_schema.User])
def get_all_users(db: Client = Depends(get_db)):
    users_ref = db.collection('users').stream()
    return [user_schema.User(id=doc.id, **doc.to_dict()) for doc in users_ref]


@router.get("/{user_id}", response_model=user_schema.User)
def get_user(user_id: str, db: Client = Depends(get_db)):
    user_doc = db.collection('users').document(user_id).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    return user_schema.User(id=user_doc.id, **user_doc.to_dict())


@router.patch("/{user_id}", response_model=user_schema.User)
def update_user(user_id: str, user_update: user_schema.UserUpdate, db: Client = Depends(get_db)):
    user_ref = db.collection('users').document(user_id)
    if not user_ref.get().exists:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.model_dump(exclude_unset=True)
    user_ref.update(update_data)
    updated_doc = user_ref.get()
    return user_schema.User(id=updated_doc.id, **updated_doc.to_dict())


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Client = Depends(get_db)):
    user_ref = db.collection('users').document(user_id)
    if not user_ref.get().exists:
        raise HTTPException(status_code=404, detail="User not found")
    user_ref.delete()
    return

@router.get("/{user_id}/profile/deep", response_model=Dict[str, Any])
def get_full_user_profile(user_id: str, db: Client = Depends(get_db)):
    """
    Performs a "deep fetch" to retrieve all data related to a single user,
    including their profile, farms, and all farm-related sub-collections.
    """
    full_profile = {}

    # 1. Fetch the main user profile
    user_doc = db.collection('users').document(user_id).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    full_profile['profile'] = {"id": user_doc.id, **user_doc.to_dict()}

    # 2. Fetch all user-centric collections
    finance_docs = db.collection('finance').where(filter=FieldFilter("userId", "==", user_id)).stream()
    full_profile['finance_records'] = [{"id": doc.id, **doc.to_dict()} for doc in finance_docs]
    
    alert_docs = db.collection('alerts').where(filter=FieldFilter("userId", "==", user_id)).stream()
    full_profile['alerts'] = [{"id": doc.id, **doc.to_dict()} for doc in alert_docs]

    # 3. Fetch all farms for the user
    farm_docs = db.collection('farms').where(filter=FieldFilter("userId", "==", user_id)).stream()
    farms_list = []
    
    for farm_doc in farm_docs:
        farm_data = {"id": farm_doc.id, **farm_doc.to_dict()}
        farm_id = farm_doc.id
        
        # 4. For each farm, fetch all its related data
        # One-to-one profiles
        farm_data['crop_profile'] = db.collection('crops').document(farm_id).get().to_dict()
        farm_data['resource_profile'] = db.collection('resources').document(farm_id).get().to_dict()
        farm_data['challenge_profile'] = db.collection('challenges').document(farm_id).get().to_dict()

        # One-to-many profiles
        soil_docs = db.collection('soilProfiles').where(filter=FieldFilter("farmId", "==", farm_id)).stream()
        farm_data['soil_profiles'] = [{"id": doc.id, **doc.to_dict()} for doc in soil_docs]

        log_docs = db.collection('logs').where(filter=FieldFilter("farmId", "==", farm_id)).stream()
        farm_data['activity_logs'] = [{"id": doc.id, **doc.to_dict()} for doc in log_docs]
        
        chat_docs = db.collection('chats').where(filter=FieldFilter("farmId", "==", farm_id)).stream()
        farm_data['chat_history'] = [{"id": doc.id, **doc.to_dict()} for doc in chat_docs]

        farms_list.append(farm_data)

    full_profile['farms'] = farms_list
    
    return full_profile