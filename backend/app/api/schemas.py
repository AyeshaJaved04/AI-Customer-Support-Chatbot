from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2)
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ChatRequest(BaseModel):
    user_id: int
    message: str = Field(min_length=1, max_length=2000)

class ChatResponse(BaseModel):
    response: str
    sentiment: str
    sentiment_score: float
    sources: List[str]
    escalated: bool = False

class PurchaseCreate(BaseModel):
    product_id: str
    product_name: str
    category: Optional[str] = None
    price: float = Field(gt=0)

class TicketResponse(BaseModel):
    id: int
    subject: str
    priority: str
    status: str
    created_at: datetime
    class Config:
        from_attributes = True