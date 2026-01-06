from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend import models, schemas

router = APIRouter(
    prefix="/invoices_data",
    tags=["Invoices Data"]
)

@router.post("/", response_model=schemas.InvoiceDataRead)
def create_invoice_data(invoice_data: schemas.InvoiceDataCreate, db: Session = Depends(get_db)):
    db_invoice_data = models.InvoiceData(
        invoice_id = invoice_data.invoice_id,
        invoice_number = invoice_data.invoice_number,
        vendor_name = invoice_data.vendor_name,
        total_amount = invoice_data.total_amount,
        confidence_score = getattr(invoice_data, 'confidence_score', 0.0)  # optional default
    )
    db.add(db_invoice_data)
    db.commit()
    db.refresh(db_invoice_data)
    return db_invoice_data

@router.get("/{invoice_data_number}", response_model=schemas.InvoiceDataRead)
def read_invoice_data(invoice_data_number: str, db: Session = Depends(get_db)):
    invoice_data = db.query(models.InvoiceData)\
                     .filter(models.InvoiceData.invoice_number == invoice_data_number)\
                     .first()

    if invoice_data is None:
        raise HTTPException(status_code=404, detail="Invoice data not found")

    return invoice_data