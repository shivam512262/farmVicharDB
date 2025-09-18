from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas import farm as farm_schema
from db.firestore_client import get_db
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime, timezone

router = APIRouter(tags=["Farms"])

@router.post("/api/users/{user_id}/farms/", response_model=farm_schema.Farm, status_code=status.HTTP_201_CREATED)
def create_farm(user_id: str, farm_in: farm_schema.FarmCreate, db: Client = Depends(get_db)):
    if farm_in.userId != user_id:
        raise HTTPException(status_code=400, detail="User ID in path and body do not match.")
    farm_data = farm_in.model_dump()
    farm_data['lastUpdated'] = datetime.now(timezone.utc)
    _ , farm_ref = db.collection('farms').add(farm_data)
    created_doc = farm_ref.get()
    return farm_schema.Farm(id=created_doc.id, **created_doc.to_dict())

@router.get("/api/users/{user_id}/farms/", response_model=List[farm_schema.Farm])
def get_farms_for_user(user_id: str, db: Client = Depends(get_db)):
    farms_ref = db.collection('farms').where(filter=FieldFilter("userId", "==", user_id)).stream()
    return [farm_schema.Farm(id=doc.id, **doc.to_dict()) for doc in farms_ref]

@router.get("/api/farms/{farm_id}", response_model=farm_schema.Farm)
def get_farm(farm_id: str, db: Client = Depends(get_db)):
    farm_doc = db.collection('farms').document(farm_id).get()
    if not farm_doc.exists:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm_schema.Farm(id=farm_doc.id, **farm_doc.to_dict())

@router.patch("/api/farms/{farm_id}", response_model=farm_schema.Farm)
def update_farm(farm_id: str, farm_update: farm_schema.FarmUpdate, db: Client = Depends(get_db)):
    farm_ref = db.collection('farms').document(farm_id)
    if not farm_ref.get().exists:
        raise HTTPException(status_code=404, detail="Farm not found")
    update_data = farm_update.model_dump(exclude_unset=True)
    update_data['lastUpdated'] = datetime.now(timezone.utc)
    farm_ref.update(update_data)
    updated_doc = farm_ref.get()
    return farm_schema.Farm(id=updated_doc.id, **updated_doc.to_dict())

@router.delete("/api/farms/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farm(farm_id: str, db: Client = Depends(get_db)):
    # Note: In a real app, you'd also delete all child documents (logs, crops, etc.)
    farm_ref = db.collection('farms').document(farm_id)
    if not farm_ref.get().exists:
        raise HTTPException(status_code=404, detail="Farm not found")
    farm_ref.delete()
    return