import sys
import os
from .humidity import HumidityDevice, HumidityAggregatedDevice

def run_with_mode(mode: str, device_type: str = "humidity"):
    os.environ["MODE"] = mode
    
    try: 
        # Choose the device based on the command-line argument.
        if device_type.lower() == "aggregated":
            device = HumidityAggregatedDevice()
        else:  # default to HumidityDevice
            device = HumidityDevice()
    except EnvironmentError as e:
        print(e)
        sys.exit(1)

    try:
        device.send_telemetry()
    except KeyboardInterrupt:
        print("Stopped sending data")
    finally:
        device.shutdown()

def run_dev():
    # Check for an extra command-line argument; default to "humidity"
    device_type = sys.argv[1] if len(sys.argv) > 1 else "humidity"
    if device_type != "aggregated":
        device_type = "humidity"
    run_with_mode("DEV", device_type)

def run_prod():
    device_type = sys.argv[1] if len(sys.argv) > 1 else "humidity"
    if device_type != "aggregated":
        device_type = "humidity"
    run_with_mode("PROD", device_type)

if __name__ == "__main__":
    run_dev()
