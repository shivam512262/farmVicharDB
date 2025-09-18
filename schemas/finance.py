from pydantic import BaseModel
from typing import Optional, List

class FinanceBase(BaseModel):
    userId: str
    sellingMarket: Optional[str] = None
    eligibleSchemes: Optional[List[str]] = []
    appliedSchemes: Optional[List[str]] = []
    loanStatus: Optional[str] = 'none'

class FinanceCreate(FinanceBase):
    pass

class FinanceUpdate(BaseModel):
    sellingMarket: Optional[str] = None
    eligibleSchemes: Optional[List[str]] = None
    appliedSchemes: Optional[List[str]] = None
    loanStatus: Optional[str] = None

class Finance(FinanceBase):
    id: str
    class Config: from_attributes = True
    