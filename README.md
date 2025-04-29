# CS496 Cloud Computing Project - Simulated IoT Device

## Overview

This project simulates an IoT device that collects weather data and sends it to Azure IoT Hub. The device fetches weather information from the National Weather Service API, performs some basic data processing, and then publishes the data to an Azure IoT Hub using the MQTT protocol.

## Project Structure

The project is structured as follows:

*   `.`: Root directory containing project-level files.
    *   `.env`: Stores environment-specific variables (API keys, device credentials).  **Note:** This file should not be committed to version control.  Use `.env.example` as a template.
    *   `.env.example`:  A template for the `.env` file, showing the required environment variables.
    *   `.gitignore`: Specifies intentionally untracked files that Git should ignore.
    *   `Dockerfile`:  Used to build a Docker image for the project.
    *   `README.md`: Project documentation (this file).
    *   `requirements.txt`: Lists the Python packages required to run the project.
*   `SimulatedDevice`: Contains the Python scripts for the simulated device.
    *   `config.py`: Loads configuration settings from `config.yaml` and environment variables.
    *   `config.yaml`: Contains device-specific configuration (e.g., location, send interval).
    *   `device.py`: The main script that simulates the IoT device, fetches weather data, and sends it to Azure IoT Hub.
    *   `utils.py`: Contains utility functions, such as the `make_sas` function for generating SAS tokens.
    *   `weather.py`: Fetches weather data from the National Weather Service API.

## Key Components

### 1. `device.py` ([`SimulatedDevice/device.py`](SimulatedDevice/device.py))

This is the main script that simulates the IoT device. It performs the following actions:

*   Connects to Azure IoT Hub using MQTT.
*   Fetches weather data using the `weather.py` module.
*   Optionally processes the weather data (simulating edge computing).
*   Publishes the data to Azure IoT Hub.
*   Handles connection, disconnection, and publishing events.

### 2. `weather.py` ([`SimulatedDevice/weather.py`](SimulatedDevice/weather.py))

This module is responsible for fetching weather data from the National Weather Service API. It uses the `requests` library to make HTTP requests and extracts relevant information from the API response.  It uses the `POSITION`, `HEADERS`, and `BASE_URL` variables defined in [`SimulatedDevice/config.py`](SimulatedDevice/config.py).

### 3. `config.py` ([`SimulatedDevice/config.py`](SimulatedDevice/config.py))

This module loads configuration settings from two sources:

*   `config.yaml`:  A YAML file containing device-specific settings like location coordinates and the data sending interval.
*   Environment variables: Stores sensitive information like IoT Hub credentials and API keys.  Environment variables are loaded from the `.env` file using the `python-dotenv` library.

### 4. `utils.py` ([`SimulatedDevice/utils.py`](SimulatedDevice/utils.py))

This module provides utility functions used in the project. Currently, it only contains the `make_sas` function, which generates Shared Access Signature (SAS) tokens for authenticating with Azure IoT Hub.

## Setup and Installation

1.  **Clone the repository:**

2.  **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**

    ```bash
    .venv\Scripts\activate  # Windows
    source .venv/bin/activate # Linux or macOS
    ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure environment variables:**

    *   Create a `.env` file in the root directory.  Use `.env.example` as a template.
    *   Set the following environment variables:
        *   `IOT_HUB_NAME`: The name of your Azure IoT Hub.
        *   `DEVICE_ID`: The ID of your simulated device.
        *   `SHARED_ACCESS_KEY`: The shared access key for your device.
        *   `WEATHER_USER_AGENT`: A user agent string for the weather API.

6.  **Configure device settings:**

    *   Modify the `SimulatedDevice/config.yaml` file to set the device's location (latitude and longitude) and the data sending interval.

## Running the Simulation

To run the simulated device, execute the following command from the project root directory:

```bash
python SimulatedDevice/device.py
```

This will start the device, which will connect to Azure IoT Hub, fetch weather data, and send it to the hub at the specified interval.

## Docker

A Dockerfile is provided to containerize the application.

1.  **Build the Docker image:**

    ```bash
    docker build -t simulated-device .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run --env-file .env -d --name simulated-device-container simulated-device
    ```

    **Note:** Ensure `.env` file is properly formated or use `-e` flag for environment variables.

## Edge Computing Simulation

The device.py script includes a `process_weather_data` function that simulates edge computing. This function performs basic data processing on the weather data before sending it to Azure IoT Hub. The function calculates wind speed in mph, dew point, and "feels like" temperature. To enable this, the `run_device` function should be adjusted to call `process_weather_data` before publishing to the IoT Hub.