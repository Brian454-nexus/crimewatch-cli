from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from database.connection import Base

class PersonType(enum.Enum):
    VICTIM = "victim"
    WITNESS = "witness"

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact = Column(String)  # Optional contact information
    type = Column(Enum(PersonType), nullable=False)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    
    # Relationships
    incident = relationship("Incident", back_populates="persons")

    def __repr__(self):
        return f"<Person(id={self.id}, name={self.name}, type={self.type.value})>" 