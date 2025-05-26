from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.connection import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    street = Column(String, nullable=False)
    neighborhood = Column(String, nullable=False)
    city = Column(String, nullable=False)
    zone = Column(String)  # Optional zone for grouping (e.g., "Zone A", "Zone B")

    # Relationships
    incidents = relationship("Incident", back_populates="location")

    def __repr__(self):
        return f"<Location(id={self.id}, street={self.street}, neighborhood={self.neighborhood})>" 