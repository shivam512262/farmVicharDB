from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas import soil_profile as sp_schema
from db.firestore_client import get_db
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime, timezone

router = APIRouter(tags=["Soil Profiles"])

@router.post("/api/farms/{farm_id}/soil-profiles/", response_model=sp_schema.SoilProfile, status_code=status.HTTP_201_CREATED)
def create_soil_profile(farm_id: str, sp_in: sp_schema.SoilProfileCreate, db: Client = Depends(get_db)):
    if sp_in.farmId != farm_id:
        raise HTTPException(status_code=400, detail="Farm ID in path and body do not match.")
    sp_data = sp_in.model_dump()
    sp_data['lastTestedAt'] = datetime.now(timezone.utc)
    _ , sp_ref = db.collection('soilProfiles').add(sp_data)
    created_doc = sp_ref.get()
    return sp_schema.SoilProfile(id=created_doc.id, **created_doc.to_dict())

@router.get("/api/farms/{farm_id}/soil-profiles/", response_model=List[sp_schema.SoilProfile])
def get_soil_profiles_for_farm(farm_id: str, db: Client = Depends(get_db)):
    sp_ref = db.collection('soilProfiles').where(filter=FieldFilter("farmId", "==", farm_id)).stream()
    return [sp_schema.SoilProfile(id=doc.id, **doc.to_dict()) for doc in sp_ref]

@router.get("/api/soil-profiles/{profile_id}", response_model=sp_schema.SoilProfile)
def get_soil_profile(profile_id: str, db: Client = Depends(get_db)):
    sp_doc = db.collection('soilProfiles').document(profile_id).get()
    if not sp_doc.exists:
        raise HTTPException(status_code=404, detail="Soil profile not found")
    return sp_schema.SoilProfile(id=sp_doc.id, **sp_doc.to_dict())

@router.patch("/api/soil-profiles/{profile_id}", response_model=sp_schema.SoilProfile)
def update_soil_profile(profile_id: str, sp_update: sp_schema.SoilProfileUpdate, db: Client = Depends(get_db)):
    sp_ref = db.collection('soilProfiles').document(profile_id)
    if not sp_ref.get().exists:
        raise HTTPException(status_code=404, detail="Soil profile not found")
    update_data = sp_update.model_dump(exclude_unset=True)
    update_data['lastTestedAt'] = datetime.now(timezone.utc)
    sp_ref.update(update_data)
    updated_doc = sp_ref.get()
    return sp_schema.SoilProfile(id=updated_doc.id, **updated_doc.to_dict())