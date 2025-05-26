from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database.connection import Base

class CrimeType(enum.Enum):
    THEFT = "theft"
    ASSAULT = "assault"
    VANDALISM = "vandalism"
    BURGLARY = "burglary"
    FRAUD = "fraud"
    OTHER = "other"

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(CrimeType), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    description = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    
    # Relationships
    location = relationship("Location", back_populates="incidents")
    persons = relationship("Person", back_populates="incident")

    def __repr__(self):
        return f"<Incident(id={self.id}, type={self.type.value}, date={self.date})>" 