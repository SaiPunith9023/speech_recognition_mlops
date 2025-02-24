import zmq
import toml
import time

# Load config
config = toml.load("config.toml")
PORT = config["logging"]["log_server_port"]

# Setup ZeroMQ Client
context = zmq.Context()
socket = context.socket(zmq.PUSH)

# Try to connect with retries
connected = False
for _ in range(5):  # Retry up to 5 times
    try:
        socket.connect(f"tcp://localhost:{PORT}")
        connected = True
        break
    except Exception as e:
        print(f"Failed to connect to log server: {e}. Retrying...")
        time.sleep(2)

if not connected:
    print("Could not connect to log server after multiple attempts.")

def send_log(level, text):
    try:
        message = {"level": level, "text": text}
        socket.send_json(message, zmq.NOBLOCK)  # Non-blocking send
    except zmq.error.Again:
        print("Log server is not responding. Skipping log.")
    except Exception as e:
        print(f"Error sending log: {e}")
