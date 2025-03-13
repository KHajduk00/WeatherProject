import sqlite3
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = None
    try:
        conn = sqlite3.connect('weather_data.db')
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()