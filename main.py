from database.connection import engine, Base
from cli.menu import main

def init_db():
    """Initialize the database with all tables."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    main() 