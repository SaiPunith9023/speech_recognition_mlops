# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from main.browser_control import BrowserController
# from main.rpa_control import RPAController  # New RPA module
# from main.hardware_control import hardware_control
# from main.log_client import send_log  # Use centralized logging

# app = FastAPI()
# browser_controller = BrowserController()
# rpa_controller = RPAController()  # RPA controller instance

# class CommandRequest(BaseModel):
#     command: str

# @app.get("/")
# async def root():
#     send_log("INFO", "API is running successfully")
#     return {"message": "API is running successfully"}

# # Browser Control Endpoints
# @app.post("/browser_control/")
# async def browser_control(request: CommandRequest):
#     command = request.command.lower()
#     send_log("INFO", f"Received browser command: {command}")

#     if command == "open browser":
#         if browser_controller.is_browser_open():
#             send_log("WARNING", "Attempted to open browser, but it is already open.")
#             raise HTTPException(status_code=400, detail="Browser is already open")
#         await browser_controller.open_browser()
#         send_log("INFO", "Browser opened successfully.")
#         return {"message": "Browser opened successfully"}

#     elif command == "new tab":
#         if not browser_controller.is_browser_open():
#             send_log("ERROR", "Cannot open a new tab: Browser is not open")
#             raise HTTPException(status_code=400, detail="Cannot open a new tab: Browser is not open")
#         await browser_controller.new_tab()
#         send_log("INFO", "New tab opened successfully.")
#         return {"message": "New tab opened successfully"}

#     elif command == "refresh tab":
#         if not browser_controller.is_browser_open():
#             send_log("ERROR", "Cannot refresh: Browser is not open")
#             raise HTTPException(status_code=400, detail="Cannot refresh: Browser is not open")
#         if not browser_controller.is_tab_open():
#             send_log("ERROR", "Cannot refresh: No active tab")
#             raise HTTPException(status_code=400, detail="Cannot refresh: No active tab")
#         await browser_controller.refresh_tab()
#         send_log("INFO", "Tab refreshed successfully.")
#         return {"message": "Tab refreshed successfully"}

#     elif command == "close tab":
#         if not browser_controller.is_browser_open():
#             send_log("ERROR", "Cannot close tab: Browser is not open")
#             raise HTTPException(status_code=400, detail="Cannot close tab: Browser is not open")
#         if not browser_controller.is_tab_open():
#             send_log("ERROR", "Cannot close tab: No active tab")
#             raise HTTPException(status_code=400, detail="Cannot close tab: No active tab")
#         await browser_controller.close_tab()
#         send_log("INFO", "Tab closed successfully.")
#         return {"message": "Tab closed successfully"}

#     elif command == "close browser":
#         if not browser_controller.is_browser_open():
#             send_log("ERROR", "Cannot close browser: Browser is not open")
#             raise HTTPException(status_code=400, detail="Cannot close browser: Browser is not open")
#         await browser_controller.close_browser()
#         send_log("INFO", "Browser closed successfully.")
#         return {"message": "Browser closed successfully"}

#     else:
#         send_log("WARNING", f"Invalid browser command received: {command}")
#         raise HTTPException(status_code=400, detail="Invalid command. Use one of: 'open browser', 'new tab', 'refresh tab', 'close tab', 'close browser'.")

# # RPA Control Endpoints
# @app.post("/rpa_control/")
# async def rpa_control(request: CommandRequest):
#     command = request.command.lower()
#     send_log("INFO", f"Received RPA command: {command}")

#     if command.startswith("search google for"):
#         query = command.replace("search google for", "").strip()
#         results = await rpa_controller.search_google(query)
#         send_log("INFO", f"Google search executed for: {query}")
#         return {"message": f"Google search results for '{query}'", "results": results}

#     elif command == "login to moodle":
#         await rpa_controller.login_moodle()
#         send_log("INFO", "Moodle opened successfully.")
#         return {"message": "Moodle opened"}

#     elif command.startswith("search job for"):
#         job_query = command.replace("search job for", "").strip()
#         results = await rpa_controller.search_jobs(job_query)
#         send_log("INFO", f"Job search executed for: {job_query}")
#         return {"message": f"Job search results for '{job_query}'", "results": results}

#     elif command.startswith("amazon search for"):
#         product = command.replace("amazon search for", "").strip()
#         await rpa_controller.search_amazon(product)
#         send_log("INFO", f"Amazon search started for: {product}")
#         return {"message": f"Amazon search started for '{product}'"}

#     elif command == "close browser":
#         if not rpa_controller.is_browser_open():
#             send_log("ERROR", "Attempted to close RPA browser, but it is not open.")
#             raise HTTPException(status_code=400, detail="Browser is not open")
#         await rpa_controller.close_browser()
#         send_log("INFO", "RPA Browser closed successfully.")
#         return {"message": "Browser closed successfully"}

#     else:
#         send_log("WARNING", f"Invalid RPA command received: {command}")
#         raise HTTPException(status_code=400, detail="Invalid RPA command.")

# # Hardware Control Endpoint
# @app.post("/hardware_control/")
# async def hardware_control_api(request: CommandRequest):
#     send_log("INFO", f"Received hardware command: {request.command}")
#     try:
#         hardware_control(request.command)
#         send_log("INFO", f"Executed hardware command: {request.command}")
#         return {"status": "success", "command": request.command}
#     except Exception as e:
#         send_log("EXCEPTION", f"Error in hardware_control: {e}")
#         raise HTTPException(status_code=500, detail=f"Hardware Control Error: {str(e)}")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main.browser_control import BrowserController
from main.rpa_control import RPAController  # RPA module
from main.hardware_control import hardware_control
from main.log_client import send_log  # Centralized logging
import yaml

app = FastAPI()
browser_controller = BrowserController()
rpa_controller = RPAController()

# Load commands from YAML file
try:
    with open("commands.yaml", "r") as file:
        commands = yaml.safe_load(file)
        if not commands:
            raise ValueError("commands.yaml is empty!")
except (FileNotFoundError, yaml.YAMLError, ValueError) as e:
    send_log("ERROR", f"Failed to load commands.yaml: {e}")
    commands = {}

# Pydantic model for command requests
class CommandRequest(BaseModel):
    command: str

@app.get("/")
async def root():
    send_log("INFO", "API is running successfully")
    return {"message": "API is running successfully"}

@app.get("/commands")
async def get_commands():
    send_log("INFO", "Commands list accessed.")
    return {"available_commands": commands}

@app.post("/execute_command/")
async def execute_command(request: CommandRequest):
    command = request.command.lower()
    send_log("INFO", f"Received command: {command}")

    category, action = get_command_category(command)

    if category and action:
        send_log("INFO", f"Executing {action} under {category}")

        if category == "application_control":
            return await execute_application_control(action)
        elif category == "hardware_control":
            return execute_hardware_control(action,command)
        elif category == "rpa_control":
            return await execute_rpa_control(action, command)  # Pass full command string

    send_log("WARNING", f"Invalid command received: {command}")
    raise HTTPException(status_code=400, detail="Invalid command")


# Function to get category & action from YAML
def get_command_category(command: str):
    """Finds the category and action of a command from commands.yaml"""
    send_log("DEBUG", f"Checking command category for: {command}")

    for category, actions in commands.items():
        for action, phrases in actions.items():
            for phrase in phrases:  # Iterate over the list of valid phrases
                if command.startswith(phrase):  # Check if command starts with the phrase
                    send_log("INFO", f"Matched command '{command}' to category '{category}', action '{action}'")
                    return category, action

    send_log("WARNING", f"Command '{command}' not recognized in commands.yaml")
    return None, None  # Return None if no match is found


# Function to handle browser-related commands
async def execute_application_control(action):
    if action == "open_browser":
        if browser_controller.is_browser_open():
            raise HTTPException(status_code=400, detail="Browser is already open")
        await browser_controller.open_browser()
        return {"message": "Browser opened successfully"}

    elif action == "close_browser":
        if not browser_controller.is_browser_open():
            raise HTTPException(status_code=400, detail="Browser is not open")
        await browser_controller.close_browser()
        return {"message": "Browser closed successfully"}

    elif action == "open_new_tab":
        if not browser_controller.is_browser_open():
            raise HTTPException(status_code=400, detail="Cannot open new tab: Browser is not open")
        await browser_controller.new_tab()
        return {"message": "New tab opened successfully"}

    elif action == "close_tab":
        if not browser_controller.is_browser_open():
            raise HTTPException(status_code=400, detail="Cannot close tab: Browser is not open")
        if not browser_controller.is_tab_open():
            raise HTTPException(status_code=400, detail="Cannot close tab: No active tab")
        await browser_controller.close_tab()
        return {"message": "Tab closed successfully"}

    elif action == "refresh_tab":
        if not browser_controller.is_browser_open():
            raise HTTPException(status_code=400, detail="Cannot refresh: Browser is not open")
        if not browser_controller.is_tab_open():
            raise HTTPException(status_code=400, detail="Cannot refresh: No active tab")
        await browser_controller.refresh_tab()
        return {"message": "Tab refreshed successfully"}

# Hardware control functions
def execute_hardware_control(action, command):
    if action == "set_brightness":
        import re
        match = re.search(r"set brightness to (\d+)", command)
        if match:
            brightness = int(match.group(1))
            if 0 <= brightness <= 100:
                hardware_control(f"set_brightness:{brightness}")
                return {"message": f"Brightness set to {brightness}%"}
            else:
                raise HTTPException(status_code=400, detail="Brightness out of range")
    
    actions_map = {
        "caps_lock_on": "caps lock on",
        "caps_lock_off": "caps lock off",
        "take_screenshot": "take screenshot",
        "move_mouse": "move to top left",
        "full_brightness": "full brightness",
        "decrease_brightness": "decrease brightness",
        "lock_screen": "lock screen"
    }
    
    if action in actions_map:
        hardware_control(actions_map[action])
        return {"message": f"{action.replace('_', ' ').title()} executed"}
    
    raise HTTPException(status_code=400, detail="Invalid hardware control action")



async def execute_rpa_control(action, full_command):
    send_log("INFO", f"Executing RPA action: {action}")

    if action == "search_google":
        query = full_command.replace("search google for", "").strip()
        if not query:
            send_log("ERROR", "Google search query is empty")
            return {"error": "Invalid Google search query"}
        send_log("INFO", f"Searching Google for: {query}")
        return await rpa_controller.search_google(query)

    elif action == "login_moodle":
        send_log("INFO", "Logging into Moodle")
        return await rpa_controller.login_moodle()

    elif action == "search_job":
        query = full_command.replace("search job for", "").strip()
        if not query:
            send_log("ERROR", "Job search query is empty")
            return {"error": "Invalid job search query"}
        send_log("INFO", f"Searching jobs for: {query}")
        return await rpa_controller.search_jobs(query)

    elif action == "amazon_search":
        query = full_command.replace("amazon search for", "").strip()
        if not query:
            send_log("ERROR", "Amazon search query is empty")
            return {"error": "Invalid Amazon search query"}
        send_log("INFO", f"Searching Amazon for: {query}")
        return await rpa_controller.search_amazon(query)

    elif action == "weather_update":
        send_log("INFO", "Fetching weather updates")
        return {"message": "Fetching weather updates..."}  

    send_log("WARNING", f"Unknown RPA action: {action}")
    return {"error": "Invalid RPA action"}




