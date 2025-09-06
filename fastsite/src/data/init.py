"""Initialise SQLite database"""

import os
from pathlib import Path
from sqlite3 import connect, Connection, Cursor, IntegrityError

# NOTE: These are global variables, acting as a singleton for the database connection.
# This ensures the entire application shares one connection.
conn: Connection | None = None
curs: Cursor | None = None

def get_db(name: str | None = None, reset: bool = False) -> None:
    """Connect to SQLite database file"""
    global conn, curs
    
    if conn:
        # NOTE: The 'reset' flag is a crucial feature for testing.
        # It allows test fixtures to tear down and recreate the database schema.
        if not reset:
            return None
        conn = None
    
    if not name:
        # NOTE: Prioritising an environment variable for the DB path is a best practice.
        # It allows us to switch to an in-memory db for tests (":memory:").
        name = os.getenv("CRYPTID_SQLITE_DB")
        
        # FIX: The path is calculated from this file's location, going up two directories
        # to the project root. This is more robust than using relative paths.
        top_dir = Path(__file__).resolve().parents[2]
        db_dir = top_dir / "db"

        # NOTE: This ensures the database directory exists before we try to connect.
        # sqlite3.connect() can create a file, but not a directory.
        db_dir.mkdir(parents=True, exist_ok=True)
        
        db_name = "cryptid.db"
        db_path = str(db_dir / db_name)
        name = os.getenv("CRYPTID_SQLITE_DB", db_path)
    
    # NOTE: 'check_same_thread=False' is required for using SQLite with FastAPI/uvicorn.
    conn = connect(name, check_same_thread=False)
    curs = conn.cursor()

get_db()
