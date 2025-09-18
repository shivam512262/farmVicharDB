from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class LogBase(BaseModel):
    farmId: str
    activityType: str
    description: str
    geoLocation: Optional[Dict[str, float]] = None

class LogCreate(LogBase):
    pass

class LogUpdate(BaseModel):
    activityType: Optional[str] = None
    description: Optional[str] = None
    geoLocation: Optional[Dict[str, float]] = None

class Log(LogBase):
    id: str
    timestamp: datetime
    class Config: from_attributes = True