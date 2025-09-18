from fastapi import APIRouter, Depends, HTTPException, status
from schemas import crop as crop_schema
from db.firestore_client import get_db
from google.cloud.firestore_v1.client import Client
from datetime import datetime, timezone

router = APIRouter(prefix="/api/farms/{farm_id}/crops", tags=["Crops"])

@router.post("/", response_model=crop_schema.Crop, status_code=status.HTTP_201_CREATED)
def create_or_replace_crop_profile(farm_id: str, crop_in: crop_schema.CropCreate, db: Client = Depends(get_db)):
    if crop_in.farmId != farm_id:
        raise HTTPException(status_code=400, detail="Farm ID in path and body do not match.")
    
    crop_ref = db.collection('crops').document(farm_id)
    crop_data = crop_in.model_dump()
    crop_data['createdAt'] = datetime.now(timezone.utc)
    
    # Use set() to create or overwrite the document with the farm_id
    crop_ref.set(crop_data)
    created_doc = crop_ref.get()
    return crop_schema.Crop(id=created_doc.id, **created_doc.to_dict())

@router.get("/", response_model=crop_schema.Crop)
def get_crop_profile(farm_id: str, db: Client = Depends(get_db)):
    crop_doc = db.collection('crops').document(farm_id).get()
    if not crop_doc.exists:
        raise HTTPException(status_code=404, detail="Crop profile not found for this farm")
    return crop_schema.Crop(id=crop_doc.id, **crop_doc.to_dict())

@router.patch("/", response_model=crop_schema.Crop)
def update_crop_profile(farm_id: str, crop_update: crop_schema.CropUpdate, db: Client = Depends(get_db)):
    crop_ref = db.collection('crops').document(farm_id)
    if not crop_ref.get().exists:
        raise HTTPException(status_code=404, detail="Crop profile not found for this farm")
    update_data = crop_update.model_dump(exclude_unset=True)
    crop_ref.update(update_data)
    updated_doc = crop_ref.get()
    return crop_schema.Crop(id=updated_doc.id, **updated_doc.to_dict())