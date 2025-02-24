import gradio as gr
import requests
import yaml
import os
from voice_control import listen_instruction  # Custom voice module

# Load commands from YAML
yaml_path = os.path.join(os.path.dirname(__file__), "commands.yaml")
try:
    with open(yaml_path, "r") as file:
        commands = yaml.safe_load(file) or {}
except Exception as e:
    commands = {}
    print(f"Error loading commands.yaml: {e}")

# Function to send commands to FastAPI server
def send_command(command):
    response = requests.post(
        "http://127.0.0.1:8000/execute_command/",
        json={"command": command},
    )
    if response.status_code == 200:
        return f"✅ {response.json().get('message', 'Command executed successfully!')}"
    return f"❌ {response.json().get('detail', 'Invalid command')}"

# Function to process voice input
def voice_command():
    command = listen_instruction()
    if not command:
        return "❌ No voice command detected. Try again."
    return send_command(command)

# Predefined buttons categorized
commands_ui = {
    "Application Control": {
        "Open Browser": "open browser",
        "Close Browser": "close browser",
        " Open New Tab": "new tab",
        "Close Tab": "close tab",
        "Refresh Tab": "refresh tab",
    },
    "RPA Control": {
        "Search Google (Python)": "search google for Python",
        "Search Amazon (Laptop)": "amazon search for laptop",
        "Search Jobs (Software Engineer)": "search job for Software Engineer",
        "open Moodle": "login to moodle",
    },
    "Hardware Control": {
        "Set Brightness (50%)": "set brightness to 50",
        "Increase Brightness": "full brightness",
        "Decrease Brightness": "decrease brightness",
        "Lock Screen": "lock screen",
        "Take Screenshot": "take screenshot",
        "Move Mouse (Top Left)": "move to top left",
        "Caps Lock On": "caps lock on",
        "Caps Lock Off": "caps lock off",
    },
}

# Gradio UI
with gr.Blocks() as interface:
    gr.Markdown("🎙 **Voice-Controlled Assistant**\n")
    gr.Markdown("Control applications, RPA, and hardware using voice or buttons\n")

    with gr.Row():
        textbox = gr.Textbox(label="🔹 Enter Command (or use voice input)")
        submit_btn = gr.Button("🚀 Submit", variant="primary")
        voice_btn = gr.Button("🎤 Speak")

    output = gr.Textbox(label="🔹 Response", interactive=False)

    # Event handlers
    submit_btn.click(send_command, inputs=textbox, outputs=output)
    voice_btn.click(voice_command, inputs=[], outputs=output)

    gr.Markdown("---")  # Separator

    # Add buttons for all commands under their categories
    for category, cmds in commands_ui.items():
        gr.Markdown(f"### 🔹 {category}")
        with gr.Row():
            for label, command in cmds.items():
                btn = gr.Button(label)
                btn.click(send_command, inputs=[gr.Textbox(value=command, visible=False)], outputs=output)

interface.launch()
