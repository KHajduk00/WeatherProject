import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# Get the base directory of your backend
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

# API configuration
API_KEY: Optional[str] = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY must be set in .env file")

# API endpoints
CURRENT_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
AIR_POLLUTION_API_URL = "https://api.openweathermap.org/data/2.5/air_pollution"

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/data/weather_data.db")

# Output configuration
OUTPUT_CSV_PATH = BASE_DIR / "data" / "cities_weather_data.csv"

# Units
TEMP_UNIT = "Celsius"  # Use Celsius for temperature

# Collection interval (in seconds)
# 3600 = 1 hour, 1800 = 30 minutes, etc.
COLLECTION_INTERVAL = int(os.getenv("COLLECTION_INTERVAL", "3600"))

# Request settings
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))  # seconds

# Additional configurations that could be useful
DEBUG = os.getenv("DEBUG", "False").lower() == "true"