from backend.database import SessionLocal
from backend.models import User, Invoice, InvoiceData

# Open a session
db = SessionLocal()

# Add a test user
test_user = User(email="test@example.com", password_hash="hashed")
db.add(test_user)
db.commit()
db.refresh(test_user)

# Add a test invoice
test_invoice = Invoice(filename="invoice1.pdf", uploaded_by=test_user.id)
db.add(test_invoice)
db.commit()
db.refresh(test_invoice)

# Add a test invoice data
test_invoice_data = InvoiceData(
    invoice_id=test_invoice.id,
    invoice_number="INV-001",
    vendor_name="VendorX",
    total_amount=123.45,
    confidence_score=0.99
)
db.add(test_invoice_data)
db.commit()
db.refresh(test_invoice_data)

# Query back
user = db.get(User, test_user.id)
print(f"User: {user.email}")
for invoice in user.invoices:
    print(f"Invoice: {invoice.filename}, Status: {invoice.status}")
    for data in invoice.data:
        print(f"  InvoiceData: {data.invoice_number}, Vendor: {data.vendor_name}, Total: {data.total_amount}")
