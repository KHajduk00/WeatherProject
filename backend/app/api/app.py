from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, timedelta
import sqlite3
import logging

from app.models.models import WeatherData, AirPollutionData, CityStats, WeatherQueryParams
from app.services.collector_service import CollectorService
from app.database.database import get_db
from app.core.config import ALLOWED_ORIGINS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title="Weather Data API",
    description="API for collecting and retrieving weather and air pollution data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

collector_service = CollectorService()

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API status and database connection
    """
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()

            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "database": {
                    "connected": True,
                    "tables_count": len(tables)
                },
                "version": app.version
            }
    except sqlite3.Error as e:
        logger.error(f"Database health check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

@app.get("/api/v1/weather", response_model=List[WeatherData])
async def get_weather_data(
    city: Optional[str] = None,
    country: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Get weather data with optional filtering
    """
    try:
        query = """
            SELECT 
                c.name, c.country, w.measurement_timestamp,
                w.temperature, w.feels_like, w.humidity,
                w.pressure, w.wind_speed, w.weather_description
            FROM weather_measurements w
            JOIN cities c ON w.city_id = c.city_id
            WHERE 1=1
        """
        params = []

        if city:
            query += " AND c.name = ?"
            params.append(city)
        if country:
            query += " AND c.country = ?"
            params.append(country)
        if start_date:
            query += " AND w.measurement_timestamp >= ?"
            params.append(start_date.isoformat())
        if end_date:
            query += " AND w.measurement_timestamp <= ?"
            params.append(end_date.isoformat())

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()

            return [
                WeatherData(
                    city=row[0],
                    country=row[1],
                    measurement_timestamp=datetime.fromisoformat(row[2]),
                    temperature=row[3],
                    feels_like=row[4],
                    humidity=row[5],
                    pressure=row[6],
                    wind_speed=row[7],
                    weather_description=row[8]
                )
                for row in results
            ]

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/api/v1/air-pollution", response_model=List[AirPollutionData])
async def get_air_pollution_data(
    city: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Get air pollution data with optional filtering
    """
    try:
        query = """
            SELECT 
                c.name, c.country, a.measurement_timestamp,
                a.aqi, a.co, a.no2, a.o3, a.pm2_5, a.pm10
            FROM air_pollution_measurements a
            JOIN cities c ON a.city_id = c.city_id
            WHERE 1=1
        """
        params = []

        if city:
            query += " AND c.name = ?"
            params.append(city)
        if start_date:
            query += " AND a.measurement_timestamp >= ?"
            params.append(start_date.isoformat())
        if end_date:
            query += " AND a.measurement_timestamp <= ?"
            params.append(end_date.isoformat())

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()

            return [
                AirPollutionData(
                    city=row[0],
                    country=row[1],
                    measurement_timestamp=datetime.fromisoformat(row[2]),
                    aqi=row[3],
                    co=row[4],
                    no2=row[5],
                    o3=row[6],
                    pm2_5=row[7],
                    pm10=row[8]
                )
                for row in results
            ]

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/api/v1/statistics", response_model=List[CityStats])
async def get_statistics(
    city: Optional[str] = None,
    days: Optional[int] = Query(default=7, ge=1, le=30)
):
    """
    Get statistical data for cities
    """
    try:
        start_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        query = """
            SELECT 
                c.name,
                AVG(w.temperature) as avg_temp,
                MAX(w.temperature) as max_temp,
                MIN(w.temperature) as min_temp,
                AVG(a.aqi) as avg_aqi,
                COUNT(w.weather_id) as measurement_count
            FROM cities c
            LEFT JOIN weather_measurements w ON c.city_id = w.city_id
            LEFT JOIN air_pollution_measurements a ON c.city_id = a.city_id
            WHERE w.measurement_timestamp >= ?
            GROUP BY c.name
        """
        params = [start_date]

        if city:
            query += " HAVING c.name = ?"
            params.append(city)

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()

            return [
                CityStats(
                    city=row[0],
                    avg_temperature=row[1],
                    max_temperature=row[2],
                    min_temperature=row[3],
                    avg_aqi=row[4],
                    measurements_count=row[5]
                )
                for row in results
            ]

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/api/v1/analytics/weather-pollution-correlation")
async def get_weather_pollution_correlation(
    city: Optional[str] = None,
    days: Optional[int] = Query(default=30, ge=7, le=90)
):
    """
    Get weather and pollution data correlation for analysis
    """
    try:
        start_date = (datetime.now() - timedelta(days=days)).isoformat()

        query = """
            SELECT
                c.name as city,
                w.measurement_timestamp,
                w.temperature,
                w.humidity,
                w.pressure,
                w.wind_speed,
                w.weather_description,
                a.aqi,
                a.pm2_5,
                a.pm10,
                a.no2,
                a.o3,
                a.co
            FROM weather_measurements w
            JOIN cities c ON w.city_id = c.city_id
            JOIN air_pollution_measurements a ON w.city_id = a.city_id
                AND datetime(w.measurement_timestamp) = datetime(a.measurement_timestamp)
            WHERE w.measurement_timestamp >= ?
        """
        params = [start_date]

        if city:
            query += " AND c.name = ?"
            params.append(city)

        query += " ORDER BY w.measurement_timestamp DESC"

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return [
                {
                    "city": row[0],
                    "timestamp": row[1],
                    "temperature": row[2],
                    "humidity": row[3],
                    "pressure": row[4],
                    "wind_speed": row[5],
                    "weather_description": row[6],
                    "aqi": row[7],
                    "pm2_5": row[8],
                    "pm10": row[9],
                    "no2": row[10],
                    "o3": row[11],
                    "co": row[12]
                }
                for row in results
            ]

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/api/v1/analytics/high-pollution-alerts")
async def get_high_pollution_alerts(
    aqi_threshold: Optional[int] = Query(default=100, ge=50, le=300),
    pm25_threshold: Optional[float] = Query(default=35.0, ge=10.0, le=100.0),
    days: Optional[int] = Query(default=30, ge=7, le=90)
):
    """
    Get high pollution events with associated weather conditions for alert analysis
    """
    try:
        start_date = (datetime.now() - timedelta(days=days)).isoformat()

        query = """
            SELECT
                c.name as city,
                w.measurement_timestamp,
                w.temperature,
                w.humidity,
                w.pressure,
                w.wind_speed,
                w.weather_description,
                a.aqi,
                a.pm2_5,
                a.pm10,
                a.no2,
                CASE
                    WHEN a.aqi > ? OR a.pm2_5 > ? THEN 1
                    ELSE 0
                END as is_high_pollution_event
            FROM weather_measurements w
            JOIN cities c ON w.city_id = c.city_id
            JOIN air_pollution_measurements a ON w.city_id = a.city_id
                AND datetime(w.measurement_timestamp) = datetime(a.measurement_timestamp)
            WHERE w.measurement_timestamp >= ?
                AND (a.aqi > ? OR a.pm2_5 > ?)
            ORDER BY a.aqi DESC, a.pm2_5 DESC
        """
        params = [aqi_threshold, pm25_threshold, start_date, aqi_threshold, pm25_threshold]

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()

            return [
                {
                    "city": row[0],
                    "timestamp": row[1],
                    "temperature": row[2],
                    "humidity": row[3],
                    "pressure": row[4],
                    "wind_speed": row[5],
                    "weather_description": row[6],
                    "aqi": row[7],
                    "pm2_5": row[8],
                    "pm10": row[9],
                    "no2": row[10],
                    "is_high_pollution_event": row[11]
                }
                for row in results
            ]

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/api/v1/analytics/prediction-data")
async def get_prediction_data(
    city: Optional[str] = None,
    hours_back: Optional[int] = Query(default=168, ge=24, le=720)  # Default 7 days
):
    """
    Get time series data for AQI prediction modeling
    """
    try:
        start_date = (datetime.now() - timedelta(hours=hours_back)).isoformat()

        query = """
            SELECT
                c.name as city,
                w.measurement_timestamp,
                w.temperature,
                w.humidity,
                w.pressure,
                w.wind_speed,
                a.aqi,
                a.pm2_5,
                a.no2,
                LAG(a.aqi, 1) OVER (PARTITION BY c.name ORDER BY w.measurement_timestamp) as prev_aqi_1h,
                LAG(a.aqi, 3) OVER (PARTITION BY c.name ORDER BY w.measurement_timestamp) as prev_aqi_3h,
                LAG(a.aqi, 6) OVER (PARTITION BY c.name ORDER BY w.measurement_timestamp) as prev_aqi_6h,
                LEAD(a.aqi, 12) OVER (PARTITION BY c.name ORDER BY w.measurement_timestamp) as future_aqi_12h,
                LEAD(a.aqi, 24) OVER (PARTITION BY c.name ORDER BY w.measurement_timestamp) as future_aqi_24h
            FROM weather_measurements w
            JOIN cities c ON w.city_id = c.city_id
            JOIN air_pollution_measurements a ON w.city_id = a.city_id
                AND datetime(w.measurement_timestamp) = datetime(a.measurement_timestamp)
            WHERE w.measurement_timestamp >= ?
        """
        params = [start_date]

        if city:
            query += " AND c.name = ?"
            params.append(city)

        query += " ORDER BY c.name, w.measurement_timestamp"

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()

            return [
                {
                    "city": row[0],
                    "timestamp": row[1],
                    "temperature": row[2],
                    "humidity": row[3],
                    "pressure": row[4],
                    "wind_speed": row[5],
                    "aqi": row[6],
                    "pm2_5": row[7],
                    "no2": row[8],
                    "prev_aqi_1h": row[9],
                    "prev_aqi_3h": row[10],
                    "prev_aqi_6h": row[11],
                    "future_aqi_12h": row[12],
                    "future_aqi_24h": row[13]
                }
                for row in results if row[12] is not None  # Only include rows where we have future data
            ]

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@app.post("/api/v1/collector/start")
async def start_collector():
    """Start the data collection process"""
    success, message = collector_service.start_collection()
    if success:
        return {"status": "success", "message": message}
    raise HTTPException(status_code=400, detail=message)

@app.post("/api/v1/collector/stop")
async def stop_collector():
    """Stop the data collection process"""
    success, message = collector_service.stop_collection()
    if success:
        return {"status": "success", "message": message}
    raise HTTPException(status_code=400, detail=message)

@app.get("/api/v1/collector/status")
async def get_collector_status():
    """Get the current status of the collector"""
    status = collector_service.get_status()
    return status

@app.put("/api/v1/collector/interval")
async def set_collection_interval(interval: int = Query(..., gt=0)):
    """Set the collection interval in seconds"""
    success, message = collector_service.set_interval(interval)
    if success:
        return {"status": "success", "message": message}
    raise HTTPException(status_code=400, detail=message)

@app.get("/api/v1/analytics/prediction-data-flexible")
async def get_prediction_data_flexible(
    city: Optional[str] = None,
    hours_back: Optional[int] = Query(default=168, ge=24, le=720)
):
    """
    Get time series data for AQI prediction modeling with flexible time windows
    """
    try:
        start_date = (datetime.now() - timedelta(hours=hours_back)).isoformat()

        query = """
            WITH time_series AS (
                SELECT
                    c.name as city,
                    w.measurement_timestamp,
                    w.temperature,
                    w.humidity,
                    w.pressure,
                    w.wind_speed,
                    a.aqi,
                    a.pm2_5,
                    a.no2,
                    ROW_NUMBER() OVER (PARTITION BY c.name ORDER BY w.measurement_timestamp) as row_num
                FROM weather_measurements w
                JOIN cities c ON w.city_id = c.city_id
                JOIN air_pollution_measurements a ON w.city_id = a.city_id
                    AND datetime(w.measurement_timestamp) = datetime(a.measurement_timestamp)
                WHERE w.measurement_timestamp >= ?
            )
            SELECT
                ts1.city,
                ts1.measurement_timestamp,
                ts1.temperature,
                ts1.humidity,
                ts1.pressure,
                ts1.wind_speed,
                ts1.aqi,
                ts1.pm2_5,
                ts1.no2,
                -- Previous values (if available)
                LAG(ts1.aqi, 1) OVER (PARTITION BY ts1.city ORDER BY ts1.measurement_timestamp) as prev_aqi_1,
                LAG(ts1.aqi, 2) OVER (PARTITION BY ts1.city ORDER BY ts1.measurement_timestamp) as prev_aqi_2,
                -- Future values using smaller windows that might actually exist
                LEAD(ts1.aqi, 1) OVER (PARTITION BY ts1.city ORDER BY ts1.measurement_timestamp) as future_aqi_next,
                LEAD(ts1.aqi, 2) OVER (PARTITION BY ts1.city ORDER BY ts1.measurement_timestamp) as future_aqi_2nd,
                -- Try to find future values within reasonable time windows
                (
                    SELECT a2.aqi 
                    FROM weather_measurements w2
                    JOIN air_pollution_measurements a2 ON w2.city_id = a2.city_id
                        AND datetime(w2.measurement_timestamp) = datetime(a2.measurement_timestamp)
                    WHERE w2.city_id = (SELECT city_id FROM cities WHERE name = ts1.city)
                        AND w2.measurement_timestamp > ts1.measurement_timestamp
                        AND w2.measurement_timestamp <= datetime(ts1.measurement_timestamp, '+1 day')
                    ORDER BY w2.measurement_timestamp
                    LIMIT 1
                ) as future_aqi_24h_approx
            FROM time_series ts1
        """
        params = [start_date]

        if city:
            query += " WHERE ts1.city = ?"
            params.append(city)

        query += " ORDER BY ts1.city, ts1.measurement_timestamp"

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()

            return [
                {
                    "city": row[0],
                    "timestamp": row[1],
                    "temperature": row[2],
                    "humidity": row[3],
                    "pressure": row[4],
                    "wind_speed": row[5],
                    "aqi": row[6],
                    "pm2_5": row[7],
                    "no2": row[8],
                    "prev_aqi_1": row[9],
                    "prev_aqi_2": row[10],
                    "future_aqi_next": row[11],
                    "future_aqi_2nd": row[12],
                    "future_aqi_24h_approx": row[13]
                }
                for row in results
            ]

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "name": "Weather Data API",
        "version": app.version,
        "documentation": "/docs",
        "health_check": "/health"
    }

