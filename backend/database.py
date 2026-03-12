from sqlalchemy import create_engine, Column, Integer, String, Date, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./cpe_database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class CPEMessage(Base):
    __tablename__ = "cpes"

    id = Column(Integer, primary_key=True, index=True)
    cpe_title = Column(String, index=True)
    cpe_22_uri = Column(Text, index=True)
    cpe_23_uri = Column(Text, index=True)
    reference_links = Column(JSON)
    cpe_22_deprecation_date = Column(Date, nullable=True)
    cpe_23_deprecation_date = Column(Date, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)
