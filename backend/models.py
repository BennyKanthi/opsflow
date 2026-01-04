from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base, SessionLocal

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    invoices = relationship("Invoice", back_populates="user")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, nullable=False)
    upload_time = Column(DateTime, index=True, default=datetime.utcnow)
    status = Column(String, nullable=False, default = "uploaded")
    uploaded_by = Column(Integer, ForeignKey("users.id"), index=True)

    user = relationship("User", back_populates="invoices")

class InvoiceData(Base):
    __tablename__ = "invoice_data"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), index=True)
    invoice_number = Column(String, index=True)
    vendor_name = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    extracted_at = Column(DateTime, default=datetime.utcnow)

    invoice = relationship("Invoice", back_populates="data")

Invoice.data = relationship("InvoiceData", back_populates="invoice")


db = SessionLocal()

# Example: get all invoices for user 1
user = db.get(User, 1)
for invoice in user.invoices:
    print(invoice.filename)