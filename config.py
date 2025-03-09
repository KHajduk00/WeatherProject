import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CURRENT_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
AIR_POLLUTION_API_URL = "https://api.openweathermap.org/data/2.5/air_pollution"

# Output configuration
OUTPUT_CSV_PATH = "cities_weather_data.csv"

# Units
TEMP_UNIT = "metric"  # Use Celsius for temperature

# Collection interval (in seconds)
# 3600 = 1 hour, 1800 = 30 minutes, etc.
COLLECTION_INTERVAL = 3600

# Request settings
REQUEST_TIMEOUT = 10  # seconds