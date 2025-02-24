import zmq
from loguru import logger
from config_loader import config

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect(f"tcp://127.0.0.1:{config.logging.logging_server_port_no}")

class ZMQLogHandler:
    def write(self, message):
        if message.strip():
            socket.send_json({"log": message.strip()})

logger.remove()
logger.add(ZMQLogHandler(), format="{time} {level} {message}")
logger.add(config.logging.log_file_name, rotation=config.logging.log_rotation, compression=config.logging.log_compression, level=config.logging.min_log_level)

logger.info("Logging system initialized and sending logs via ZeroMQ")
