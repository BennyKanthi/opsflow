from backend.database import Base, engine
from backend.models import User, Invoice, InvoiceData

# Create tables in the database
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")