from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend import models, schemas

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

@router.post("/", response_model=schemas.InvoiceRead)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    db_invoice = models.Invoice(
        filename = invoice.filename,
        status="uploaded"
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

@router.get("/{invoice_filename}", response_model=schemas.InvoiceRead)
def read_invoice(invoice_filename: str, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.filename == invoice_filename).first()

    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return invoice