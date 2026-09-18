from pydantic import BaseModel, EmailStr
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

# --- PROPERTY SCHEMAS ---
class PropertyBase(BaseModel):
    street_address: str
    city: str
    state: str
    purchase_price: Decimal
    current_mortgage_balance: Optional[Decimal] = None

class PropertyCreate(PropertyBase):
    contact_id: int

class PropertyResponse(PropertyBase):
    id: int
    contact_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- CONTACT SCHEMAS ---
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    lifecycle_stage: Optional[str] = "Lead" # e.g., Lead, Active Buyer, Under Contract, Past Client

class ContactCreate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    properties: List[PropertyResponse] = []

    class Config:
        from_attributes = True