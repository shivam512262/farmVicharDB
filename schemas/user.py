# schemas/user.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    fullName: str
    phone: str
    age: Optional[int] = None
    gender: Optional[str] = None
    preferredLanguage: Optional[str] = 'Malayalam'
    educationLevel: Optional[str] = None
    farmingExperienceYears: Optional[int] = None
    
class UserCreate(UserBase):
    password: str

# New schema for the login endpoint body
class UserLogin(BaseModel):
    phone: str
    password: str

class UserUpdate(BaseModel):
    fullName: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    preferredLanguage: Optional[str] = None
    educationLevel: Optional[str] = None
    farmingExperienceYears: Optional[int] = None

class User(UserBase):
    id: str
    createdAt: datetime
    lastLogin: Optional[datetime] = None
    class Config: 
        from_attributes = True