# Weather Data Collection System

A full-stack application for collecting and displaying weather data and air quality information from multiple cities using the OpenWeather API.

## Prerequisites

- Python 3.8 or higher
- Bun.js (for frontend)
- Git
- OpenWeather API key (Get it here: https://openweathermap.org/api)

## Project Structure
```
weather-app/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   └── services/
│   ├── data/
│   └── requirements.txt
└── frontend/         # Vue.js frontend
    ├── src/
    ├── public/
    └── package.json
```
## Installation

### 1. Clone the Repository

git clone https://github.com/yourusername/weather-app.git
cd weather-app

### 2. Backend Setup

# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENWEATHER_API_KEY=your_api_key_here" > .env

# Initialize the database
python -m app.database.init_db

### 3. Frontend Setup

# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
bun install

## Configuration

### Backend Configuration

Edit the following files to customize the backend:

- backend/app/core/config.py: General settings like API endpoints and intervals
- backend/app/core/cities.py: List of cities to collect data from
- backend/.env: Environment variables (API keys, database settings)

Example .env file:
OPENWEATHER_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./data/weather_data.db
COLLECTION_INTERVAL=3600
DEBUG=False

### Frontend Configuration

- Edit frontend/src/services/api.js to change API base URL if needed
- Environment variables can be added to .env file in frontend directory

## Running the Application

### Start the Backend

# From the backend directory, with virtual environment activated
uvicorn app.api.app:app --host 0.0.0.0 --port 8000 --reload

The backend will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

### Start the Frontend

# From the frontend directory
bun dev

The frontend will be available at:
- http://localhost:8080

## API Endpoints

- GET /api/v1/weather: Get weather data
- GET /api/v1/air-pollution: Get air pollution data
- GET /api/v1/statistics: Get statistical data
- POST /api/v1/collector/start: Start data collection
- POST /api/v1/collector/stop: Stop data collection
- GET /api/v1/collector/status: Get collector status

## Development

### Backend Development

# Run tests (if implemented)
pytest

# Check code style
flake8

### Frontend Development

# Lint and fix files
bun run lint

# Build for production
bun run build

## Contributing

1. Fork the repository
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## Troubleshooting

### Common Issues

1. Database Initialization Failed
   - Check if you have write permissions in the data directory
   - Ensure SQLite is installed on your system

2. API Key Issues
   - Verify your OpenWeather API key is correct
   - Check if the .env file is in the correct location

3. Frontend API Connection Issues
   - Ensure backend is running and accessible
   - Check CORS settings in backend
   - Verify API base URL in frontend configuration

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

- OpenWeather API for providing weather data
- FastAPI framework
- Vue.js framework