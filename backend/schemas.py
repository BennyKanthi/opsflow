from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class InvoiceCreate(BaseModel):
    filename: str

class InvoiceRead(BaseModel):
    id: int
    filename: str
    status: str
    upload_time: datetime

    class Config:
        from_attributes = True

class InvoiceDataCreate(BaseModel):
    invoice_id: int
    invoice_number: str
    vendor_name: str
    total_amount: float

class InvoiceDataRead(BaseModel):
    id: int
    invoice_number: str
    vendor_name: str
    total_amount: float
    confidence_score: float
    extracted_at: datetime

    class Config:
        from_attributes = True