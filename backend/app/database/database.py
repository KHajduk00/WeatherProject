import sqlite3
from contextlib import contextmanager
import logging
from pathlib import Path
from app.core.config import BASE_DIR, DATABASE_URL

logger = logging.getLogger(__name__)

# Get the database path from DATABASE_URL
DB_PATH = Path(DATABASE_URL.replace("sqlite:///", ""))
if not DB_PATH.is_absolute():
    DB_PATH = BASE_DIR / DB_PATH.relative_to(".")

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = None
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()