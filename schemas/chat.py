from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatBase(BaseModel):
    farmId: str
    messageType: str
    messageText: str

class ChatCreate(ChatBase):
    pass

class ChatUpdate(BaseModel):
    messageText: Optional[str] = None

class Chat(ChatBase):
    id: str
    timestamp: datetime
    class Config: from_attributes = True