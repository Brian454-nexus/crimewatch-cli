# 🕵️ CrimeWatch CLI

A command-line tool for tracking and analyzing local crime reports. Built with Python, SQLAlchemy, and a beautiful CLI interface.

## Features

- Add and manage crime reports
- Track victims and witnesses
- Filter and search incidents
- Generate crime analysis reports
- Export data to CSV/JSON
- Beautiful CLI interface with colors and tables

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/crimewatch-cli.git
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

Run the application:

```bash
python main.py
```

### Main Menu Options

1. Add New Crime Report
2. List All Incidents
3. Filter Incidents
4. View Detailed Report
5. Add Victim/Witness
6. Update/Delete Report
7. Analyze Crime Data
8. Export Reports
9. Exit

## Project Structure

```
crimewatch-cli/
│
├── main.py                 # Entry point
├── Pipfile / Pipfile.lock  # Environment files
├── cli/
│   └── menu.py            # Main CLI interface logic
│
├── models/
│   └── incident.py        # Incident model
│   └── person.py          # Victim/Witness model
│   └── location.py        # Crime location model
│
└── database/
    └── connection.py      # SQLAlchemy setup
```

## Dependencies

- SQLAlchemy: Database ORM
- Tabulate: Pretty table formatting
- Colorama: Terminal colors
- Rich: Enhanced terminal output
- PyFiglet: ASCII art headers

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
