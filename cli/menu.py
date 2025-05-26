# Updated: CrimeWatch CLI - Menu Interface
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import print as rprint
import pyfiglet
from colorama import init, Fore, Style
from datetime import datetime
from tabulate import tabulate
from sqlalchemy import func, or_
import time

# Local imports
from models.incident import Incident, CrimeType
from models.location import Location
from models.person import Person, PersonType
from database.connection import get_db
from helpers.analyzer import (
    get_top_crimes_by_month,
    get_most_dangerous_neighborhoods,
    get_crime_trends,
    get_crime_patterns
)
from helpers.exporter import export_to_csv, export_to_json

init()  # Initialize colorama
console = Console()

def display_header():
    """Display the CrimeWatch CLI header."""
    ascii_art = pyfiglet.figlet_format("CRIMEWATCH CLI", font="slant")
    rprint(f"{Fore.BLUE}{ascii_art}{Style.RESET_ALL}")
    rprint(f"{Fore.YELLOW}🕵️  Your Local Crime Reporting System{Style.RESET_ALL}\n")

def get_main_menu():
    """Display and get user choice from main menu."""
    menu = {
        "1": "Add New Crime Report",
        "2": "List All Incidents",
        "3": "Filter Incidents",
        "4": "View Detailed Report",
        "5": "Add Victim/Witness",
        "6": "Update/Delete Report",
        "7": "Analyze Crime Data",
        "8": "Export Reports",
        "0": "Exit"
    }
    
    table = Table(title="Main Menu")
    table.add_column("Option", style="cyan")
    table.add_column("Action", style="green")
    
    for key, value in menu.items():
        table.add_row(key, value)
    
    console.print(table)
    return Prompt.ask("Select an option", choices=list(menu.keys()))

def add_incident():
    """Add a new crime incident."""
    console.print("\n[bold blue]Add New Crime Report[/bold blue]")
    
    try:
        # Get crime type
        crime_types = [t.value for t in CrimeType]
        console.print("\nAvailable crime types:")
        for i, crime_type in enumerate(crime_types, 1):
            console.print(f"{i}. {crime_type}")
        
        type_choice = int(Prompt.ask("Select crime type", choices=[str(i) for i in range(1, len(crime_types) + 1)]))
        crime_type = CrimeType(crime_types[type_choice - 1])
        
        # Get location details
        street = Prompt.ask("Street")
        neighborhood = Prompt.ask("Neighborhood")
        city = Prompt.ask("City")
        zone = Prompt.ask("Zone (optional)", default="")
        
        # Get incident details
        description = Prompt.ask("Description")
        date_str = Prompt.ask("Date (YYYY-MM-DD HH:MM)", default=datetime.now().strftime("%Y-%m-%d %H:%M"))
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        
        # Save to database
        db = next(get_db())
        try:
            location = Location(street=street, neighborhood=neighborhood, city=city, zone=zone)
            db.add(location)
            db.flush()
            
            incident = Incident(
                type=crime_type,
                date=date,
                description=description,
                location_id=location.id
            )
            db.add(incident)
            db.commit()
            
            console.print("[bold green]✓ Incident added successfully![/bold green]")
        except Exception as e:
            db.rollback()
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
        finally:
            db.close()
    except ValueError as e:
        console.print(f"[bold red]Invalid input: {str(e)}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {str(e)}[/bold red]")

def list_incidents():
    """List all incidents in a table format."""
    db = next(get_db())
    try:
        incidents = db.query(Incident).all()
        
        if not incidents:
            console.print("[yellow]No incidents found.[/yellow]")
            return
        
        table_data = []
        for incident in incidents:
            table_data.append([
                incident.id,
                incident.type.value,
                incident.date.strftime("%Y-%m-%d %H:%M"),
                incident.location.neighborhood,
                incident.description[:50] + "..." if len(incident.description) > 50 else incident.description
            ])
        
        headers = ["ID", "Type", "Date", "Location", "Description"]
        console.print(tabulate(table_data, headers=headers, tablefmt="simple"))
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
    finally:
        db.close()

def filter_incidents():
    """Filter incidents by various criteria."""
    console.print("\n[bold blue]Filter Incidents[/bold blue]")
    
    filter_options = {
        "1": "By Date Range",
        "2": "By Location",
        "3": "By Crime Type",
        "4": "By Description",
        "0": "Back to Main Menu"
    }
    
    table = Table(title="Filter Options", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Action", style="green")
    
    for key, value in filter_options.items():
        table.add_row(key, value)
    
    console.print(table)
    choice = Prompt.ask("Select filter option", choices=list(filter_options.keys()))
    
    if choice == "0":
        return
    
    db = next(get_db())
    try:
        query = db.query(Incident)
        
        if choice == "1":  # Date Range
            start_date = Prompt.ask("Start date (YYYY-MM-DD)")
            end_date = Prompt.ask("End date (YYYY-MM-DD)")
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Incident.date.between(start, end))
            
        elif choice == "2":  # Location
            location_type = Prompt.ask("Search by (1) Street, (2) Neighborhood, or (3) City", choices=["1", "2", "3"])
            search_term = Prompt.ask("Enter search term")
            
            if location_type == "1":
                query = query.join(Location).filter(Location.street.ilike(f"%{search_term}%"))
            elif location_type == "2":
                query = query.join(Location).filter(Location.neighborhood.ilike(f"%{search_term}%"))
            else:
                query = query.join(Location).filter(Location.city.ilike(f"%{search_term}%"))
                
        elif choice == "3":  # Crime Type
            crime_types = [t.value for t in CrimeType]
            console.print("\nAvailable crime types:")
            for i, crime_type in enumerate(crime_types, 1):
                console.print(f"{i}. {crime_type}")
            type_choice = int(Prompt.ask("Select crime type", choices=[str(i) for i in range(1, len(crime_types) + 1)]))
            crime_type = CrimeType(crime_types[type_choice - 1])
            query = query.filter(Incident.type == crime_type)
            
        elif choice == "4":  # Description
            search_term = Prompt.ask("Enter search term")
            query = query.filter(Incident.description.ilike(f"%{search_term}%"))
        
        incidents = query.all()
        
        if not incidents:
            console.print("[yellow]No incidents found matching your criteria.[/yellow]")
            return
        
        table_data = []
        for incident in incidents:
            table_data.append([
                incident.id,
                incident.type.value,
                incident.date.strftime("%Y-%m-%d %H:%M"),
                incident.location.neighborhood,
                incident.description[:50] + "..." if len(incident.description) > 50 else incident.description
            ])
        
        headers = ["ID", "Type", "Date", "Location", "Description"]
        console.print(tabulate(table_data, headers=headers, tablefmt="simple"))
        
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
    finally:
        db.close()

def view_detailed_report():
    """View detailed information about a specific incident."""
    incident_id = Prompt.ask("Enter incident ID")
    
    db = next(get_db())
    try:
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        
        if not incident:
            console.print("[yellow]Incident not found.[/yellow]")
            return
        
        # Create detailed report table
        table = Table(title=f"Incident Report #{incident.id}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Type", incident.type.value)
        table.add_row("Date", incident.date.strftime("%Y-%m-%d %H:%M"))
        table.add_row("Description", incident.description)
        table.add_row("Location", f"{incident.location.street}, {incident.location.neighborhood}")
        table.add_row("City", incident.location.city)
        if incident.location.zone:
            table.add_row("Zone", incident.location.zone)
        
        # Add victims and witnesses
        victims = [p.name for p in incident.persons if p.type.value == 'victim']
        witnesses = [p.name for p in incident.persons if p.type.value == 'witness']
        
        table.add_row("Victims", "\n".join(victims) if victims else "None")
        table.add_row("Witnesses", "\n".join(witnesses) if witnesses else "None")
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
    finally:
        db.close()

def add_person():
    """Add a victim or witness to an incident."""
    incident_id = Prompt.ask("Enter incident ID")
    
    db = next(get_db())
    try:
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        
        if not incident:
            console.print("[yellow]Incident not found.[/yellow]")
            return
        
        # Get person type
        person_types = [t.value for t in PersonType]
        console.print("\nPerson type:")
        for i, person_type in enumerate(person_types, 1):
            console.print(f"{i}. {person_type}")
        
        type_choice = int(Prompt.ask("Select person type", choices=[str(i) for i in range(1, len(person_types) + 1)]))
        person_type = PersonType(person_types[type_choice - 1])
        
        # Get person details
        name = Prompt.ask("Name")
        contact = Prompt.ask("Contact information (optional)", default="")
        
        # Save to database
        try:
            person = Person(
                name=name,
                contact=contact,
                type=person_type,
                incident_id=incident_id
            )
            db.add(person)
            db.commit()
            
            console.print("[bold green]✓ Person added successfully![/bold green]")
        except Exception as e:
            db.rollback()
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
            
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
    finally:
        db.close()

def update_delete_report():
    """Update or delete an incident report."""
    incident_id = Prompt.ask("Enter incident ID")
    
    db = next(get_db())
    try:
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        
        if not incident:
            console.print("[yellow]Incident not found.[/yellow]")
            return
        
        action = Prompt.ask("Choose action: (1) Update, (2) Delete", choices=["1", "2"])
        
        if action == "1":
            # Update incident
            console.print("\nLeave blank to keep current values:")
            
            # Get crime type
            crime_types = [t.value for t in CrimeType]
            console.print("\nAvailable crime types:")
            for i, crime_type in enumerate(crime_types, 1):
                console.print(f"{i}. {crime_type}")
            
            type_choice = Prompt.ask("Select new crime type (or press Enter to keep current)", default="")
            if type_choice:
                incident.type = CrimeType(crime_types[int(type_choice) - 1])
            
            # Get new description
            new_description = Prompt.ask("New description", default=incident.description)
            incident.description = new_description
            
            # Get new date
            new_date = Prompt.ask("New date (YYYY-MM-DD HH:MM)", default=incident.date.strftime("%Y-%m-%d %H:%M"))
            incident.date = datetime.strptime(new_date, "%Y-%m-%d %H:%M")
            
            try:
                db.commit()
                console.print("[bold green]✓ Incident updated successfully![/bold green]")
            except Exception as e:
                db.rollback()
                console.print(f"[bold red]Error: {str(e)}[/bold red]")
                
        else:
            # Delete incident
            confirm = Prompt.ask("Are you sure you want to delete this incident? (y/n)", choices=["y", "n"])
            if confirm == "y":
                try:
                    db.delete(incident)
                    db.commit()
                    console.print("[bold green]✓ Incident deleted successfully![/bold green]")
                except Exception as e:
                    db.rollback()
                    console.print(f"[bold red]Error: {str(e)}[/bold red]")
            
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
    finally:
        db.close()

def analyze_crime_data():
    """Display various crime analysis reports."""
    analysis_options = {
        "1": "Top 3 Crime Types This Month",
        "2": "Most Dangerous Neighborhoods",
        "3": "Crime Trends Over Time",
        "4": "Crime Patterns",
        "0": "Back to Main Menu"
    }
    
    table = Table(title="Analysis Options")
    table.add_column("Option", style="cyan")
    table.add_column("Action", style="green")
    
    for key, value in analysis_options.items():
        table.add_row(key, value)
    
    console.print(table)
    choice = Prompt.ask("Select analysis option", choices=list(analysis_options.keys()))
    
    if choice == "0":
        return
    
    try:
        if choice == "1":
            results = get_top_crimes_by_month()
            if not results:
                console.print("[yellow]No data available for analysis.[/yellow]")
                return
            
            table = Table(title="Top 3 Crime Types This Month")
            table.add_column("Crime Type", style="cyan")
            table.add_column("Count", style="green")
            
            for crime_type, count in results:
                table.add_row(crime_type, str(count))
            
            console.print(table)
            
        elif choice == "2":
            results = get_most_dangerous_neighborhoods()
            if not results:
                console.print("[yellow]No data available for analysis.[/yellow]")
                return
            
            table = Table(title="Most Dangerous Neighborhoods")
            table.add_column("Neighborhood", style="cyan")
            table.add_column("Incident Count", style="green")
            
            for neighborhood, count in results:
                table.add_row(neighborhood, str(count))
            
            console.print(table)
            
        elif choice == "3":
            results = get_crime_trends()
            if not results:
                console.print("[yellow]No data available for analysis.[/yellow]")
                return
            
            table = Table(title="Crime Trends Over Time")
            table.add_column("Month", style="cyan")
            table.add_column("Incident Count", style="green")
            
            for month, count in results:
                table.add_row(month, str(count))
            
            console.print(table)
            
        elif choice == "4":
            results = get_crime_patterns()
            if not results:
                console.print("[yellow]No patterns found.[/yellow]")
                return
            
            table = Table(title="Crime Patterns")
            table.add_column("Street", style="cyan")
            table.add_column("Incident Count", style="green")
            
            for street, count in results:
                table.add_row(street, str(count))
            
            console.print(table)
            
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")

def export_reports():
    """Export incident reports to CSV or JSON format."""
    export_options = {
        "1": "Export to CSV",
        "2": "Export to JSON",
        "0": "Back to Main Menu"
    }
    
    table = Table(title="Export Options")
    table.add_column("Option", style="cyan")
    table.add_column("Action", style="green")
    
    for key, value in export_options.items():
        table.add_row(key, value)
    
    console.print(table)
    choice = Prompt.ask("Select export option", choices=list(export_options.keys()))
    
    if choice == "0":
        return
    
    try:
        if choice == "1":
            filename = Prompt.ask("Enter filename", default="crime_report.csv")
            if export_to_csv(filename):
                console.print(f"[bold green]✓ Data exported to {filename} successfully![/bold green]")
            else:
                console.print("[bold red]Error exporting data.[/bold red]")
                
        elif choice == "2":
            filename = Prompt.ask("Enter filename", default="crime_report.json")
            if export_to_json(filename):
                console.print(f"[bold green]✓ Data exported to {filename} successfully![/bold green]")
            else:
                console.print("[bold red]Error exporting data.[/bold red]")
                
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")

def main():
    """Main program loop."""
    display_header()
    
    while True:
        choice = get_main_menu()
        
        if choice == "0":
            console.print("[bold red]Goodbye![/bold red]")
            break
        elif choice == "1":
            add_incident()
        elif choice == "2":
            list_incidents()
        elif choice == "3":
            filter_incidents()
        elif choice == "4":
            view_detailed_report()
        elif choice == "5":
            add_person()
        elif choice == "6":
            update_delete_report()
        elif choice == "7":
            analyze_crime_data()
        elif choice == "8":
            export_reports()
        
        Prompt.ask("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 