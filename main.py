# re-crm-app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models

app = FastAPI(
    title="AgentFlow CRM API",
    description="Decoupled backend engine tracking contacts and property equity milestones."
)

# 🚀 AUTOMATICALLY AUTO-GENERATE THE CRM TABLES IN THE NEW crm_db
models.Base.metadata.create_all(bind=engine)

# Dependency to safely handle database sessions per API call
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "application": "AgentFlow Real Estate Engine",
        "version": "1.0.0"
    }

# 🚀 SEED PROTOTYPE DATA ENDPOINT
@app.get("/seed-prototype")
def seed_prototype_data(db: Session = Depends(get_db)):
    # Check if we've already seeded to prevent duplicates
    existing_contact = db.query(models.Contact).filter(models.Contact.email == "testclient@example.com").first()
    if existing_contact:
        return {"message": "Prototype database already seeded with sample contact records."}
        
    try:
        # 1. Create a mock high-value past client profile
        mock_contact = models.Contact(
            first_name="Robert",
            last_name="Chen",
            email="testclient@example.com",
            phone="415-555-0192",
            lifecycle_stage="Past Client"
        )
        db.add(mock_contact)
        db.commit() # Commit first to generate the contact ID
        db.refresh(mock_contact)
        
        # 2. Add an associated physical property asset to their profile
        mock_property = models.Property(
            contact_id=mock_contact.id,
            street_address="742 Evergreen Terrace",
            city="San Francisco",
            state="CA",
            purchase_price=850000.00,
            current_mortgage_balance=510000.00
        )
        db.add(mock_property)
        db.commit()
        
        return {
            "status": "Success",
            "message": "Pristine prototype real estate data injected into crm_db.",
            "seeded_records": {
                "contact_id": mock_contact.id,
                "client_name": f"{mock_contact.first_name} {mock_contact.last_name}",
                "property_linked": mock_property.street_address
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database seeding error: {str(e)}")
