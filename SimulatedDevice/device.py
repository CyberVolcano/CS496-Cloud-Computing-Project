from paho.mqtt import client as mqtt
import certifi, ssl, json
from utils import make_sas
from weather import fetch_weather
from config import IOT_HUB_HOSTNAME, DEVICE_ID, SHARED_ACCESS_KEY

sas_token = make_sas(IOT_HUB_HOSTNAME, DEVICE_ID, SHARED_ACCESS_KEY)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Azure IoT Hub")
        
        # Fetch weather data
        weather_data = fetch_weather()
        if weather_data:
            print("Weather data fetched successfully:", weather_data)

            message_payload = json.dumps(weather_data)

             # Publish the combined message
            print("Publishing message:", message_payload)  # Debugging print
            client.publish(f"devices/{DEVICE_ID}/messages/events/", message_payload, qos=1)

        else:
            print("Failed to fetch weather data")

def on_disconnect(client, userdata, rc):
    print("Device disconnected with result code: " + str(rc))
    

def on_publish(client, userdata, mid):
    print("Device sent message")

def run_device():
    client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv311)
    client.username_pw_set(username=f"{IOT_HUB_HOSTNAME}/{DEVICE_ID}/?api-version=2021-04-12",
                        password=sas_token)

    # use certifi so you never need to download .pem by hand
    client.tls_set(ca_certs=certifi.where(),
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2)

    client.on_connect    = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish    = on_publish

    # 5) Connect & loop
    client.connect(IOT_HUB_HOSTNAME, port=8883)
    client.loop_forever()

if __name__ == "__main__":
    run_device()