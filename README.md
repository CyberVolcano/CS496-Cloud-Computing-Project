### Description

This project demonstrates how real or simulated devices (e.g., sensors measuring
temperature/humidity) can send data to a central platform for real-time storage,
analytics, or dashboarding. It exposes you to event-driven architectures, message
brokering (MQTT), and how to set up dashboards for streaming data.

Use Case
 - 	A greenhouse or small farm environment logging conditions to optimize plant growth.
 - 	A “smart home” demonstration collecting sensor data (door sensors, temperature, light levels).
 - 	A robotics club streaming data from multiple bots or drones to a single dashboard.
Difficulty Bonus
3

Basic Rubric (How to Start) - D.L. Assuming we are taking the cloud route.
1.	Messaging Protocol
- [ ] Cloud: Azure IoT Hub free tier.
- Local: Mosquitto (MQTT broker) installed in a container or on your machine.
2.	Simulated Device Script
- [ ] Python or Node.js program that sends random sensor readings at intervals.
- [ ] Structure the data as JSON (e.g., { "temp": 22.5, "humidity": 60 }).
3.	Data Storage
- [ ] Azure: Use Cosmos DB or Table Storage.
-	Local: Try InfluxDB (time-series) or PostgreSQL.
5.	Visualization
- [ ] Grafana or a custom front-end that queries your DB for the latest readings.
5.	Testing
Confirm your script sends data, see it appear in the DB, and visualize in near real-time on the dashboard.
Extra Credit Opportunity (Optional)
- [ ]	Alerts & Thresholds: Trigger notifications if a sensor reading goes above/below a certain level.
- [ ]	Edge Computing: Perform partial data processing on the “device” side before sending final metrics.


### Websites

 - [Cosmos DB](https://azure.microsoft.com/en-us/products/cosmos-db/)
 - [Grafana](https://grafana.com/)
 - [Azure IOT Hub](https://learn.microsoft.com/en-us/azure/iot-hub/create-hub?tabs=portal)


### Description

This project demonstrates how real or simulated devices (e.g., sensors measuring temperature/humidity) can send data to a central platform for real-time storage, analytics, or dashboarding. It exposes you to event-driven architectures, message brokering (MQTT), and how to set up dashboards for streaming data.

**Use Cases**
- A greenhouse or small farm environment logging conditions to optimize plant growth.
- A “smart home” demonstration collecting sensor data (door sensors, temperature, light levels).
- A robotics club streaming data from multiple bots or drones to a single dashboard.

**Difficulty Bonus:** 3

---

### Basic Rubric (How to Start) - D.L. Assuming we are taking the cloud route.
1. **Messaging Protocol**
   - [ ] Cloud: Azure IoT Hub free tier.
   - [ ] Local: Mosquitto (MQTT broker) installed in a container or on your machine.
2. **Simulated Device Script**
   - [ ] Python or Node.js program that sends random sensor readings at intervals.
   - [ ] Structure the data as JSON (e.g., `{ "temp": 22.5, "humidity": 60 }`).
3. **Data Storage**
   - [ ] Azure: Use Cosmos DB or Table Storage.
   - [ ] Local: Try InfluxDB (time-series) or PostgreSQL.
4. **Visualization**
   - [ ] Grafana or a custom front-end that queries your DB for the latest readings.
5. **Testing**
   - Confirm your script sends data, see it appear in the DB, and visualize in near real-time on the dashboard.

**Extra Credit Opportunity (Optional)**
- [ ] Alerts & Thresholds: Trigger notifications if a sensor reading goes above/below a certain level.
- [ ] Edge Computing: Perform partial data processing on the “device” side before sending final metrics.

---

### Websites

- [Cosmos DB](https://azure.microsoft.com/en-us/products/cosmos-db/)
- [Grafana](https://grafana.com/)
- [Azure IoT Hub](https://learn.microsoft.com/en-us/azure/iot-hub/create-hub?tabs=portal)

---

## Project Structure

- **`devices/main.py`** – Main entry point that sets the mode (DEV or PROD) and chooses which device to run based on command-line arguments.
- **`devices/humidity/Humidity.py`** – Implements the default simulated humidity sensor device with support for DEV (print to console) or PROD (send to IoT Hub) modes. Pulls configuration from `humidity_config.yaml`.
- **`devices/humidity/HumidityAggregated.py`** – Implements a simulated humidity sensor device that aggregates data with support for DEV (print to console) or PROD (send to IoT Hub) modes. Pulls configuration from `humidity_config.yaml`.
- **`devices/VibrationDevice.py`** – Example vibrating sensor device that sends alerts when vibration exceeds a threshold.
- **`devices/script.py`** – Demonstrates how to send telemetry data to IoT Hub and store incoming messages in Cosmos DB.
- **`devices/util/load_env.py`** – Loads environment variables and defines helper functions to create IoT Hub connection strings and determine the current mode.
- **`.env`** – Contains your configuration settings (IoT Hub hostname, keys, and device IDs).

---

## Setup

1. **Install Dependencies**

   Make sure you have [Poetry](https://python-poetry.org/) installed. Then run:

   ```sh
   poetry install
   ```

2. **Configure Environment Variables**

   - Copy `.env.example` to `.env` if needed.
   - Edit the `.env` file to provide your Azure IoT Hub hostname, shared access key, and device IDs. For example:

     ```env
     MODE="DEV"
     HOSTNAME="CS496ProjectHub.azure-devices.net"
     SHARED_ACCESS_KEY="your-shared-key"
     HUMIDITY_DEVICE_ID="FirstDevice"
     ```

---

## Running the Code

The project supports two modes (DEV and PROD) and two types of humidity devices. You can choose which device to run by providing an optional command-line argument. In both cases, the default device is the standard humidity sensor, and the alternate option is the aggregated humidity sensor.

### Development Mode

In DEV mode, simulated sensor data is printed to the console rather than sending messages.

- **Default (Humidity Sensor):**

  ```sh
  poetry run dev
  # or explicitly
  poetry run dev humidity
  ```

- **Aggregated Humidity Sensor:**

  ```sh
  poetry run dev aggregated
  ```

### Production Mode

In PROD mode, the device sends telemetry data to Azure IoT Hub. To use PROD mode, update the `MODE` variable in your `.env` file to `"PROD"`. Then run:

- **Default (Humidity Sensor):**

  ```sh
  poetry run prod
  # or explicitly
  poetry run prod humidity
  ```

- **Aggregated Humidity Sensor:**

  ```sh
  poetry run prod aggregated
  ```

---

## Additional Devices & Scripts

- **Vibration Alerts:**  
  Run the [`devices/VibrationDevice.py`](devices/VibrationDevice.py) to simulate a device that sends vibration alerts if readings exceed a threshold.

- **Cosmos DB Integration:**  
  The [`devices/script.py`](devices/script.py) script shows how to send telemetry data to IoT Hub and use the Cosmos DB client to store received messages.

---

## Testing & Visualization

- **Testing:**  
  - Confirm that your simulated devices send data (printed output in DEV mode or messages sent in PROD mode).
  - In a production environment, verify that data appears in your Cosmos DB (or your chosen storage service).

- **Visualization:**  
  - Use dashboards (e.g., Grafana) to visualize the near-real-time sensor data.

---

## Useful Resources

- [Azure IoT Hub](https://learn.microsoft.com/en-us/azure/iot-hub/create-hub?tabs=portal)
- [Cosmos DB](https://azure.microsoft.com/en-us/products/cosmos-db/)
- [Grafana](https://grafana.com/)
```