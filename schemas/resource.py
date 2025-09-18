from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ResourceBase(BaseModel):
    farmId: str
    machinery: Optional[List[str]] = []
    laborAvailability: Optional[str] = None
    fertilizerHistory: Optional[List[Dict[str, Any]]] = []
    pesticideHistory: Optional[List[Dict[str, Any]]] = []
    storageAccess: Optional[str] = None

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    machinery: Optional[List[str]] = None
    laborAvailability: Optional[str] = None
    fertilizerHistory: Optional[List[Dict[str, Any]]] = None
    pesticideHistory: Optional[List[Dict[str, Any]]] = None
    storageAccess: Optional[str] = None
    
class Resource(ResourceBase):
    id: str # Will be the same as farmId
    class Config: from_attributes = True    