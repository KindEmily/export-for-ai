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
from typing import Optional

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

# --- Setup ---
def setup_logging():
    """Sets up basic logging to the console."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

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

# --- Main Execution ---
def main():
    global icon
    setup_logging()
    logging.info("Initializing systray application...")
    
    icon_image = create_icon_image()
    menu = pystray.Menu(
        pystray.MenuItem("Open UI", open_ui, default=True),
        pystray.MenuItem("Run Export", on_export_activate),
        pystray.MenuItem("Quit", on_quit)
    )
    icon = pystray.Icon("export_for_ai", icon_image, "Export for AI", menu)

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