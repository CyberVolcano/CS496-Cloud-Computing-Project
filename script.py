import time
import random
import json
from datetime import datetime, UTC
import paho.mqtt.client as mqtt
from azure.iot.device import IoTHubDeviceClient, Message

# Azure IoT Hub connection string
AZURE_CONNECTION_STRING = "HostName=CS496ProjectHub.azure-devices.net;DeviceId=FirstDevice;SharedAccessKey=Bygk3gIvOcqlIfjsJSpTAFIdy50qRJGeTbrV9X0FKeg="

# Local MQTT broker settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "telemetry/device1"

# Initialize MQTT client
mqtt_client = mqtt.Client()

# Initialize Azure IoT client
azure_client = IoTHubDeviceClient.create_from_connection_string(AZURE_CONNECTION_STRING)

def send_telemetry():
    try:
        print("Connecting to Azure IoT Hub...")
        azure_client.connect()

        print("Connecting to local Mosquitto broker...")
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()

        while True:
            temperature = round(random.uniform(20, 30), 2)
            humidity = round(random.uniform(40, 60), 2)
            timestamp = datetime.now(UTC).isoformat()

            payload = {
                "timestamp": timestamp,
                "temperature": temperature,
                "humidity": humidity
            }

            json_payload = json.dumps(payload)

            # Send to Azure
            azure_msg = Message(json_payload)
            azure_msg.content_encoding = "utf-8"
            azure_msg.content_type = "application/json"
            azure_client.send_message(azure_msg)
            print("✅ Sent to Azure")

            # Send to Mosquitto
            mqtt_client.publish(MQTT_TOPIC, json_payload)
            print(f"✅ Published to Mosquitto topic '{MQTT_TOPIC}'\n")

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nTelemetry stopped by user.")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        azure_client.shutdown()
        print("Disconnected from both brokers.")

if __name__ == "__main__":
    send_telemetry()
