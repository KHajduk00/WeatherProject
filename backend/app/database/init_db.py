import sqlite3
import logging
from pathlib import Path
from app.core.config import BASE_DIR, DATABASE_URL
from app.core.cities import CITIES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the database path from DATABASE_URL
DB_PATH = Path(DATABASE_URL.replace("sqlite:///", ""))
if not DB_PATH.is_absolute():
    DB_PATH = BASE_DIR / DB_PATH.relative_to(".")

# Ensure the database directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_database():
    """Initialize the SQLite database with schema and initial city data"""
    try:
        # Connect to SQLite (this will create the database if it doesn't exist)
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # Create cities table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            city_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            country VARCHAR(100) NOT NULL,
            latitude DECIMAL(10,6) NOT NULL,
            longitude DECIMAL(10,6) NOT NULL,
            UNIQUE(name, country)
        )
        ''')

        # Create weather measurements table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_measurements (
            weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            measurement_timestamp DATETIME NOT NULL,
            collection_timestamp DATETIME NOT NULL,
            temperature DECIMAL(5,2),
            feels_like DECIMAL(5,2),
            temp_min DECIMAL(5,2),
            temp_max DECIMAL(5,2),
            pressure INTEGER,
            humidity INTEGER,
            sea_level INTEGER,
            ground_level INTEGER,
            visibility INTEGER,
            wind_speed DECIMAL(5,2),
            wind_degree INTEGER,
            wind_gust DECIMAL(5,2),
            clouds_all INTEGER,
            rain_1h DECIMAL(5,2),
            rain_3h DECIMAL(5,2),
            snow_1h DECIMAL(5,2),
            snow_3h DECIMAL(5,2),
            weather_condition_id INTEGER,
            weather_main VARCHAR(50),
            weather_description VARCHAR(100),
            weather_icon VARCHAR(10),
            sunrise TIME,
            sunset TIME,
            FOREIGN KEY (city_id) REFERENCES cities(city_id)
        )
        ''')

        # Create air pollution measurements table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS air_pollution_measurements (
            air_pollution_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            measurement_timestamp DATETIME NOT NULL,
            collection_timestamp DATETIME NOT NULL,
            aqi INTEGER,
            co DECIMAL(10,2),
            no DECIMAL(10,2),
            no2 DECIMAL(10,2),
            o3 DECIMAL(10,2),
            so2 DECIMAL(10,2),
            pm2_5 DECIMAL(10,2),
            pm10 DECIMAL(10,2),
            nh3 DECIMAL(10,2),
            FOREIGN KEY (city_id) REFERENCES cities(city_id)
        )
        ''')

        # Create indexes for better query performance
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_weather_city_date 
        ON weather_measurements(city_id, measurement_timestamp)
        ''')

        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_pollution_city_date 
        ON air_pollution_measurements(city_id, measurement_timestamp)
        ''')

        # Insert initial cities data
        for city in CITIES:
            cursor.execute('''
            INSERT OR IGNORE INTO cities (name, country, latitude, longitude)
            VALUES (?, ?, ?, ?)
            ''', (city['name'], city['country'], city['lat'], city['lon']))

        # Commit the changes
        conn.commit()
        logger.info(f"Database initialized successfully at {DB_PATH}!")
        
        # Log the number of cities inserted
        cursor.execute("SELECT COUNT(*) FROM cities")
        city_count = cursor.fetchone()[0]
        logger.info(f"Number of cities in database: {city_count}")

    except sqlite3.Error as e:
        logger.error(f"An error occurred while initializing the database: {e}")
        raise

    finally:
        # Close the connection
        if conn:
            conn.close()

def verify_database():
    """Verify that the database was initialized correctly"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        logger.info("Created tables: " + ", ".join([table[0] for table in tables]))

        # Check cities were inserted
        cursor.execute("SELECT COUNT(*) FROM cities")
        city_count = cursor.fetchone()[0]
        logger.info(f"Verified {city_count} cities in database")

        return True

    except sqlite3.Error as e:
        logger.error(f"Database verification failed: {e}")
        return False

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_database()
    verify_database()