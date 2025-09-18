from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas import chat as chat_schema
from db.firestore_client import get_db
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.base_query import FieldFilter # Import FieldFilter
from datetime import datetime, timezone

router_for_farm = APIRouter(prefix="/api/farms/{farm_id}/chats", tags=["Chats"])
router_for_single_chat = APIRouter(prefix="/api/chats", tags=["Chats"])

@router_for_farm.post("/", response_model=chat_schema.Chat, status_code=status.HTTP_201_CREATED)
def create_chat_message(farm_id: str, chat_in: chat_schema.ChatCreate, db: Client = Depends(get_db)):
    if chat_in.farmId != farm_id:
        raise HTTPException(status_code=400, detail="Farm ID in path and body do not match.")
    
    farm_ref = db.collection('farms').document(farm_id)
    if not farm_ref.get().exists:
        raise HTTPException(status_code=404, detail="Farm not found")

    chat_data = chat_in.model_dump()
    chat_data['timestamp'] = datetime.now(timezone.utc)
    
    # Correctly save to the top-level 'chats' collection
    _ , chat_ref = db.collection('chats').add(chat_data)
    created_doc = chat_ref.get()
    return chat_schema.Chat(id=created_doc.id, **created_doc.to_dict())


@router_for_farm.get("/", response_model=List[chat_schema.Chat])
def get_chats_for_farm(farm_id: str, db: Client = Depends(get_db)):
    # THIS FUNCTION IS NOW CORRECTED
    farm_ref = db.collection('farms').document(farm_id)
    if not farm_ref.get().exists:
        raise HTTPException(status_code=404, detail="Farm not found")
        
    # Correctly query the top-level 'chats' collection and filter by farmId
    chats_ref = db.collection('chats').where(
        filter=FieldFilter("farmId", "==", farm_id)
    ).order_by("timestamp").stream()
    
    return [chat_schema.Chat(id=doc.id, **doc.to_dict()) for doc in chats_ref]

# --- (The single get and patch endpoints remain the same) ---
@router_for_single_chat.get("/{chat_id}", response_model=chat_schema.Chat)
def get_chat_message(chat_id: str, db: Client = Depends(get_db)):
    # ... code ...
    pass
@router_for_single_chat.patch("/{chat_id}", response_model=chat_schema.Chat)
def update_chat_message(chat_id: str, chat_update: chat_schema.ChatUpdate, db: Client = Depends(get_db)):
    # ... code ...
    pass