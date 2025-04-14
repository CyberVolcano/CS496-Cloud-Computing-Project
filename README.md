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


### HOW TO RUN THE SCRIPT
1. cd into Mosquitto if necessary via and start MQTT broker:
cd "C:\Program Files\mosquitto"
.\mosquitto.exe -v

Subscribing to a topic
2. Open a second terminal simultaneously and run:
cd "C:\Program Files\mosquitto"
.\mosquitto_sub -t "telemetry/device1" -v

3. Open the python script and run the script:
python script.py

Output should look like:
Sent to Azure
Published to Mosquitto topic 'telemetry/device1'

And second terminal should print Mosquitto Telemetry:
telemetry/device1 {"timestamp": "...", "temperature": ..., "humidity": ...}

(OPTIONAL - NEED TO INSTALL CLI to work)
Azure Telemetry messages can be printed in seperate terminal with (BUT HAS NOT BEEN SETUP YET IF DESIRED TOO):
cd "C:\Program Files\mosquitto"
az iot hub monitor-events --hub-name CS496ProjectHub --device-id FirstDevice