from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas import finance as finance_schema
from db.firestore_client import get_db
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.base_query import FieldFilter

router = APIRouter(tags=["Finance"])

@router.post("/api/users/{user_id}/finance/", response_model=finance_schema.Finance, status_code=status.HTTP_201_CREATED)
def create_finance_profile(user_id: str, finance_in: finance_schema.FinanceCreate, db: Client = Depends(get_db)):
    if finance_in.userId != user_id:
        raise HTTPException(status_code=400, detail="User ID in path and body do not match.")
    data = finance_in.model_dump()
    _ , ref = db.collection('finance').add(data)
    doc = ref.get()
    return finance_schema.Finance(id=doc.id, **doc.to_dict())

@router.get("/api/users/{user_id}/finance/", response_model=List[finance_schema.Finance])
def get_finance_profiles_for_user(user_id: str, db: Client = Depends(get_db)):
    docs = db.collection('finance').where(filter=FieldFilter("userId", "==", user_id)).stream()
    return [finance_schema.Finance(id=doc.id, **doc.to_dict()) for doc in docs]

@router.get("/api/finance/{finance_id}", response_model=finance_schema.Finance)
def get_finance_profile(finance_id: str, db: Client = Depends(get_db)):
    doc = db.collection('finance').document(finance_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Finance profile not found")
    return finance_schema.Finance(id=doc.id, **doc.to_dict())

@router.patch("/api/finance/{finance_id}", response_model=finance_schema.Finance)
def update_finance_profile(finance_id: str, finance_update: finance_schema.FinanceUpdate, db: Client = Depends(get_db)):
    ref = db.collection('finance').document(finance_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Finance profile not found")
    update_data = finance_update.model_dump(exclude_unset=True)
    ref.update(update_data)
    updated_doc = ref.get()
    return finance_schema.Finance(id=updated_doc.id, **updated_doc.to_dict())