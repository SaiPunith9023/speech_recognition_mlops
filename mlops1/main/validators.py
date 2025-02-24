from pydantic import BaseModel, ValidationError
import yaml
import toml

# Define the expected structure of config.toml
class ConfigModel(BaseModel):
    logging: dict
    server: dict

# Define the expected structure of commands.yaml
class CommandsModel(BaseModel):
    application_control: dict
    hardware_control: dict
    rpa_control: dict
    
    

def validate_toml():
    """Validates config.toml"""
    try:
        config = toml.load("config.toml")
        ConfigModel(**config)
        print("✅ config.toml is valid")
    except ValidationError as e:
        print(f"❌ config.toml validation error: {e}")

def validate_yaml():
    """Validates commands.yaml"""
    try:
        with open("commands.yaml", "r") as file:
            commands = yaml.safe_load(file)
            CommandsModel(**commands)
            print("✅ commands.yaml is valid")
    except ValidationError as e:
        print(f"❌ commands.yaml validation error: {e}")

# Run validations when script is executed
if __name__ == "__main__":
    validate_toml()
    validate_yaml()



