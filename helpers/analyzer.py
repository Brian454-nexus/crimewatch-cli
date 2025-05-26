from sqlalchemy import func, desc
from datetime import datetime, timedelta
from models.incident import Incident, CrimeType
from models.location import Location
from database.connection import get_db

def get_top_crimes_by_month(months=1):
    """Get top 3 crime types for the last N months."""
    db = next(get_db())
    try:
        cutoff_date = datetime.now() - timedelta(days=30 * months)
        results = (
            db.query(Incident.type, func.count(Incident.id).label('count'))
            .filter(Incident.date >= cutoff_date)
            .group_by(Incident.type)
            .order_by(desc('count'))
            .limit(3)
            .all()
        )
        return [(crime_type.value, count) for crime_type, count in results]
    finally:
        db.close()

def get_most_dangerous_neighborhoods(limit=5):
    """Get top N most dangerous neighborhoods based on incident count."""
    db = next(get_db())
    try:
        results = (
            db.query(
                Location.neighborhood,
                func.count(Incident.id).label('incident_count')
            )
            .join(Incident)
            .group_by(Location.neighborhood)
            .order_by(desc('incident_count'))
            .limit(limit)
            .all()
        )
        return results
    finally:
        db.close()

def get_crime_trends():
    """Get crime trends over time (monthly breakdown)."""
    db = next(get_db())
    try:
        results = (
            db.query(
                func.strftime('%Y-%m', Incident.date).label('month'),
                func.count(Incident.id).label('count')
            )
            .group_by('month')
            .order_by('month')
            .all()
        )
        return results
    finally:
        db.close()

def get_crime_patterns():
    """Analyze patterns in crime data."""
    db = next(get_db())
    try:
        # Find streets with multiple incidents
        results = (
            db.query(
                Location.street,
                func.count(Incident.id).label('incident_count')
            )
            .join(Incident)
            .group_by(Location.street)
            .having(func.count(Incident.id) > 1)
            .order_by(desc('incident_count'))
            .all()
        )
        return results
    finally:
        db.close() 