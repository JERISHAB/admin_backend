import os
import subprocess
import logging
import uvicorn

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_migrations():
    """
    Run the Alembic migrations before starting the server.
    """
    logging.info("Running database migrations...")
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        logging.info("Migrations applied successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error applying migrations: {e}")
        exit(1)

if __name__ == "__main__":
    #run_migrations()

    port = int(os.getenv("PORT", 8000))  # Default to 8000 if PORT is not set
    host = os.getenv("HOST","127.0.0.1")  # Default to 0.0.0.0 for external access

    logging.info(f"Starting FastAPI server at {host}:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
