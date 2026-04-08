# Task 1 — Data Ingestion

Script that ingests book data from a JSON file into a PostgreSQL database and produces a summary table.

## Summary table fields
- `publication_year` — year the books were published
- `book_count` — number of books published that year
- `average_price` — average price in USD (€1 = $1.2), rounded to cents

## Requirements

- Python 3.x
- PostgreSQL

Install dependencies:
pip install psycopg2-binary python-dotenv

## Setup

1. Create a PostgreSQL database
2. Create a `.env` file in the project folder:

DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

## Run

python solution.py