from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import engine, SessionLocal
import models
import schemas

app = FastAPI(
    title="AgentFlow CRM API",
    description="Decoupled backend engine tracking contacts and property equity milestones."
)

# Automatically generate database tables
models.Base.metadata.create_all(bind=engine)

# DB Session dependency
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


# --- CONTACTS PIPELINE ENDPOINTS ---

@app.get("/contacts", response_model=List[schemas.ContactResponse], tags=["Contacts"])
def get_all_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Fetch all CRM contacts along with their linked property portfolios."""
    return db.query(models.Contact).offset(skip).limit(limit).all()


@app.post("/contacts", response_model=schemas.ContactResponse, status_code=status.HTTP_201_CREATED, tags=["Contacts"])
def create_new_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    """Create a brand new lead or client in the CRM pipeline."""
    db_contact = db.query(models.Contact).filter(models.Contact.email == contact.email).first()
    if db_contact:
        raise HTTPException(status_code=400, detail="A contact with this email address already exists.")
    
    new_contact = models.Contact(**contact.model_dump())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


# --- PROPERTIES PIPELINE ENDPOINTS ---

@app.get("/properties", response_model=List[schemas.PropertyResponse], tags=["Properties"])
def get_all_properties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Fetch all real estate property transactions recorded in the system."""
    return db.query(models.Property).offset(skip).limit(limit).all()


@app.post("/properties", response_model=schemas.PropertyResponse, status_code=status.HTTP_201_CREATED, tags=["Properties"])
def link_property_to_contact(property_data: schemas.PropertyCreate, db: Session = Depends(get_db)):
    """Log a property asset transaction and bind it explicitly to a client profile ID."""
    db_contact = db.query(models.Contact).filter(models.Contact.id == property_data.contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=44, detail="Target contact ID not found in database.")
    
    new_property = models.Property(**property_data.model_dump())
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return new_property


# --- SEED PROTOTYPE DATA ENDPOINT ---
@app.get("/seed-prototype", tags=["Utilities"])
def seed_prototype_data(db: Session = Depends(get_db)):
    existing_contact = db.query(models.Contact).filter(models.Contact.email == "testclient@example.com").first()
    if existing_contact:
        return {"message": "Prototype database already seeded with sample contact records."}
        
    try:
        mock_contact = models.Contact(
            first_name="Robert",
            last_name="Chen",
            email="testclient@example.com",
            phone="415-555-0192",
            lifecycle_stage="Past Client"
        )
        db.add(mock_contact)
        db.commit()
        db.refresh(mock_contact)
        
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
            "message": "Pristine prototype real estate data injected into crm_db."
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database seeding error: {str(e)}")