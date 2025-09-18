from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas import log as log_schema
from db.firestore_client import get_db
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime, timezone

router = APIRouter(tags=["Activity Logs"])

@router.post("/api/farms/{farm_id}/logs/", response_model=log_schema.Log, status_code=status.HTTP_201_CREATED)
def create_log(farm_id: str, log_in: log_schema.LogCreate, db: Client = Depends(get_db)):
    if log_in.farmId != farm_id:
        raise HTTPException(status_code=400, detail="Farm ID in path and body do not match.")
    data = log_in.model_dump()
    data['timestamp'] = datetime.now(timezone.utc)
    _ , ref = db.collection('logs').add(data)
    doc = ref.get()
    return log_schema.Log(id=doc.id, **doc.to_dict())

@router.get("/api/farms/{farm_id}/logs/", response_model=List[log_schema.Log])
def get_logs_for_farm(farm_id: str, db: Client = Depends(get_db)):
    docs = db.collection('logs').where(filter=FieldFilter("farmId", "==", farm_id)).order_by("timestamp", direction="DESCENDING").stream()
    return [log_schema.Log(id=doc.id, **doc.to_dict()) for doc in docs]

@router.get("/api/logs/{log_id}", response_model=log_schema.Log)
def get_log(log_id: str, db: Client = Depends(get_db)):
    doc = db.collection('logs').document(log_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Log not found")
    return log_schema.Log(id=doc.id, **doc.to_dict())

@router.patch("/api/logs/{log_id}", response_model=log_schema.Log)
def update_log(log_id: str, log_update: log_schema.LogUpdate, db: Client = Depends(get_db)):
    ref = db.collection('logs').document(log_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Log not found")
    update_data = log_update.model_dump(exclude_unset=True)
    ref.update(update_data)
    updated_doc = ref.get()
    return log_schema.Log(id=updated_doc.id, **updated_doc.to_dict())