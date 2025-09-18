from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FarmBase(BaseModel):
    userId: str
    village: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pinCode: Optional[str] = None
    landStatus: Optional[str] = 'Owned'
    totalFarmArea: Optional[float] = None
    soilType: Optional[str] = None
    waterSource: Optional[str] = None
    irrigationMethod: Optional[str] = None
    climateNotes: Optional[str] = None
    yieldScore: Optional[float] = 0.0
    soilScore: Optional[float] = 0.0
    storageScore: Optional[float] = 0.0
    sustainabilityScore: Optional[float] = 0.0
    qualityScore: Optional[float] = 0.0

class FarmCreate(FarmBase):
    pass

class FarmUpdate(BaseModel):
    village: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pinCode: Optional[str] = None
    landStatus: Optional[str] = None
    totalFarmArea: Optional[float] = None
    soilType: Optional[str] = None
    waterSource: Optional[str] = None
    irrigationMethod: Optional[str] = None
    climateNotes: Optional[str] = None
    yieldScore: Optional[float] = None
    soilScore: Optional[float] = None
    storageScore: Optional[float] = None
    sustainabilityScore: Optional[float] = None
    qualityScore: Optional[float] = None

class Farm(FarmBase):
    id: str
    lastUpdated: datetime
    class Config: from_attributes = True    