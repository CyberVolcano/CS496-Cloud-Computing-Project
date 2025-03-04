from azure.iot.device import IoTHubDeviceClient, Message
from devices.util.load_env import create_connection_string
import time, random, json

"""
This is just an example of what another dvice might look like

It has an alert example but we can work on the other script and add alerts to it.
"""

# No connection string since we haven't decided if we are doing a second device
CONNECTION_STRING = create_connection_string("")

# Create an IoT Hub client for the second device
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

def send_vibration_alerts():
    # Set a threshold value for vibration alert
    threshold = 3.0  # example threshold value
    while True:
        # Simulate a vibration sensor reading (e.g., amplitude in g's)
        vibration_value = round(random.uniform(0.0, 5.0), 2)
        print(f"Vibration sensor reading: {vibration_value}")

        # Only send an alert if the vibration exceeds the threshold
        if vibration_value > threshold:
            telemetry_data = {
                "alert": "High Vibration Detected",
                "vibration_value": vibration_value,
                "timestamp": time.time()
            }
            message = Message(json.dumps(telemetry_data))
            message.content_encoding = "utf-8"
            message.content_type = "application/json"
            print(f"Sending alert message: {message}")
            client.send_message(message)
        else:
            print("Vibration reading within normal limits.")

        # Wait before reading the sensor again
        time.sleep(5)

try:
    send_vibration_alerts()
except KeyboardInterrupt:
    print("Stopped sending alerts")
finally:
    client.shutdown()
