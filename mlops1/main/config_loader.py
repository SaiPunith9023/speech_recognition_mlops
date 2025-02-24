import toml
import yaml
from pydantic import BaseModel, ValidationError

class LoggingConfig(BaseModel):
    log_file_name: str
    log_rotation: str
    log_compression: str
    min_log_level: str
    logging_server_port_no: int

class ServerConfig(BaseModel):
    port_no: int
    number_of_workers: int
    timeout_keep_alive: int

class Config(BaseModel):
    logging: LoggingConfig
    server: ServerConfig  

def load_toml_config():
    try:
        with open("config/config.toml", "r") as file:
            config_data = toml.load(file)
        return Config(**config_data)
    except (FileNotFoundError, ValidationError) as e:
        print(f"❌ Error loading TOML config: {e}")
        return None

def load_yaml_commands():
    try:
        with open("config/commands.yaml", "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("❌ Error: commands.yaml file not found.")
        return {}

config = load_toml_config()
commands = load_yaml_commands()
