# Weather Data Collection System

A full-stack application for collecting and displaying weather data and air quality information from multiple cities using the OpenWeather API.

## Prerequisites

* Python 3.8+
* Bun.js
* OpenWeather API key ([Get it here](https://openweathermap.org/api))

## Installation

### 1. Clone the Repository
```
git clone https://github.com/yourusername/weather-app.git
cd weather-app
```

### 2. Backend Setup
```
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with your API key
echo "OPENWEATHER_API_KEY=your_api_key_here" > .env

# Initialize database
python -m app.database.init_db
```

### 3. Frontend Setup
```
cd frontend
bun install
```

## Configuration

### Backend
Edit these files to customize:
- `backend/app/core/config.py`: General settings
- `backend/app/core/cities.py`: Cities to collect data from
- `backend/.env`: Environment variables

### Frontend
- Edit `frontend/src/services/api.js` to change API base URL if needed

## Running the Application

### Start Backend
```
cd backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uvicorn app.api.app:app --host 0.0.0.0 --port 8000 --reload
```
Access at: http://localhost:8000 (API docs at /docs)

### Start Frontend
```
cd frontend
bun dev
```
Access at: http://localhost:8080

## Main API Endpoints

- `GET /api/v1/weather`: Get weather data
- `GET /api/v1/air-pollution`: Get air pollution data
- `GET /api/v1/statistics`: Get statistical data
- `POST /api/v1/collector/start`: Start data collection
- `POST /api/v1/collector/stop`: Stop data collection

## Troubleshooting

- **Database issues**: Check write permissions in data directory
- **API key issues**: Verify your OpenWeather API key is correct
- **Frontend connection issues**: Ensure backend is running and accessible