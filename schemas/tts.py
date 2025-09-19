from pydantic import BaseModel
from enum import Enum

class Language(str, Enum):
    english = "english"
    hindi = "hindi"
    marathi = "marathi"
    malayalam = "malayalam"

class TTSRequest(BaseModel):
    text: str
    language: Language