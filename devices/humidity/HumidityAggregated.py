from azure.iot.device import IoTHubDeviceClient, Message
from ..util.load_env import create_connection_string, is_dev_mode, is_prod_mode
import time, random, json, yaml, os

class HumidityAggregatedDevice:
    """ A simulated IoT device that generates and aggregates temperature and humidity data.

    This device can operate in two modes:
    - Development (DEV): Prints data to console
    - Production (PROD): Sends data to Azure IoT Hub

    The device collects temperature and humidity readings at specified intervals,
    aggregates them, and either prints or sends the statistics to IoT Hub.

    Attributes:
        client (IoTHubDeviceClient): Azure IoT Hub client connection (None in DEV mode)
        aggregation_interval (int): Number of readings to collect before processing
        sampling_interval (float): Time in seconds between readings
        temp_min (float): Minimum temperature value
        temp_max (float): Maximum temperature value
        temp_decimal_places (int): Decimal precision for temperature readings
        humidity_min (float): Minimum humidity value
        humidity_max (float): Maximum humidity value
        humidity_decimal_places (int): Decimal precision for humidity readings
    """
    def __init__(self):
        """ Initialize the device with configuration from YAML file.

        Loads device configuration from humidity_config.yaml and establishes
        IoT Hub connection if in PROD mode.
        """
        self.client = None

        # Connect to the client if in production mode
        if is_prod_mode():
            CONNECTION_STRING = create_connection_string("HUMIDITY_DEVICE_ID")
            self.client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

        # Load the yaml config
        with open(os.path.join(os.path.dirname(__file__), "humidity_config.yaml"), "r") as file:
            config = yaml.safe_load(file)

        self.aggregation_interval = config["device"]["sampling"]["aggregation_count"]
        self.sampling_interval = config["device"]["sampling"]["interval"]
        
        self.temp_min = config["device"]["sensors"]["temperature"]["min"]
        self.temp_max = config["device"]["sensors"]["temperature"]["max"]
        self.temp_decimal_places = config["device"]["sensors"]["temperature"]["decimal_places"]

        self.humidity_min = config["device"]["sensors"]["humidity"]["min"]
        self.humidity_max = config["device"]["sensors"]["humidity"]["max"]
        self.humidity_decimal_places = config["device"]["sensors"]["humidity"]["decimal_places"]

    def shutdown(self):
        """ Safely shutdown the IoT Hub client connection.

        Should be called when device operation is complete or interrupted.
        """
        try:
            if self.client is not None:
                self.client.shutdown()
        except Exception as e:
            print(e)
    
    def send_edge_computed_telemetry(self) -> None:
        """ Generate and process sensor data continuously.

        Collects temperature and humidity readings at specified intervals.
        Once enough readings are collected (specified by aggregation_interval),
        calculates statistics and either:
        - DEV mode: Prints statistics to console
        - PROD mode: Sends statistics to Azure IoT Hub as JSON message

        The following statistics are computed:
        - Minimum, maximum, and average temperature
        - Minimum, maximum, and average humidity
        - Number of readings in the aggregation

        Raises:
            KeyboardInterrupt: When user stops the process
            Exception: For any other unexpected errors
        """
        # Lists to store sensor readings locally
        collected_temperatures = []
        collected_humidities = []
        
        while True:
            # Generate simulated sensor readings
            temperature = round(random.uniform(self.temp_min, self.temp_max), self.temp_decimal_places)
            humidity = round(random.uniform(self.humidity_min, self.humidity_max), self.humidity_decimal_places)
            
            # Store readings locally
            collected_temperatures.append(temperature)
            collected_humidities.append(humidity)
            
            # When enough data is collected, process and send the aggregated metrics
            if len(collected_temperatures) >= self.aggregation_interval:
                min_temp = min(collected_temperatures)
                max_temp = max(collected_temperatures)
                min_humidity = min(collected_humidities)
                max_humidity = max(collected_humidities)
                avg_temperature = round(sum(collected_temperatures) / len(collected_temperatures), 2)
                avg_humidity = round(sum(collected_humidities) / len(collected_humidities), 2)
                
                telemetry_data = {
                    "min_temperature": min_temp,
                    "max_temperature": max_temp,
                    "avg_temperature": avg_temperature,
                    "min_humidity": min_humidity,
                    "max_humidity": max_humidity,
                    "avg_humidity": avg_humidity,
                    "reading_count": self.aggregation_interval
                }
                
                if self.client is not None and is_prod_mode():
                    # Convert the data to a JSON string for sending
                    message = Message(json.dumps(telemetry_data))
                    message.content_encoding = "utf-8"
                    message.content_type = "application/json"
                    
                    print(f"Sending aggregated message: {message}")
                    self.client.send_message(message)
                
                if is_dev_mode():
                    print(f"Aggregated the following data:")

                    for key, value in telemetry_data.items():
                        print("\t{}: {}".format(key, value))

                    print("")

                # Reset the lists for the next aggregation interval
                collected_temperatures = []
                collected_humidities = []

            elif is_dev_mode():
                print(f'Collected Humidities: {collected_humidities} \nCollected Temperatures: {collected_temperatures} \n\n')
            
            # Wait before collecting the next reading
            time.sleep(self.sampling_interval)

if __name__ == "__main__":
    try:
        device = HumidityAggregatedDevice()
        device.send_edge_computed_telemetry()

    except KeyboardInterrupt:
        print("Stopped sending data")
    finally:
        device.shutdown()