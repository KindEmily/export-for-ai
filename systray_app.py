# File: systray_app.py
import threading
import webbrowser
import sys
import os
import json
import shutil
import logging
import time
import requests
import traceback
import subprocess # Added for shell commands

import pystray
from PIL import Image, ImageDraw
from pynput import keyboard
import uvicorn

import app_main
from web_ui import app

# --- Global Variables ---
server_instance = None
server_thread = None
icon = None
UI_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "ui_config.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "systray_crash.log")
BASE_URL = "http://127.0.0.1:8000"
AUTOSTART_VBS_FILENAME = "launch_export_for_ai.vbs"

# --- Setup ---
def setup_logging():
    """Sets up basic logging to the console."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_crash(exc_info):
    """Logs a fatal exception to a file."""
    with open(LOG_FILE, "w") as f:
        f.write("--- SYSTRAY APPLICATION CRASHED ---\n")
        f.write(f"Time: {time.ctime()}\n")
        f.write("".join(traceback.format_exception(*exc_info)))

# --- Icon and Server Functions ---
def get_icon_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'assets', 'icon.png')
    return os.path.join('assets', 'icon.png')

def create_icon_image():
    try:
        return Image.open(get_icon_path())
    except FileNotFoundError:
        logging.warning("assets/icon.png not found. Creating a placeholder icon.")
        width = 64
        height = 64
        color1 = "#4f46e5" 
        color2 = "#ffffff"
        image = Image.new("RGB", (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle([(width // 4, height // 4), (width * 3 // 4, height * 3 // 4)], fill=color2)
        return image

def is_server_running():
    """Checks if the web server is running and accessible."""
    try:
        response = requests.get(f"{BASE_URL}/api/config", timeout=1)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def start_web_server():
    global server_instance, server_thread
    if server_thread and server_thread.is_alive():
        logging.info("Server is already running.")
        return

    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="warning")
    server_instance = uvicorn.Server(config)
    
    def run_server():
        try:
            server_instance.run()
        except OSError as e:
            logging.error(f"Failed to start server, port might be in use: {e}")
            if icon:
                icon.notify("Could not start Web UI: Port 8000 is likely in use.", "Error")
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    logging.info("Web server started. Giving it a moment to initialize...")
    time.sleep(2)

# --- UI and Export Functions ---
def open_ui():
    logging.info("UI requested. Checking server status...")
    if not is_server_running():
        logging.info("Server not running. Starting it now.")
        start_web_server()
    
    if is_server_running():
        logging.info("Opening UI in browser.")
        webbrowser.open(BASE_URL)
        if icon:
            icon.visible = True
    else:
        logging.error("Failed to start or connect to the server. Cannot open UI.")
        if icon:
            icon.notify("Failed to start Web UI. See console for details.", "Error")

def run_export_and_open_folder():
    # This function remains the same as before
    logging.info("--- Starting Export via Hotkey ---")
    if icon:
        icon.notify('Export process started...', 'Export for AI')

    try:
        with open(UI_CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except Exception as e:
        logging.error(f"Could not read ui_config.json: {e}")
        if icon:
            icon.notify(f'Error reading config: {e}', 'Export Failed')
        return

    export_destination = config.get("export_destination")
    repositories = config.get("repositories", [])
    assets_to_copy = config.get("assets_to_copy", [])

    if not export_destination or not os.path.isdir(export_destination):
        error_msg = f"Export destination '{export_destination}' is not a valid directory."
        logging.error(error_msg)
        if icon:
            icon.notify(error_msg, 'Export Failed')
        return

    app_main.setup_logging()
    for repo_path in repositories:
        logging.info(f"Processing repository: {repo_path}")
        md_file_path = app_main.process_single_repository(repo_path)
        if md_file_path:
            try:
                shutil.copy(md_file_path, export_destination)
                logging.info(f"  -> Copied '{os.path.basename(md_file_path)}' to destination.")
                shutil.rmtree(os.path.dirname(md_file_path))
            except Exception as e:
                logging.error(f"Failed to copy or clean up for '{repo_path}': {e}")

    for asset_path in assets_to_copy:
        logging.info(f"Copying asset: {asset_path}")
        try:
            dest_name = os.path.basename(asset_path)
            destination_path = os.path.join(export_destination, dest_name)
            if os.path.isdir(asset_path):
                shutil.copytree(asset_path, destination_path, dirs_exist_ok=True)
            else:
                shutil.copy2(asset_path, destination_path)
            logging.info(f"  -> Copied '{dest_name}'.")
        except Exception as e:
            logging.error(f"Failed to copy asset '{asset_path}': {e}")

    logging.info(f"--- Export complete. Opening folder: {export_destination} ---")
    if icon:
        icon.notify('Export complete! Opening destination folder.', 'Export for AI')
    webbrowser.open(os.path.realpath(export_destination))


def on_export_activate():
    logging.info("Export hotkey activated. Starting process in background...")
    export_thread = threading.Thread(target=run_export_and_open_folder)
    export_thread.daemon = True
    export_thread.start()

def on_quit(icon_instance, item):
    logging.info("Quit command received. Shutting down.")
    if server_instance:
        server_instance.should_exit = True
    if server_thread and server_thread.is_alive():
        logging.info("Waiting for server thread to close...")
        server_thread.join(timeout=3)
    icon_instance.stop()
    sys.exit(0)

# --- Auto-start Functionality ---
def get_startup_folder() -> Optional[str]:
    """Returns the path to the Windows Startup folder."""
    # This environment variable is typical for Windows Startup folder
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    if os.path.isdir(startup_path):
        return startup_path
    logging.error(f"Windows Startup folder not found: {startup_path}")
    return None

def toggle_autostart(icon_instance: pystray.Icon, item: pystray.MenuItem) -> None:
    """Toggles the application's auto-start setting."""
    startup_folder = get_startup_folder()
    if not startup_folder:
        icon_instance.notify("Failed to find Windows Startup folder.", "Auto-start Error")
        return

    vbs_path = os.path.join(startup_folder, AUTOSTART_VBS_FILENAME)
    
    if os.path.exists(vbs_path):
        # Auto-start is currently enabled, so disable it
        try:
            os.remove(vbs_path)
            logging.info("Auto-start disabled.")
            icon_instance.notify("Auto-start disabled for Export for AI.", "Settings Updated")
        except OSError as e:
            logging.error(f"Error disabling auto-start: {e}")
            icon_instance.notify(f"Failed to disable auto-start: {e}", "Auto-start Error")
    else:
        # Auto-start is currently disabled, so enable it
        try:
            app_exe_path = sys.executable
            # VBScript to launch pythonw.exe (for .py) or the .exe silently
            # If running as .py, sys.executable is python.exe or pythonw.exe
            # If running as bundled .exe, sys.executable is the .exe itself
            # We want to ensure it runs without a console window.
            # For bundled executables, they usually run silently by default if built as a windowed app.
            # For .py, use 'pythonw.exe' for silent execution.
            
            # Check if sys.executable points to python.exe (meaning it's run as a script)
            # Or if it's already a .exe and we want to ensure it's hidden.
            if sys.executable.endswith("python.exe"):
                # Running as a script, use pythonw.exe
                target_exe = sys.executable.replace("python.exe", "pythonw.exe")
                if not os.path.exists(target_exe):
                    logging.warning(f"pythonw.exe not found at {target_exe}, attempting with python.exe. Console may appear.")
                    target_exe = sys.executable
            else:
                # Assume it's a packaged .exe or a script launched directly via pythonw.exe
                target_exe = sys.executable

            vbs_content = f"""
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{target_exe}" & chr(34), 0, false
Set WshShell = Nothing
"""
            with open(vbs_path, "w") as f:
                f.write(vbs_content)
            logging.info("Auto-start enabled.")
            icon_instance.notify("Auto-start enabled for Export for AI.", "Settings Updated")
        except Exception as e:
            logging.error(f"Error enabling auto-start: {e}")
            icon_instance.notify(f"Failed to enable auto-start: {e}", "Auto-start Error")
    
    # Update the menu item text to reflect the current state
    update_autostart_menu_item()


def update_autostart_menu_item():
    """Updates the 'Toggle Autostart' menu item text based on current status."""
    global icon
    if not icon:
        return
    
    startup_folder = get_startup_folder()
    if not startup_folder:
        return

    vbs_path = os.path.join(startup_folder, AUTOSTART_VBS_FILENAME)
    
    autostart_enabled = os.path.exists(vbs_path)
    
    # Find and update the specific menu item
    new_menu_items = []
    found = False
    for item in icon.menu:
        if isinstance(item, pystray.MenuItem) and item.text.startswith("Toggle Auto-start"):
            item_text = f"Toggle Auto-start (Current: {'Enabled' if autostart_enabled else 'Disabled'})"
            new_menu_items.append(pystray.MenuItem(item_text, toggle_autostart))
            found = True
        else:
            new_menu_items.append(item)
    
    if not found:
        # If not found (first run or item not in initial menu), add it
        item_text = f"Toggle Auto-start (Current: {'Enabled' if autostart_enabled else 'Disabled'})"
        new_menu_items.insert(2, pystray.MenuItem(item_text, toggle_autostart)) # Insert after "Run Export"

    icon.menu = pystray.Menu(*new_menu_items)


# --- Main Execution ---
def main():
    global icon
    setup_logging()
    logging.info("Initializing systray application...")
    
    icon_image = create_icon_image()
    
    # Initial menu definition, auto-start text will be updated after creation
    menu_items = [
        pystray.MenuItem("Open UI", open_ui, default=True),
        pystray.MenuItem("Run Export", on_export_activate),
        pystray.MenuItem("Toggle Auto-start (Checking status...)", toggle_autostart), # Placeholder text
        pystray.MenuItem("Quit", on_quit)
    ]
    
    icon = pystray.Icon("export_for_ai", icon_image, "Export for AI", pystray.Menu(*menu_items))

    # Update the auto-start menu item immediately after icon creation
    update_autostart_menu_item()

    def run_hotkey_listener():
        logging.info("Starting hotkey listener... (Ctrl+Shift+Q for UI, Ctrl+Shift+E for Export)")
        hotkeys = {
            '<ctrl>+<shift>+q': open_ui,
            '<ctrl>+<shift>+e': on_export_activate
        }
        with keyboard.GlobalHotKeys(hotkeys) as h:
            h.join()

    listener_thread = threading.Thread(target=run_hotkey_listener)
    listener_thread.daemon = True
    listener_thread.start()

    logging.info("Application setup complete. Running icon.")
    icon.run()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # This is the "Crash Catcher"
        # If any unexpected error happens, it will be logged to a file.
        logging.critical("An unhandled exception occurred!")
        log_crash(sys.exc_info())
        # The program will exit, but the log file will have the error.