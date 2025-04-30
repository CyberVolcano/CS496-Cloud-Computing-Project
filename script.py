import json
import requests
from datetime import datetime, UTC
import paho.mqtt.client as mqtt
from azure.iot.device import IoTHubDeviceClient, Message

# Azure IoT Hub connection string
AZURE_CONNECTION_STRING = "HostName=CS496ProjectHub.azure-devices.net;DeviceId=FirstDevice;SharedAccessKey=Bygk3gIvOcqlIfjsJSpTAFIdy50qRJGeTbrV9X0FKeg="

# Weather API settings
LAT, LON = 32.7157, -117.1611  # San Diego
POINT = f"{LAT},{LON}"
BASE_URL = "https://api.weather.gov"
HEADERS = {"User-Agent": "CS496IotProject (aolson2733@sdsu.edu)"}

# Initialize clients
mqtt_client = mqtt.Client()
azure_client = IoTHubDeviceClient.create_from_connection_string(AZURE_CONNECTION_STRING)

def fetch_weather():
    try:
        # Get point metadata
        point_data = requests.get(f"{BASE_URL}/points/{POINT}", headers=HEADERS).json()
        gridId = point_data['properties']['gridId']
        gridX = point_data['properties']['gridX']
        gridY = point_data['properties']['gridY']

        # Get forecast data
        grid_url = f"{BASE_URL}/gridpoints/{gridId}/{gridX},{gridY}"
        grid_data = requests.get(grid_url, headers=HEADERS).json()

        # Extract desired fields
        properties = grid_data.get("properties", {})
        fields = {
            "temperature": None,
            "relativeHumidity": None,
            "skyCover": None,
            "windGust": None,
            "windSpeed": None,
            "windDirection": None,
            "visibility": None,
            "ceilingHeight": None,
            "probabilityOfPrecipitation": None,
            "quantitativePrecipitation": None,
        }

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

def run_once():
    try:
        print("Connecting to Azure IoT Hub...")
        azure_client.connect()

        weather_data = fetch_weather()
        if weather_data:
            json_payload = json.dumps(weather_data)

            # Send to Azure
            azure_msg = Message(json_payload)
            azure_msg.content_encoding = "utf-8"
            azure_msg.content_type = "application/json"
            azure_client.send_message(azure_msg)
            print("Sent to Azure")

        else:
            print("Skipping send — no weather data available.")

    finally:
        azure_client.shutdown()
        print("Disconnected from Azure.")

if __name__ == "__main__":
    run_once()