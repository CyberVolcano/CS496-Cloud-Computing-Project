from dotenv import load_dotenv
from enum import Enum
import os

class Mode(Enum):
    DEV = "DEV"
    PROD = "PROD"

load_dotenv()

HOSTNAME = os.getenv("HOSTNAME")
SHARED_ACCESS_KEY = os.getenv("SHARED_ACCESS_KEY")
# Mode the script should run in
MODE = Mode(os.getenv("MODE", "DEV"))

def create_connection_string(device_env_name: str) -> str:
    """ Creates a connection string to connecto to AzureIot Hub. """
    device_id = os.getenv(device_env_name)
    return f'HostName={HOSTNAME};DeviceId={device_id};SharedAccessKey={SHARED_ACCESS_KEY}'

def is_dev_mode() -> bool:
    """ Returns true if the mode is set to development. """
    return MODE == Mode.DEV

def is_prod_mode() -> bool:
    """ Returns true if the mode is set to production. """
    return MODE == Mode.PROD

if __name__ == '__main__':
    print(create_connection_string("HUMIDITY_DEVICE_ID"))