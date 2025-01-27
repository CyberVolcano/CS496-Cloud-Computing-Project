Purpose
This project demonstrates how real or simulated devices (e.g., sensors measuring temperature/humidity) can send data to a central platform for real-time storage, analytics, or dashboarding. It exposes you to event-driven architectures, message brokering (MQTT), and how to set up dashboards for streaming data.
Use Case
•	A greenhouse or small farm environment logging conditions to optimize plant growth.
•	A “smart home” demonstration collecting sensor data (door sensors, temperature, light levels).
•	A robotics club streaming data from multiple bots or drones to a single dashboard.
Difficulty Bonus
3

Basic Rubric (How to Start) - D.L. Assuming we are taking the cloud route.
1.	Messaging Protocol
- [ ] Cloud: Azure IoT Hub free tier.
o	Local: Mosquitto (MQTT broker) installed in a container or on your machine.
2.	Simulated Device Script
- [ ] Python or Node.js program that sends random sensor readings at intervals.
- [ ] Structure the data as JSON (e.g., { "temp": 22.5, "humidity": 60 }).
3.	Data Storage
- [ ] Azure: Use Cosmos DB or Table Storage.
o	Local: Try InfluxDB (time-series) or PostgreSQL.
5.	Visualization
- [ ] Grafana or a custom front-end that queries your DB for the latest readings.
5.	Testing
Confirm your script sends data, see it appear in the DB, and visualize in near real-time on the dashboard.
Extra Credit Opportunity (Optional)
- [ ]	Alerts & Thresholds: Trigger notifications if a sensor reading goes above/below a certain level.
- [ ]	Edge Computing: Perform partial data processing on the “device” side before sending final metrics.
