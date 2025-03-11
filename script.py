from azure.iot.device import IoTHubDeviceClient, Message
import time
import random

# Device connection string from Azure IoT Hub
CONNECTION_STRING = "HostName=CS496ProjectHub.azure-devices.net;DeviceId=FirstDevice;SharedAccessKey=Bygk3gIvOcqlIfjsJSpTAFIdy50qRJGeTbrV9X0FKeg="

# Initialize the device client
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

def send_telemetry():
    try:
        print("Connecting to Azure IoT Hub...")
        client.connect()
        
        while True:
            temperature = random.uniform(20, 30)  # Simulated temperature data
            humidity = random.uniform(40, 60)    # Simulated humidity data

            message = Message(f'{{"temperature": {temperature}, "humidity": {humidity}}}')
            message.content_encoding = "utf-8"
            message.content_type = "application/json"

            print(f"Sending message: {message}")
            client.send_message(message)

            time.sleep(5)  # Send data every 5 seconds

    except KeyboardInterrupt:
        print("\nStopping telemetry...")
    finally:
        client.shutdown()

if __name__ == "__main__":
    send_telemetry()