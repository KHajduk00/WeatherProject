import time
import requests
import logging
from datetime import datetime
import sqlite3
from typing import Dict, Optional, Any

from app.core.config import (
    API_KEY,
    CURRENT_WEATHER_API_URL,
    AIR_POLLUTION_API_URL,
    REQUEST_TIMEOUT,
    COLLECTION_INTERVAL
)
from app.core.cities import CITIES
from app.database.database import get_db

# Configure logging
logger = logging.getLogger(__name__)

def get_current_weather(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """Fetch current weather data for given coordinates"""
    if not API_KEY:
        logger.error("OpenWeather API key is not set")
        return None
        
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric',  # Always use metric units
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

def get_air_pollution_data(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """Fetch current air pollution data for given coordinates"""
    if not API_KEY:
        logger.error("OpenWeather API key is not set")
        return None
        
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

def extract_current_weather(weather_data: Dict[str, Any], city_info: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from current weather API response"""
    if not weather_data:
        return {}
    
    # Extract main weather condition
    weather = weather_data.get('weather', [{}])[0] if weather_data.get('weather') else {}
    
    try:
        return {
            'city': city_info['name'],
            'country': city_info['country'],
            'latitude': city_info['lat'],
            'longitude': city_info['lon'],
            'measurement_timestamp': datetime.fromtimestamp(weather_data.get('dt', 0)).isoformat(),
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
    except Exception as e:
        logger.error(f"Error extracting weather data: {e}")
        return {}

def extract_air_pollution_data(air_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from air pollution API response"""
    if not air_data or 'list' not in air_data or not air_data['list']:
        return {}
    
    try:
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
    except Exception as e:
        logger.error(f"Error extracting air pollution data: {e}")
        return {}

def save_data(city_info: Dict[str, Any], current_weather: Dict[str, Any], air_data: Dict[str, Any]) -> None:
    """Save weather and air pollution data to database"""
    collection_timestamp = datetime.now().isoformat()
    
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Get city_id
            cursor.execute(
                "SELECT city_id FROM cities WHERE name = ? AND country = ?",
                (city_info['name'], city_info['country'])
            )
            result = cursor.fetchone()
            
            if not result:
                logger.error(f"City not found in database: {city_info['name']}, {city_info['country']}")
                return
                
            city_id = result[0]
            
            # Extract and save weather data
            weather_dict = extract_current_weather(current_weather, city_info)
            if weather_dict:
                try:
                    cursor.execute("""
                        INSERT INTO weather_measurements (
                            city_id, measurement_timestamp, collection_timestamp,
                            temperature, feels_like, temp_min, temp_max, pressure,
                            humidity, sea_level, ground_level, visibility, wind_speed,
                            wind_degree, wind_gust, clouds_all, rain_1h, rain_3h,
                            snow_1h, snow_3h, weather_condition_id, weather_main,
                            weather_description, weather_icon, sunrise, sunset
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        city_id, weather_dict['measurement_timestamp'], collection_timestamp,
                        weather_dict['temp'], weather_dict['feels_like'], weather_dict['temp_min'],
                        weather_dict['temp_max'], weather_dict['pressure'], weather_dict['humidity'],
                        weather_dict['sea_level'], weather_dict['grnd_level'], weather_dict['visibility'],
                        weather_dict['wind_speed'], weather_dict['wind_deg'], weather_dict['wind_gust'],
                        weather_dict['clouds_all'], weather_dict['rain_1h'], weather_dict['rain_3h'],
                        weather_dict['snow_1h'], weather_dict['snow_3h'], weather_dict['weather_id'],
                        weather_dict['weather_main'], weather_dict['weather_description'],
                        weather_dict['weather_icon'], weather_dict['sunrise'], weather_dict['sunset']
                    ))
                except sqlite3.Error as e:
                    logger.error(f"Error saving weather data: {e}")
            
            # Extract and save air pollution data
            air_dict = extract_air_pollution_data(air_data)
            if air_dict:
                try:
                    cursor.execute("""
                        INSERT INTO air_pollution_measurements (
                            city_id, measurement_timestamp, collection_timestamp,
                            aqi, co, no, no2, o3, so2, pm2_5, pm10, nh3
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        city_id, weather_dict['measurement_timestamp'], collection_timestamp,
                        air_dict['aqi'], air_dict['co'], air_dict['no'], air_dict['no2'],
                        air_dict['o3'], air_dict['so2'], air_dict['pm2_5'], air_dict['pm10'],
                        air_dict['nh3']
                    ))
                except sqlite3.Error as e:
                    logger.error(f"Error saving air pollution data: {e}")
            
            conn.commit()
            logger.info(f"Data for {city_info['name']} saved to database")
            
    except Exception as e:
        logger.error(f"Error in save_data for {city_info['name']}: {e}")

def collect_data_for_city(city_info: Dict[str, Any]) -> None:
    """Collect weather and air pollution data for a single city"""
    lat, lon = city_info['lat'], city_info['lon']
    
    logger.info(f"Collecting data for {city_info['name']}, {city_info['country']}...")
    
    current_weather = get_current_weather(lat, lon)
    if current_weather:
        air_data = get_air_pollution_data(lat, lon)
        save_data(city_info, current_weather, air_data)
    else:
        logger.error(f"Failed to collect weather data for {city_info['name']}")

def collect_data_for_all_cities() -> None:
    """Collect data for all cities"""
    logger.info(f"Starting data collection at {datetime.now().isoformat()}")
    
    for city_info in CITIES:
        try:
            collect_data_for_city(city_info)
            time.sleep(1)  # Rate limiting
        except Exception as e:
            logger.error(f"Error collecting data for {city_info['name']}: {e}")
    
    logger.info(f"Data collection completed at {datetime.now().isoformat()}")