from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    userId: str
    alertType: str
    message: str
    dueDate: Optional[datetime] = None
    status: str = 'unread'
    priority: int = 1 # 3=High, 2=Medium, 1=Low

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    message: Optional[str] = None
    dueDate: Optional[datetime] = None
    status: Optional[str] = None
    priority: Optional[int] = None

class Alert(AlertBase):
    id: str
    createdAt: datetime
    class Config: from_attributes = True