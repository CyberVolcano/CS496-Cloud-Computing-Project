# Azure IoT Hub Device Simulator

A Python-based simulator for IoT devices that sends telemetry data to Azure IoT Hub.

## Prerequisites

### Install Python Poetry

1. **Windows (PowerShell)**
   ```powershell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   ```

2. **Add Poetry to your PATH**
   - Poetry is installed at `%APPDATA%\Python\Scripts\poetry`
   - Add this path to your system's PATH environment variable
   - Verify installation:
     ```powershell
     poetry --version
     ```

## Project Structure

- **`devices/main.py`** – Main entry point that sets the mode (DEV or PROD) and chooses which device to run based on command-line arguments
- **`devices/humidity/`** – Humidity sensor implementations:
  - `Humidity.py` – Basic humidity sensor with DEV/PROD modes
  - `HumidityAggregated.py` – Aggregated humidity sensor with statistical data
  - `humidity_config.yaml` – Sensor configuration file
- **`devices/VibrationDevice.py`** – Example vibrating sensor with threshold alerts
- **`devices/util/load_env.py`** – Environment configuration and connection management
- **`.env`** – Local configuration settings (not in git)

## Setup

1. **Install Project Dependencies**
   ```powershell
   poetry install
   ```

2. **Configure Environment**
   ```powershell
   copy .env.example .env
   ```

   Edit `.env` with your Azure IoT Hub details:
   ```env
   MODE="DEV"                     # DEV or PROD
   HOSTNAME="<your-hub>.azure-devices.net"
   SHARED_ACCESS_KEY="<your-key>"
   HUMIDITY_DEVICE_ID="<device-id>"
   ```

## Running Devices

### Development Mode
Prints simulated data to console:

```powershell
# Run basic humidity sensor
poetry run dev
# or
poetry run dev humidity

# Run aggregated humidity sensor
poetry run dev aggregated
```

### Production Mode
Sends real telemetry to Azure IoT Hub:

```powershell
# Run basic humidity sensor
poetry run prod
# or
poetry run prod humidity

# Run aggregated humidity sensor
poetry run prod aggregated
```

## Device Configuration

### Humidity Sensor (`humidity_config.yaml`)
```yaml
device:
  sampling:
    interval: 5            # Seconds between readings
    aggregation_count: 5   # Readings to aggregate (aggregated device only)
  sensors:
    temperature:
      min: 20.0
      max: 30.0
      decimal_places: 2
    humidity:
      min: 20.0
      max: 30.0
      decimal_places: 2
```

## Error Handling

The system provides clear error messages for:
- Missing .env file
- Missing environment variables
- Invalid configuration
- Connection issues

Example error:
```
❌ Error: Missing required environment variables

The following variables must be set in your .env file:

• HOSTNAME
  Description: Your Azure IoT Hub hostname

• SHARED_ACCESS_KEY
  Description: Your Azure IoT Hub shared access key

Please check your .env file and add the missing values.
```

## Additional Features

- **Vibration Alerts:**  
  Run `devices/VibrationDevice.py` for threshold-based alerts

- **Data Storage:**  
  `devices/script.py` demonstrates Cosmos DB integration

## Testing & Visualization

- Verify data output in DEV mode
- Monitor IoT Hub messages in PROD mode
- Use Azure Monitor or Grafana for data visualization

## Resources

- [Azure IoT Hub Documentation](https://learn.microsoft.com/en-us/azure/iot-hub/)
- [Python Azure IoT SDK](https://github.com/Azure/azure-iot-sdk-python)
- [Poetry Documentation](https://python-poetry.org/docs/)