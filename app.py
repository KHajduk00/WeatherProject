from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, timedelta
import sqlite3
from models import WeatherData, AirPollutionData, CityStats, WeatherQueryParams
import logging
from collector_service import CollectorService
from database import get_db

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
    allow_origins=["*"],
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