import uvicorn
from fastapi import FastAPI
import yaml
import os
import toml
from main.api import app  # Import FastAPI app
from main.log_client import send_log  # Use centralized logging

# Load configuration from TOML file
config = toml.load("config.toml")
LOG_SERVER_PORT = config["logging"]["log_server_port"]

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Load commands from YAML file
with open("commands.yaml", "r") as file:
    commands = yaml.safe_load(file)

app_main = FastAPI()

# Include the routes from api.py
app_main.mount("/", app)

# Expose an endpoint to check available commands
@app_main.get("/commands")
async def get_commands():
    send_log("INFO", "Commands list accessed.")
    return {"available_commands": commands}

if __name__ == "__main__":
    send_log("INFO", "Starting FastAPI server.")
    uvicorn.run("main:app_main", host="127.0.0.1", port=8000, reload=True)
