from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas import alert as alert_schema
from db.firestore_client import get_db
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime, timezone

router = APIRouter(tags=["Alerts"])

@router.post("/api/users/{user_id}/alerts/", response_model=alert_schema.Alert, status_code=status.HTTP_201_CREATED)
def create_alert(user_id: str, alert_in: alert_schema.AlertCreate, db: Client = Depends(get_db)):
    if alert_in.userId != user_id:
        raise HTTPException(status_code=400, detail="User ID in path and body do not match.")
    data = alert_in.model_dump()
    data['createdAt'] = datetime.now(timezone.utc)
    _ , ref = db.collection('alerts').add(data)
    doc = ref.get()
    return alert_schema.Alert(id=doc.id, **doc.to_dict())

@router.get("/api/users/{user_id}/alerts/", response_model=List[alert_schema.Alert])
def get_alerts_for_user(user_id: str, db: Client = Depends(get_db)):
    docs = db.collection('alerts').where(filter=FieldFilter("userId", "==", user_id)).order_by("createdAt", direction="DESCENDING").stream()
    return [alert_schema.Alert(id=doc.id, **doc.to_dict()) for doc in docs]

@router.get("/api/alerts/{alert_id}", response_model=alert_schema.Alert)
def get_alert(alert_id: str, db: Client = Depends(get_db)):
    doc = db.collection('alerts').document(alert_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert_schema.Alert(id=doc.id, **doc.to_dict())

@router.patch("/api/alerts/{alert_id}", response_model=alert_schema.Alert)
def update_alert(alert_id: str, alert_update: alert_schema.AlertUpdate, db: Client = Depends(get_db)):
    ref = db.collection('alerts').document(alert_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Alert not found")
    update_data = alert_update.model_dump(exclude_unset=True)
    ref.update(update_data)
    updated_doc = ref.get()
    return alert_schema.Alert(id=updated_doc.id, **updated_doc.to_dict())