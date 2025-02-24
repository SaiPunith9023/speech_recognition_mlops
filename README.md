# Voice-Controlled Assistant

This project is a voice-activated assistant that allows users to control applications, perform web searches, and interact with the system using voice commands. It integrates FastAPI, SpeechRecognition, PyAutoGUI, and Gradio to provide a smooth and efficient experience.

---

## Features

- Voice Commands – Execute system commands, open applications, and browse the web.
- FastAPI Backend – A lightweight and efficient API for processing voice commands.
- Logging Server – Stores logs of executed commands for auditing and debugging.
- Gradio UI – A simple web interface for interacting with the assistant.
- Asynchronous Execution – Non-blocking operations for better performance.

---

## Project Structure

```
mlops1/
│── main/
│   ├── api.py             # FastAPI backend for processing requests
│   ├── gui.py             # Gradio-based user interface
│   ├── log_client.py      # Logging server for storing command history
│   ├── browser_control.py
│   ├── main.py
│   ├── logging_config.py
│   ├── hardware_control.py
│   ├── rpa_control.py
│   ├── .py
│   ├── main.py
│   ├── log_server.py      # Logging server for storing command history
│   ├── voice_commands.py  # Handles speech recognition and command execution
│── tests/                 # Unit tests for different components
│── scripts/               # Utility scripts for setup and maintenance
│── requirements.txt       # Project dependencies
│── justfile               # Task automation with Just
│── README.txt             # Project documentation
```

---

## Quick Start

### 1. Setup the Virtual Environment

Install dependencies:
```
uv venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Full System
```
just run
```
This will:
- Start the Logging Server
- Launch the FastAPI Backend
- Open the Gradio UI



---

## Available Commands in `justfile`

The Just task runner is used for automation. Below is the configuration for `justfile`:

```
# .PHONY: setup run log_server api voice lint test

setup:
	uv venv .venv
	source .venv/bin/activate && uv pip install --system -r requirements.txt

run:
	source .venv/bin/activate && \
	python main/log_server.py & sleep 2 && \
	uvicorn main.api:app --host 127.0.0.1 --port 8000 --reload --loop asyncio & sleep 2 && \
	python main/gui.py && wait

```







Made by
GAMPA ABHINAY
BONALA SAI PUNITH

