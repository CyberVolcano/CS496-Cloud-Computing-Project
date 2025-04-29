from paho.mqtt import client as mqtt
import certifi, ssl, json, time
from utils import make_sas
from weather import fetch_weather
from config import IOT_HUB_HOSTNAME, DEVICE_ID, SHARED_ACCESS_KEY, SEND_INTERVAL

sas_token = make_sas(IOT_HUB_HOSTNAME, DEVICE_ID, SHARED_ACCESS_KEY)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Azure IoT Hub with result code: " + str(rc))

def on_disconnect(client, userdata, rc):
    print("Device disconnected with result code: " + str(rc))

def on_publish(client, userdata, mid):
    print("Device message published with mid: " + str(mid))

# Possible edge computing/processing function
def process_weather_data(weather_data):
    """
    Processes raw weather data to compute:
    - wind speed in mph
    - approximate dew point (°C)
    - simple feels-like temperature (°C) via a basic heat-index/wind-chill model.
    
    Returns a new dictionary merging the originals + the derived metrics.
    """
    out = weather_data.copy()

    t_c = weather_data.get("temperature")  # °C
    rh = weather_data.get("relativeHumidity")  # %
    ws = weather_data.get("windSpeed")  # m/s

    # Convert wind speed (m/s) to mph
    if ws is not None:
        out["wind_speed_mph"] = round(ws * 2.23694, 1)

    # Approximate dew point (°C)
    if t_c is not None and rh is not None:
        dew_point = t_c - (100 - rh) / 5.0
        out["dewPoint_c"] = round(dew_point, 1)

    # Compute feels-like temperature (°C)
    feels_like = None
    if t_c is not None and rh is not None and ws is not None:
        if t_c >= 26 and rh >= 40:
            # Simple heat-index approximation
            feels_like = t_c + 0.33 * rh - 0.70 * ws - 4.0
        elif t_c <= 10 and ws > 1.34:
            # Simple wind-chill formula
            feels_like = 13.12 + 0.6215 * t_c - 11.37 * (ws ** 0.16) + 0.3965 * t_c * (ws ** 0.16)
        
        if feels_like is not None:
            out["feelsLike_c"] = round(feels_like, 1)

    return out


def run_device():
    # Create MQTT client and set up connection parameters
    client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv311)
    client.username_pw_set(username=f"{IOT_HUB_HOSTNAME}/{DEVICE_ID}/?api-version=2021-04-12", password=sas_token)

    # Set TLS parameters
    # Note: The certifi library is used to get the CA certificates for Azure IoT Hub
    client.tls_set(ca_certs=certifi.where(),
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2)

    # Set up callbacks
    client.on_connect       = on_connect
    client.on_disconnect    = on_disconnect
    client.on_publish       = on_publish

    # Connect to Azure IoT Hub & start loop
    client.connect(IOT_HUB_HOSTNAME, port=8883)
    client.loop_start()

    try:
        while True:
            # Fetch weather data
            weather_data = fetch_weather()
            if weather_data:
                # Publish to Azure IoT Hub via MQTT
                message_payload = json.dumps(weather_data)
                client.publish(f"devices/{DEVICE_ID}/messages/events/", message_payload, qos=1)

            else:
                print("Failed to fetch weather data")

            time.sleep(SEND_INTERVAL)

    # Handle graceful shutdown
    except KeyboardInterrupt:
        print("Stopping device...")
    
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    run_device()