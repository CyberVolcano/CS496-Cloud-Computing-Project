from azure.iot.device import IoTHubDeviceClient, Message
import random
import time

# Replace with your device connection string
CONNECTION_STRING = "Your_IoT_Device_Connection_String"

# Create an IoT Hub client
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

def send_telemetry():
    while True:
        # Example telemetry data
        telemetry_data = {
            "temperature": round(random.uniform(20.0, 30.0), 2),
            "humidity": round(random.uniform(30.0, 60.0), 2)
        }
        message = Message(str(telemetry_data))
        message.content_encoding = "utf-8"
        message.content_type = "application/json"

        print(f"Sending message: {message}")
        client.send_message(message)
        time.sleep(5)  # Send data every 5 seconds

try:
    send_telemetry()
except KeyboardInterrupt:
    print("Stopped sending data")
finally:
    client.shutdown()
