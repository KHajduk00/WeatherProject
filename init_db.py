import sqlite3
import logging
from cities import CITIES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize the SQLite database with schema and initial city data"""
    try:
        # Connect to SQLite (this will create the database if it doesn't exist)
        conn = sqlite3.connect('weather_data.db')
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

        # Insert initial cities data
        for city in CITIES:
            cursor.execute('''
            INSERT OR IGNORE INTO cities (name, country, latitude, longitude)
            VALUES (?, ?, ?, ?)
            ''', (city['name'], city['country'], city['lat'], city['lon']))

        # Commit the changes
        conn.commit()
        logger.info("Database initialized successfully!")

    except sqlite3.Error as e:
        logger.error(f"An error occurred while initializing the database: {e}")
        raise

    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    init_database()