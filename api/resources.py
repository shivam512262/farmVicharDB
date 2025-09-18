from fastapi import APIRouter, Depends, HTTPException, status
from schemas import resource as resource_schema
from db.firestore_client import get_db
from google.cloud.firestore_v1.client import Client

router = APIRouter(prefix="/api/farms/{farm_id}/resources", tags=["Resources"])

@router.post("/", response_model=resource_schema.Resource, status_code=status.HTTP_201_CREATED)
def create_or_replace_resource_profile(farm_id: str, resource_in: resource_schema.ResourceCreate, db: Client = Depends(get_db)):
    if resource_in.farmId != farm_id:
        raise HTTPException(status_code=400, detail="Farm ID in path and body do not match.")
    resource_ref = db.collection('resources').document(farm_id)
    resource_data = resource_in.model_dump()
    resource_ref.set(resource_data)
    created_doc = resource_ref.get()
    return resource_schema.Resource(id=created_doc.id, **created_doc.to_dict())

@router.get("/", response_model=resource_schema.Resource)
def get_resource_profile(farm_id: str, db: Client = Depends(get_db)):
    doc = db.collection('resources').document(farm_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Resource profile not found for this farm")
    return resource_schema.Resource(id=doc.id, **doc.to_dict())

@router.patch("/", response_model=resource_schema.Resource)
def update_resource_profile(farm_id: str, resource_update: resource_schema.ResourceUpdate, db: Client = Depends(get_db)):
    ref = db.collection('resources').document(farm_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Resource profile not found for this farm")
    update_data = resource_update.model_dump(exclude_unset=True)
    ref.update(update_data)
    updated_doc = ref.get()
    return resource_schema.Resource(id=updated_doc.id, **updated_doc.to_dict())