import os
import psycopg2
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Database connection URL (Set in environment variables)
DATABASE_URL = os.getenv("DATABASE_URL")

# Migration folders
SQL_FOLDER = "migrations/sql"
PYTHON_FOLDER = "migrations/pys"

def get_applied_migrations(cursor):
    """Fetch the list of applied migrations from the database."""
    cursor.execute("SELECT migration_name FROM migrations")
    return {row[0] for row in cursor.fetchall()}

def apply_sql_migration(cursor, file_name, file_path):
    """Apply a SQL migration."""
    logging.info(f"Applying SQL migration: {file_name}")
    try:
        with open(file_path, "r") as file:
            sql = file.read()
            cursor.execute(sql)
        cursor.execute("INSERT INTO migrations (migration_name) VALUES (%s)", (file_name,))
    except Exception as e:
        logging.error(f"Error applying SQL migration {file_name}: {e}")
        exit(1)

def apply_python_migration(cursor, file_name, module_name):
    """Apply a Python migration by running its 'run' function."""
    logging.info(f"Applying Python migration: {file_name}")
    try:
        migration_module = __import__(module_name, fromlist=["run"])
        migration_module.run(cursor)
        cursor.execute("INSERT INTO migrations (migration_name) VALUES (%s)", (file_name,))
    except Exception as e:
        logging.error(f"Error applying Python migration {file_name}: {e}")
        exit(1)

def ensure_migrations_table(cursor):
    """Ensure that the migrations tracking table exists."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id SERIAL PRIMARY KEY,
            migration_name TEXT NOT NULL UNIQUE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

def run_migrations():
    """Run all unapplied migrations in the correct order."""
    logging.info("Starting database migrations...")

    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()

    # Ensure the migrations table exists
    ensure_migrations_table(cursor)

    # Get already applied migrations
    applied_migrations = get_applied_migrations(cursor)

    # Apply SQL migrations (excluding 'latest.sql')
    sql_files = sorted(Path(SQL_FOLDER).glob("*.sql"))
    for file in sql_files:
        if file.name == "latest.sql":
            continue
        if file.name not in applied_migrations:
            apply_sql_migration(cursor, file.name, file)

    # Apply SQL migrations from 'alter' subdirectory
    alter_sql_files = sorted(Path(SQL_FOLDER, "alter").glob("*.sql"))
    for file in alter_sql_files:
        if file.name not in applied_migrations:
            apply_sql_migration(cursor, file.name, file)

    # Apply Python migrations
    python_files = sorted(Path(PYTHON_FOLDER).glob("*.py"))
    for file in python_files:
        if file.name not in applied_migrations:
            module_name = f"migrations.pys.{file.stem}"
            apply_python_migration(cursor, file.name, module_name)

    # Apply Python migrations from 'alter' subdirectory
    alter_python_files = sorted(Path(PYTHON_FOLDER, "alter").glob("*.py"))
    for file in alter_python_files:
        if file.name not in applied_migrations:
            module_name = f"migrations.pys.{file.stem}"
            apply_python_migration(cursor, file.name, module_name)

    cursor.close()
    conn.close()
    print("All migrations applied successfully.")
if __name__ == "__main__":
    run_migrations()
