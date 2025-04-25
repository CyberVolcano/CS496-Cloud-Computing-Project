from dotenv import load_dotenv
import yaml, os

load_dotenv()

def load_config(config_path="config.yaml"):
    """
    Loads configuration from a YAML file in the same directory as this script.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, config_path)
    try:
        with open(config_file_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file_path}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None

config = load_config()
if not config:
    print("Configuration failed to load.")
    exit(1)

# Load Environment Variables
IOT_HUB_HOSTNAME = os.environ.get("IOT_HUB_NAME") + ".azure-devices.net"
DEVICE_ID = os.environ.get("DEVICE_ID") 
SHARED_ACCESS_KEY = os.environ.get("SHARED_ACCESS_KEY") 

# Device configuration
POSITION = f'{config["device"]["position"]["latitude"]},{config["device"]["position"]["longitude"]}'
USER_AGENT = os.environ.get("WEATHER_USER_AGENT")
BASE_URL = "https://api.weather.gov"
HEADERS = {"User-Agent": USER_AGENT}

if not (IOT_HUB_HOSTNAME and DEVICE_ID and SHARED_ACCESS_KEY and USER_AGENT):
    print("Error: Environment variables for IoT Hub configuration are not set.")
    exit(1)