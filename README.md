## How to Use
### Create a .env file in the project directory with your OpenWeather API key:

```bash
OPENWEATHER_API_KEY=your_api_key_here
```

### Install the required dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### Configure settings (optional):

- Edit COLLECTION_INTERVAL in config.py to change how often data is collected (default is 3600 seconds = 1 hour)
- Edit CITIES in cities.py to add or remove cities
- Change OUTPUT_CSV_PATH in config.py to change the output file location

### Run the collector:

```bash
python collector.py
```

To stop the collector, press Ctrl+C. The program will gracefully stop after the current collection cycle completes.