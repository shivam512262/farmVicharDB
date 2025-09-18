from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class SoilProfileBase(BaseModel):
    farmId: str
    soilPH: Optional[float] = None
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    organicCarbon: Optional[float] = None
    micronutrients: Optional[Dict[str, float]] = None

class SoilProfileCreate(SoilProfileBase):
    pass

class SoilProfileUpdate(BaseModel):
    soilPH: Optional[float] = None
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    organicCarbon: Optional[float] = None
    micronutrients: Optional[Dict[str, float]] = None

class SoilProfile(SoilProfileBase):
    id: str
    lastTestedAt: datetime
    class Config: from_attributes = True