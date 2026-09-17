# re-crm-app/models.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(30), nullable=True)
    lifecycle_stage = Column(String(50), default="Past Client")  # e.g., Lead, Active Buyer, Past Client
    created_at = Column(DateTime, server_default=func.now())

    # Relationship linking back to their properties
    properties = relationship("Property", back_populates="owner", cascade="all, delete-orphan")

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False)
    street_address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    purchase_price = Column(Numeric(12, 2), nullable=False)
    current_mortgage_balance = Column(Numeric(12, 2), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    owner = relationship("Contact", back_populates="properties")