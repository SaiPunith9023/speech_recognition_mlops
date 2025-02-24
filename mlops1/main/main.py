import uvicorn
from fastapi import FastAPI, HTTPException
import yaml
import os
import toml
from main.api import app  # Import FastAPI app
from main.log_client import send_log  # Use centralized logging

# Load configuration from TOML file
config = toml.load("config.toml")

# Extract server settings
HOST = config["server"]["host"]
PORT = config["server"]["port_no"]
WORKERS = config["server"]["number_of_workers"]
TIMEOUT_KEEP_ALIVE = config["server"]["timeout_keep_alive"]

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Load commands from YAML file with error handling
try:
    with open("commands.yaml", "r") as file:
        commands = yaml.safe_load(file)
        if not commands:
            raise ValueError("commands.yaml is empty!")
except (FileNotFoundError, yaml.YAMLError, ValueError) as e:
    send_log("ERROR", f"Failed to load commands.yaml: {e}")
    commands = {}

app_main = FastAPI()

# Include the routes from api.py
app_main.mount("/", app)

# Expose an endpoint to check available commands
@app_main.get("/commands")
async def get_commands():
    send_log("INFO", "Commands list accessed.")
    return {"available_commands": commands}

# Function to dynamically process commands
@app_main.post("/execute_command/")
async def execute_command(command: str):
    """Processes user commands dynamically from commands.yaml"""
    send_log("INFO", f"Received command: {command}")

    category, action = get_command_category(command)
    
    if category and action:
        send_log("INFO", f"Executing {action} under {category}")

        # Here, you should call the appropriate function based on category/action
        # Example:
        if category == "application_control":
            return {"message": f"Executed application control: {action}"}
        elif category == "hardware_control":
            return {"message": f"Executed hardware control: {action}"}
        elif category == "rpa_control":
            return {"message": f"Executed RPA control: {action}"}

    # If no match found
    send_log("WARNING", f"Invalid command received: {command}")
    raise HTTPException(status_code=400, detail="Invalid command")

# Function to find command category from YAML
def get_command_category(command: str):
    """Finds the category and action of a command from commands.yaml"""
    for category, actions in commands.items():
        for action, phrases in actions.items():
            if command in phrases:
                return category, action
    return None, None

if __name__ == "__main__":
    send_log("INFO", "Starting FastAPI server.")
    uvicorn.run(
        "main:app_main",
        host=HOST,
        port=PORT,
        workers=WORKERS,
        timeout_keep_alive=TIMEOUT_KEEP_ALIVE,
        reload=True
    )
