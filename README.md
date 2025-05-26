# CrimeWatch CLI

A command-line interface application for reporting and tracking local crime incidents. Built with Python, SQLAlchemy ORM, and Rich CLI framework.

## Features

- 📝 Report new crime incidents with detailed information
- 👥 Track victims and witnesses
- 📍 Location-based incident tracking
- 🔍 Search and filter incidents
- 📊 View incident statistics
- 🎨 Rich, colorful CLI interface
- 💾 SQLite database with SQLAlchemy ORM
- 🔒 Data validation and error handling

## Project Structure

```
crimewatch-cli/
├── cli/                    # CLI interface components
│   ├── menu.py            # Main menu and navigation
│   └── display.py         # Display formatting utilities
├── models/                 # Database models
│   └── incident.py        # Incident, Location, and Person models
├── database/              # Database configuration
│   └── connection.py      # Database connection and setup
├── helpers/               # Utility functions
│   └── validators.py      # Input validation utilities
├── main.py               # Application entry point
├── setup.py              # Package setup configuration
├── Pipfile              # Pipenv dependencies
└── README.md            # Project documentation
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Brian454-nexus/crimewatch-cli.git
cd crimewatch-cli
```

2. Install dependencies using Pipenv:

```bash
pipenv install
```

3. Activate the virtual environment:

```bash
pipenv shell
```

## Usage

1. Start the application:

```bash
python main.py
```

2. Follow the interactive menu to:
   - Report new incidents
   - View incident reports
   - Search and filter incidents
   - View statistics
   - Exit the application

## Features in Detail

### Incident Reporting

- Report various types of crimes (theft, assault, vandalism, etc.)
- Add detailed location information
- Record victim and witness details
- Add incident descriptions and timestamps

### Search and Filter

- Search by incident type
- Filter by date range
- Search by location
- View detailed incident reports

### Statistics

- View incident counts by type
- Track incidents by location
- Monitor incident trends

## Database Schema

The application uses SQLAlchemy ORM with the following models:

### Incident

- ID (Primary Key)
- Type (Enum: theft, assault, vandalism, etc.)
- Date
- Description
- Location (Foreign Key)

### Location

- ID (Primary Key)
- Street/Address
- Area/Neighborhood
- Incidents (Relationship)

### Person

- ID (Primary Key)
- Name
- Type (Enum: victim, witness)
- Contact
- Incident (Foreign Key)

## Development

### Prerequisites

- Python 3.8+
- Pipenv
- SQLite3

### Dependencies

- SQLAlchemy
- Rich
- Tabulate
- Click

### Running Tests

```bash
pipenv run pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Brian Terer

## Acknowledgments

- Rich library for beautiful CLI interfaces
- SQLAlchemy for ORM functionality
- Python community for excellent documentation and support
