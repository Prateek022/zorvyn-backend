from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class RecordCreate(BaseModel):
    amount: float
    type: str  # income or expense
    category: str
    date: datetime
    notes: Optional[str] = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        if v not in ["income", "expense"]:
            raise ValueError("type must be 'income' or 'expense'")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("amount must be greater than 0")
        return v


class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None


class RecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: datetime
    notes: Optional[str]
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class RecordFilter(BaseModel):
    type: Optional[str] = None
    category: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None