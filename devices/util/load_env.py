from dotenv import load_dotenv
from enum import Enum
from pathlib import Path
import os
import sys

class Mode(Enum):
    DEV = "DEV"
    PROD = "PROD"

def check_env_file():
    """Check if .env file exists and provide helpful guidance"""
    env_path = Path('.env')

    if not env_path.is_file():        
        error_message = [
            "\n❌ Error: Missing .env configuration file",
            "\nTo fix this:",
            "1. Copy .env.example to .env:",
            "   `cp .env.example .env`" if sys.platform != "win32" else "   `copy .env.example .env`",
            "2. Edit .env with your Azure IoT Hub credentials:",
            "   - HOSTNAME",
            "   - SHARED_ACCESS_KEY",
            "   - Device IDs\n"
        ]
        raise EnvironmentError('\n'.join(error_message))

def check_required_variables():
    """Verify all required environment variables are set"""
    required_vars = {
        "HOSTNAME": "Your Azure IoT Hub hostname (e.g., your-hub.azure-devices.net)",
        "SHARED_ACCESS_KEY": "Your Azure IoT Hub shared access key"
    }
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        error_message = [
            "\n❌ Error: Missing required environment variables",
            "\nThe following variables must be set in your .env file:"
        ]
        
        for var in missing_vars:
            error_message.append(f"\n• {var}")
            error_message.append(f"  Description: {required_vars[var]}")
        
        error_message.append("\nPlease check your .env file and add the missing values.\n")
        raise EnvironmentError('\n'.join(error_message))

try:
    # Check .env file existence before loading
    check_env_file()
    load_dotenv()
    # Verify required variables after loading
    check_required_variables()

    HOSTNAME = os.getenv("HOSTNAME")
    SHARED_ACCESS_KEY = os.getenv("SHARED_ACCESS_KEY")
    # Mode the script should run in
    MODE = Mode(os.getenv("MODE", "DEV"))

except EnvironmentError as e:
    print(e)
    sys.exit(1)

def create_connection_string(device_env_name: str) -> str:
    """Creates a connection string to connect to Azure IoT Hub"""
    device_id = os.getenv(device_env_name)
    if not device_id:
        raise EnvironmentError(
            f"\n❌ Error: Missing device ID environment variable"
            f"\n\nThe environment variable '{device_env_name}' is not set in your .env file."
            f"\nPlease add it with your device ID from Azure IoT Hub.\n"
        )
    return f'HostName={HOSTNAME};DeviceId={device_id};SharedAccessKey={SHARED_ACCESS_KEY}'

def is_dev_mode() -> bool:
    """Returns true if the mode is set to development"""
    return MODE == Mode.DEV

def is_prod_mode() -> bool:
    """Returns true if the mode is set to production"""
    return MODE == Mode.PROD

if __name__ == '__main__':
    print(create_connection_string("HUMIDITY_DEVICE_ID"))