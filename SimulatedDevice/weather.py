from datetime import datetime, UTC
from dotenv import load_dotenv
import requests

from config import POSITION, USER_AGENT

load_dotenv()

BASE_URL = "https://api.weather.gov"
HEADERS = {"User-Agent": USER_AGENT}

def fetch_weather():
    try:
        # Get point metadata
        point_data = requests.get(f"{BASE_URL}/points/{POSITION}", headers=HEADERS).json()
        gridId = point_data['properties']['gridId']
        gridX = point_data['properties']['gridX']
        gridY = point_data['properties']['gridY']

        # Get forecast data
        grid_url = f"{BASE_URL}/gridpoints/{gridId}/{gridX},{gridY}"
        grid_data = requests.get(grid_url, headers=HEADERS).json()

        # Extract desired fields
        properties = grid_data.get("properties", {})

        field_list = ["temperature", "relativeHumidity", "skyCover", "windGust",
                      "windSpeed", "windDirection", "visibility", "ceilingHeight",
                      "probabilityOfPrecipitation", "quantitativePrecipitation"]
        
        fields = {field: None for field in field_list}

        for field in fields:
            values = properties.get(field, {}).get("values", [])
            if values:
                fields[field] = values[0]["value"]

        # Get preset weather (as description)
        weather_description = properties.get("weather", {}).get("values", [])
        preset_weather = weather_description[0]["value"] if weather_description else "Unknown"

        return {
            "timestamp": datetime.now(UTC).isoformat(),
            **fields,
            "cloudCover": fields["skyCover"],
            "presetWeather": preset_weather
        }

    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None
    
if __name__ == "__main__":
    print("Fetching weather data...")
    weather_data = fetch_weather()
    if weather_data:
        print(weather_data)
    else:
        print("Failed to fetch weather data.")