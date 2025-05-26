# Updated: CrimeWatch CLI - Main Application Entry Point
from database.connection import engine, Base
from cli.menu import main_menu

def init_db():
    """Initialize the database with all tables."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    main_menu() 