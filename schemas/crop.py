from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class CropBase(BaseModel):
    farmId: str
    currentCrop: Optional[str] = None
    season: Optional[str] = None
    cropRotationHistory: Optional[List[str]] = []
    yieldHistory: Optional[Dict[str, float]] = {}
    seedSource: Optional[str] = None

class CropCreate(CropBase):
    pass

class CropUpdate(BaseModel):
    currentCrop: Optional[str] = None
    season: Optional[str] = None
    cropRotationHistory: Optional[List[str]] = None
    yieldHistory: Optional[Dict[str, float]] = None
    seedSource: Optional[str] = None

class Crop(CropBase):
    id: str # Will be the same as farmId
    createdAt: datetime
    class Config: from_attributes = True