from azure.iot.device import IoTHubDeviceClient, Message
from azure.cosmos import CosmosClient, PartitionKey
import json
import datetime
import os

# Configuration for Cosmos DB connection
COSMOS_ENDPOINT = "your-cosmos-db-endpoint"
COSMOS_KEY = "your-cosmos-db-key"
DATABASE_NAME = "SensorData"
CONTAINER_NAME = "Readings"

# IoT Hub Configuration
IOTHUB_CONNECTION_STRING = "HostName=CS496ProjectHub.azure-devices.net;DeviceId=FirstDevice;SharedAccessKey=Bygk3gIvOcqlIfjsJSpTAFIdy50qRJGeTbrV9X0FKeg="  # Device connection string

# Initialize CosmosClient for Cosmos DB
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

# Initialize the IoT Hub device client
device_client = IoTHubDeviceClient.create_from_connection_string(IOTHUB_CONNECTION_STRING)

# Function to send telemetry data (temperature, humidity) to IoT Hub
def send_telemetry_to_iot_hub(temperature, humidity):
    try:
        # Create the message to send
        telemetry_data = {
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

        # Convert the telemetry data to a JSON string
        message = Message(json.dumps(telemetry_data))
        
        # Send the message to IoT Hub
        device_client.send_message(message)
        print(f"Sent message: {message}")
    except Exception as e:
        print(f"Error sending telemetry data: {e}")

# Function to handle incoming telemetry data from IoT Hub and store in Cosmos DB
def on_message_received(message):
    try:
        # Parse the message body (JSON string)
        telemetry_data = json.loads(message.data.decode("utf-8"))
        
        # Extract temperature, humidity, and timestamp
        temperature = telemetry_data['temperature']
        humidity = telemetry_data['humidity']
        timestamp = telemetry_data['timestamp']

        # Store the data in Cosmos DB
        sensor_id = "sensor_1"  # In real scenarios, this can be dynamic or based on device info
        document = {
            "id": str(datetime.datetime.utcnow()),  # Unique ID based on timestamp
            "sensorId": sensor_id,
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": timestamp,
            "_partitionKey": sensor_id  # Partition key
        }

        # Insert or upsert the document into the Cosmos DB container
        container.upsert_item(document)
        print(f"Successfully stored telemetry data in Cosmos DB: {json.dumps(document, indent=2)}")
    except Exception as e:
        print(f"Error processing received message: {e}")

# Set up the message handler to receive messages from IoT Hub
device_client.on_message_received = on_message_received

# Example of sending telemetry data from a device (simulate periodic sensor readings)
send_telemetry_to_iot_hub(22.5, 60)  # Example: temperature 22.5°C, humidity 60%

# Simulate the device receiving telemetry from IoT Hub (typically this would be a long-running process)
try:
    print("Waiting for messages from IoT Hub...")
    device_client.loop_forever()  # Keep listening for messages from IoT Hub
except KeyboardInterrupt:
    print("Device client has stopped.")
finally:
    # Close the IoT Hub connection
    device_client.shutdown()

