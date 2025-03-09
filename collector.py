import os
import time
import requests
import pandas as pd
import logging
from datetime import datetime
import signal
import sys

# Import configuration and cities
from config import (
    API_KEY, 
    CURRENT_WEATHER_API_URL, 
    AIR_POLLUTION_API_URL, 
    TEMP_UNIT, 
    REQUEST_TIMEOUT,
    OUTPUT_CSV_PATH,
    COLLECTION_INTERVAL
)
from cities import CITIES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("weather_collector.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global flag to control the main loop
running = True

def signal_handler(sig, frame):
    """Handle Ctrl+C to gracefully exit the program"""
    global running
    logger.info("Stopping data collection. Please wait for the current cycle to complete...")
    running = False

def get_current_weather(lat, lon):
    """Fetch current weather data for given coordinates"""
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': TEMP_UNIT,
    }
    
    try:
        response = requests.get(
            CURRENT_WEATHER_API_URL,
            params=params,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching current weather for coordinates ({lat}, {lon}): {e}")
        return None

def get_air_pollution_data(lat, lon):
    """Fetch current air pollution data for given coordinates"""
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
    }
    
    try:
        response = requests.get(
            AIR_POLLUTION_API_URL,
            params=params,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching air pollution data for coordinates ({lat}, {lon}): {e}")
        return None

def extract_current_weather(weather_data, city_info):
    """Extract relevant fields from current weather API response"""
    if not weather_data:
        return {}
    
    # Extract main weather condition
    weather = weather_data.get('weather', [{}])[0] if weather_data.get('weather') else {}
    
    return {
        'city': city_info['name'],
        'country': city_info['country'],
        'latitude': city_info['lat'],
        'longitude': city_info['lon'],
        'measurement_timestamp': datetime.fromtimestamp(weather_data.get('dt', 0)).strftime('%Y-%m-%d %H:%M:%S') if weather_data.get('dt') else None,
        'temp': weather_data.get('main', {}).get('temp'),
        'feels_like': weather_data.get('main', {}).get('feels_like'),
        'temp_min': weather_data.get('main', {}).get('temp_min'),
        'temp_max': weather_data.get('main', {}).get('temp_max'),
        'pressure': weather_data.get('main', {}).get('pressure'),
        'humidity': weather_data.get('main', {}).get('humidity'),
        'sea_level': weather_data.get('main', {}).get('sea_level'),
        'grnd_level': weather_data.get('main', {}).get('grnd_level'),
        'visibility': weather_data.get('visibility'),
        'wind_speed': weather_data.get('wind', {}).get('speed'),
        'wind_deg': weather_data.get('wind', {}).get('deg'),
        'wind_gust': weather_data.get('wind', {}).get('gust'),
        'clouds_all': weather_data.get('clouds', {}).get('all'),
        'rain_1h': weather_data.get('rain', {}).get('1h'),
        'rain_3h': weather_data.get('rain', {}).get('3h'),
        'snow_1h': weather_data.get('snow', {}).get('1h'),
        'snow_3h': weather_data.get('snow', {}).get('3h'),
        'weather_id': weather.get('id'),
        'weather_main': weather.get('main'),
        'weather_description': weather.get('description'),
        'weather_icon': weather.get('icon'),
        'sunrise': datetime.fromtimestamp(weather_data.get('sys', {}).get('sunrise', 0)).strftime('%H:%M:%S') if weather_data.get('sys', {}).get('sunrise') else None,
        'sunset': datetime.fromtimestamp(weather_data.get('sys', {}).get('sunset', 0)).strftime('%H:%M:%S') if weather_data.get('sys', {}).get('sunset') else None,
    }

def extract_air_pollution_data(air_data):
    """Extract relevant fields from air pollution API response"""
    if not air_data or 'list' not in air_data or not air_data['list']:
        return {}
    
    components = air_data['list'][0].get('components', {})
    return {
        'aqi': air_data['list'][0].get('main', {}).get('aqi'),
        'co': components.get('co'),
        'no': components.get('no'),
        'no2': components.get('no2'),
        'o3': components.get('o3'),
        'so2': components.get('so2'),
        'pm2_5': components.get('pm2_5'),
        'pm10': components.get('pm10'),
        'nh3': components.get('nh3'),
    }

def save_data(city_info, current_weather, air_data):
    """Process and save weather and air pollution data to CSV"""
    collection_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Extract data
    weather_dict = extract_current_weather(current_weather, city_info)
    air_dict = extract_air_pollution_data(air_data)
    
    # Combine all data
    combined_data = {
        'collection_timestamp': collection_timestamp,
        **weather_dict,
        **air_dict
    }
    
    # Create DataFrame from the combined data
    df_new = pd.DataFrame([combined_data])
    
    # Check if the output file exists
    if os.path.exists(OUTPUT_CSV_PATH):
        try:
            # Load existing CSV and append new data
            df_existing = pd.read_csv(OUTPUT_CSV_PATH)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(OUTPUT_CSV_PATH, index=False)
            logger.info(f"Data for {city_info['name']} appended to {OUTPUT_CSV_PATH}")
        except Exception as e:
            logger.error(f"Error appending to CSV: {e}")
            # Save just the new data if there's an error with the existing file
            df_new.to_csv(OUTPUT_CSV_PATH, index=False)
    else:
        # Create new CSV file
        df_new.to_csv(OUTPUT_CSV_PATH, index=False)
        logger.info(f"Created new CSV file {OUTPUT_CSV_PATH} with data for {city_info['name']}")

def collect_data_for_city(city_info):
    """Collect weather and air pollution data for a single city"""
    lat, lon = city_info['lat'], city_info['lon']
    
    logger.info(f"Collecting data for {city_info['name']}, {city_info['country']}...")
    
    # Get current weather data
    current_weather = get_current_weather(lat, lon)
    
    # Get air pollution data
    air_data = get_air_pollution_data(lat, lon)
    
    # Save data to CSV
    save_data(city_info, current_weather, air_data)

def collect_data_for_all_cities():
    """Collect data for all cities"""
    logger.info(f"Starting data collection at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    for city_info in CITIES:
        try:
            collect_data_for_city(city_info)
            # Add a small delay between API calls to avoid rate limiting
            time.sleep(1)
        except Exception as e:
            logger.error(f"Error collecting data for {city_info['name']}: {e}")
    
    logger.info(f"Data collection completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main function to run the data collection"""
    global running
    
    # Set up the signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    if not API_KEY:
        logger.error("OpenWeather API key is not set. Please set the OPENWEATHER_API_KEY environment variable.")
        return 1
    
    logger.info("Weather and Air Pollution Data Collector starting...")
    logger.info(f"Collection interval set to {COLLECTION_INTERVAL} seconds")
    
    try:
        # Collect data immediately when starting
        collect_data_for_all_cities()
        
        # Record the last collection time
        last_collection = time.time()
        
        # Main loop for periodic collection
        while running:
            # Calculate time to sleep until next collection
            current_time = time.time()
            elapsed = current_time - last_collection
            
            if elapsed >= COLLECTION_INTERVAL:
                # Time to collect data again
                collect_data_for_all_cities()
                last_collection = time.time()
            else:
                # Sleep for a bit before checking again
                # Check every 10 seconds if we should stop or continue
                time.sleep(min(10, COLLECTION_INTERVAL - elapsed))
    
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return 1
    
    logger.info("Weather data collection stopped")
    return 0

if __name__ == "__main__":
    sys.exit(main())