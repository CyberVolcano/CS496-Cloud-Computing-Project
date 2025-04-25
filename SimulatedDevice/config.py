import yaml, os

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

POSITION = f'{config["device"]["weather"]["position"]["latitude"]},{config["device"]["weather"]["position"]["longitude"]}'
USER_AGENT = config["device"]["weather"]["user_agent"]