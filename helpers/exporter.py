import csv
import json
from datetime import datetime
from models.incident import Incident
from models.location import Location
from models.person import Person
from database.connection import get_db

def export_to_csv(filename="crime_report.csv"):
    """Export all incidents to CSV format."""
    db = next(get_db())
    try:
        incidents = db.query(Incident).all()
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow([
                'ID', 'Type', 'Date', 'Description',
                'Street', 'Neighborhood', 'City', 'Zone',
                'Victims', 'Witnesses'
            ])
            
            # Write data
            for incident in incidents:
                victims = [p.name for p in incident.persons if p.type.value == 'victim']
                witnesses = [p.name for p in incident.persons if p.type.value == 'witness']
                
                writer.writerow([
                    incident.id,
                    incident.type.value,
                    incident.date.strftime('%Y-%m-%d %H:%M'),
                    incident.description,
                    incident.location.street,
                    incident.location.neighborhood,
                    incident.location.city,
                    incident.location.zone or '',
                    '; '.join(victims),
                    '; '.join(witnesses)
                ])
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {str(e)}")
        return False
    finally:
        db.close()

def export_to_json(filename="crime_report.json"):
    """Export all incidents to JSON format."""
    db = next(get_db())
    try:
        incidents = db.query(Incident).all()
        data = []
        
        for incident in incidents:
            victims = [p.name for p in incident.persons if p.type.value == 'victim']
            witnesses = [p.name for p in incident.persons if p.type.value == 'witness']
            
            data.append({
                'id': incident.id,
                'type': incident.type.value,
                'date': incident.date.strftime('%Y-%m-%d %H:%M'),
                'description': incident.description,
                'location': {
                    'street': incident.location.street,
                    'neighborhood': incident.location.neighborhood,
                    'city': incident.location.city,
                    'zone': incident.location.zone
                },
                'victims': victims,
                'witnesses': witnesses
            })
        
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=2)
        return True
    except Exception as e:
        print(f"Error exporting to JSON: {str(e)}")
        return False
    finally:
        db.close() 