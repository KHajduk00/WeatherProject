from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Request Models
class DateRangeParams(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class WeatherQueryParams(DateRangeParams):
    city: Optional[str] = None
    country: Optional[str] = None
    measurement_type: Optional[List[str]] = None

# Response Models
class WeatherData(BaseModel):
    city: str
    country: str
    measurement_timestamp: datetime
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    weather_description: str

class AirPollutionData(BaseModel):
    city: str
    country: str
    measurement_timestamp: datetime
    aqi: int
    co: float
    no2: float
    o3: float
    pm2_5: float
    pm10: float

class CityStats(BaseModel):
    city: str
    avg_temperature: float
    max_temperature: float
    min_temperature: float
    avg_aqi: float
    measurements_count: int