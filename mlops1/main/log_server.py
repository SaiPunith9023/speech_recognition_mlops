import zmq
import os
import toml
from loguru import logger

# Load configuration from config.toml
config = toml.load("config.toml")
LOG_FILE = config["logging"]["log_file_name"]
LOG_ROTATION = config["logging"]["log_rotation"]
LOG_COMPRESSION = config["logging"]["log_compression"]
PORT = config["logging"]["log_server_port"]

# Ensure logs directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configure Loguru Logging
logger.remove()
logger.add(LOG_FILE, rotation=LOG_ROTATION, compression=LOG_COMPRESSION, level="INFO")

def start_log_server():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind(f"tcp://*:{PORT}")
    logger.info(f"Logging server started on port {PORT}")

    while True:
        try:
            message = socket.recv_json()
            level = message.get("level", "INFO")
            text = message.get("text", "")

            # Log message based on level
            if level == "INFO":
                logger.info(text)
            elif level == "WARNING":
                logger.warning(text)
            elif level == "ERROR":
                logger.error(text)
            elif level == "EXCEPTION":
                logger.exception(text)
        except Exception as e:
            logger.exception(f"Error in log server: {e}")

if __name__ == "__main__":
    start_log_server()
