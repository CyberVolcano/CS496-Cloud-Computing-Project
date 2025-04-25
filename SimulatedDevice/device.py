from paho.mqtt import client as mqtt
from dotenv import load_dotenv
import certifi, ssl, os, json
from utils import make_sas
from weather import fetch_weather

load_dotenv()

# Load environment variables from .env file
iot_hub_hostname = os.environ.get("IOT_HUB_NAME") + ".azure-devices.net"
device_id = os.environ.get("DEVICE_ID") 
shared_access_key = os.environ.get("SHARED_ACCESS_KEY") 
sas_token = make_sas(iot_hub_hostname, device_id, shared_access_key)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Azure IoT Hub")
        
        # Fetch weather data
        weather_data = fetch_weather()
        
        # Create a test message
        test_message = {"test": 123}
        
        # Combine the weather data and test message
        if weather_data:
            combined_message = {**test_message, **weather_data}
        else:
            combined_message = test_message
        
        # Convert the combined message to JSON
        message_payload = json.dumps(combined_message)
        
        # Publish the combined message
        print("Publishing message:", message_payload)  # Debugging print
        client.publish(f"devices/{device_id}/messages/events/", message_payload, qos=1)

def on_disconnect(client, userdata, rc):
    print("Device disconnected with result code: " + str(rc))
    

def on_publish(client, userdata, mid):
    print("Device sent message")

def run_device():
    client = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311)
    client.username_pw_set(username=f"{iot_hub_hostname}/{device_id}/?api-version=2021-04-12",
                        password=sas_token)

    # use certifi so you never need to download .pem by hand
    client.tls_set(ca_certs=certifi.where(),
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2)

    client.on_connect    = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish    = on_publish

    # 5) Connect & loop
    client.connect(iot_hub_hostname, port=8883)
    client.loop_forever()

if __name__ == "__main__":
    run_device()