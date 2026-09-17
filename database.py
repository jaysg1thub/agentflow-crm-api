# re-crm-app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🚀 TARGETING AN ISOLATED CRM DATABASE INSTANCE
# DATABASE_URL = "postgresql+psycopg://postgres:admin@localhost:5432/crm_db"

# 🚀 Container-aware connection switch with a localhost fallback
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+psycopg://postgres:admin@localhost:5432/crm_db"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()