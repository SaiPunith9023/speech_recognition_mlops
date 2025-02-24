import os
import mss
import pyautogui
import subprocess
from main.voice_control import assistant_voice
from main.log_client import send_log  # Using centralized logging
import re

def take_screenshot():
    try:
        screenshot_path = os.path.join(os.getcwd(), "screenshot.png")
        with mss.mss() as sct:
            sct.shot(output=screenshot_path)
        assistant_voice(f"Screenshot saved at {screenshot_path}")
        send_log("INFO", f"Screenshot saved at {screenshot_path}")
    except Exception as e:
        send_log("EXCEPTION", f"Error taking screenshot: {e}")
        assistant_voice("Failed to take a screenshot.")

def is_caps_lock_on():
    """Check if Caps Lock is ON."""
    try:
        output = subprocess.check_output("xset q", shell=True).decode()
        match = re.search(r"Caps Lock:\s+(\w+)", output)  
        status = match and match.group(1).lower() == "on"
        send_log("INFO", f"Checked Caps Lock status: {'ON' if status else 'OFF'}")
        return status
    except subprocess.CalledProcessError:
        send_log("EXCEPTION", "Error checking Caps Lock status")
        return False 

def toggle_caps_lock():
    try:
        os.system("xdotool key Caps_Lock")
        send_log("INFO", "Caps Lock toggled.")
    except Exception as e:
        send_log("EXCEPTION", f"Error toggling Caps Lock: {e}")
        assistant_voice("Failed to toggle Caps Lock.")

def hardware_control(instruction):
    instruction = instruction.lower()
    send_log("INFO", f"Received hardware command: {instruction}")

    if "caps lock on" in instruction:
        if is_caps_lock_on():
            assistant_voice("Caps Lock is already on.")
            send_log("INFO", "Caps Lock was already on.")
        else:
            toggle_caps_lock()
            assistant_voice("Caps Lock turned on.")
            send_log("INFO", "Caps Lock turned on.")

    elif "caps lock off" in instruction:
        if is_caps_lock_on():
            toggle_caps_lock()
            assistant_voice("Caps Lock turned off.")
            send_log("INFO", "Caps Lock turned off.")
        else:
            assistant_voice("Caps Lock is already off.")
            send_log("INFO", "Caps Lock was already off.")

    elif "move to top left" in instruction:
        pyautogui.moveTo(0, 0)
        assistant_voice("Mouse moved to the top left corner.")
        send_log("INFO", "Mouse moved to the top left corner.")

    elif "take screenshot" in instruction or "take a photo" in instruction:
        take_screenshot()

    elif "full brightness" in instruction:
        os.system("sudo brightnessctl set 100%")
        assistant_voice("Brightness set to 100%.")
        send_log("INFO", "Brightness set to 100%.")

    elif "decrease brightness" in instruction:
        os.system("sudo brightnessctl set 20%")
        assistant_voice("Brightness decreased to 20%.")
        send_log("INFO", "Brightness decreased to 20%.")

    elif instruction.startswith("set_brightness:"):
        try:
            brightness = int(instruction.split(":")[1])
            if 0 <= brightness <= 100:
                os.system(f"sudo brightnessctl set {brightness}%")
                send_log("INFO", f"Brightness set to {brightness}%.")
            else:
                send_log("WARNING", "Invalid brightness level: Out of range.")
        except ValueError:
            send_log("WARNING", "Invalid brightness value received.")


    elif "lock screen" in instruction:
        os.system("xdg-screensaver lock || gnome-screensaver-command -l")
        assistant_voice("Screen locked.")
        send_log("INFO", "Screen locked.")

    else:
        assistant_voice("I did not understand the command.")
        send_log("WARNING", f"Unknown command received: {instruction}")
