import sys
import traceback

try:
    print("Step 1: Importing modules...")
    from backend.database import Base, engine, SessionLocal
    from backend.models import User, Invoice, InvoiceData
    print("✓ Imports successful\n")
    
    print("Step 2: Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created\n")
    
    print("Step 3: Testing database...")
    db = SessionLocal()
    
    # Clear existing test data
    db.query(InvoiceData).filter(InvoiceData.invoice_id.in_(
        db.query(Invoice.id).filter(Invoice.uploaded_by.in_(
            db.query(User.id).filter(User.email == 'test@example.com')
        ))
    )).delete(synchronize_session=False)
    db.query(Invoice).filter(Invoice.uploaded_by.in_(
        db.query(User.id).filter(User.email == 'test@example.com')
    )).delete(synchronize_session=False)
    db.query(User).filter(User.email == 'test@example.com').delete()
    db.commit()
    
    test_user = User(email="test@example.com", password_hash="hashed")
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    print(f"✓ User created: {test_user.email}")
    
    test_invoice = Invoice(filename="invoice1.pdf", uploaded_by=test_user.id)
    db.add(test_invoice)
    db.commit()
    db.refresh(test_invoice)
    print(f"✓ Invoice created: {test_invoice.filename}")
    
    test_invoice_data = InvoiceData(
        invoice_id=test_invoice.id,
        invoice_number="INV-001",
        vendor_name="VendorX",
        total_amount=123.45,
        confidence_score=0.99
    )
    db.add(test_invoice_data)
    db.commit()
    print(f"✓ Invoice data created: {test_invoice_data.invoice_number}\n")
    
    print("Step 4: Querying data...")
    user = db.get(User, test_user.id)
    print(f"User: {user.email}")
    for invoice in user.invoices:
        print(f"  Invoice: {invoice.filename}, Status: {invoice.status}")
        for data in invoice.data:
            print(f"    Data: {data.invoice_number}, Vendor: {data.vendor_name}, Total: ${data.total_amount}")
    
    print("\n✓ ALL TESTS PASSED!")
    
except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    traceback.print_exc()
finally:
    if 'db' in locals():
        db.close()