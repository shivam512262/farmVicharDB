from fastapi import APIRouter, Depends, HTTPException, status
from schemas import challenge as challenge_schema
from db.firestore_client import get_db
from google.cloud.firestore_v1.client import Client

router = APIRouter(prefix="/api/farms/{farm_id}/challenges", tags=["Challenges"])

@router.post("/", response_model=challenge_schema.Challenge, status_code=status.HTTP_201_CREATED)
def create_or_replace_challenge_profile(farm_id: str, challenge_in: challenge_schema.ChallengeCreate, db: Client = Depends(get_db)):
    if challenge_in.farmId != farm_id:
        raise HTTPException(status_code=400, detail="Farm ID in path and body do not match.")
    ref = db.collection('challenges').document(farm_id)
    data = challenge_in.model_dump()
    ref.set(data)
    doc = ref.get()
    return challenge_schema.Challenge(id=doc.id, **doc.to_dict())

@router.get("/", response_model=challenge_schema.Challenge)
def get_challenge_profile(farm_id: str, db: Client = Depends(get_db)):
    doc = db.collection('challenges').document(farm_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Challenge profile not found for this farm")
    return challenge_schema.Challenge(id=doc.id, **doc.to_dict())

@router.patch("/", response_model=challenge_schema.Challenge)
def update_challenge_profile(farm_id: str, challenge_update: challenge_schema.ChallengeUpdate, db: Client = Depends(get_db)):
    ref = db.collection('challenges').document(farm_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Challenge profile not found for this farm")
    update_data = challenge_update.model_dump(exclude_unset=True)
    ref.update(update_data)
    updated_doc = ref.get()
    return challenge_schema.Challenge(id=updated_doc.id, **updated_doc.to_dict())   