from pydantic import BaseModel
from typing import Optional, List

class ChallengeBase(BaseModel):
    farmId: str
    pastPests: Optional[List[str]] = []
    pastDiseases: Optional[List[str]] = []
    weatherLosses: Optional[List[str]] = []
    marketAccess: Optional[str] = None

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeUpdate(BaseModel):
    pastPests: Optional[List[str]] = None
    pastDiseases: Optional[List[str]] = None
    weatherLosses: Optional[List[str]] = None
    marketAccess: Optional[str] = None

class Challenge(ChallengeBase):
    id: str # Will be the same as farmId
    class Config: from_attributes = True    