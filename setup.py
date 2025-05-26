from setuptools import setup, find_packages

setup(
    name="crimewatch-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy",
        "tabulate",
        "colorama",
        "rich",
        "pyfiglet",
        "python-dateutil",
    ],
    python_requires=">=3.9",
) 