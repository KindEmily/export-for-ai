import threading
import webbrowser
import sys
import os
import json
import shutil

import pystray
from PIL import Image, ImageDraw
from pynput import keyboard
import uvicorn

import app_main
from web_ui import app

server_instance = None
server_thread = None
icon = None
UI_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "ui_config.json")


def get_icon_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'assets', 'icon.png')
    return os.path.join('assets', 'icon.png')


def create_icon_image():
    try:
        return Image.open(get_icon_path())
    except FileNotFoundError:
        print("Warning: assets/icon.png not found. Creating a placeholder icon.")
        width = 64
        height = 64
        color1 = "#4f46e5" 
        color2 = "#ffffff"
        image = Image.new("RGB", (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle([(width // 4, height // 4), (width * 3 // 4, height * 3 // 4)], fill=color2)
        return image


def start_web_server():
    global server_instance, server_thread
    if server_thread and server_thread.is_alive():
        print("Server is already running.")
        return

    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="warning")
    server_instance = uvicorn.Server(config)
    server_thread = threading.Thread(target=server_instance.run)
    server_thread.daemon = True
    server_thread.start()
    print("Web server started.")


def open_ui():
    print("Hotkey activated. Opening UI...")
    start_web_server()
    webbrowser.open("http://127.0.0.1:8000")
    if icon:
        icon.visible = True


def run_export_and_open_folder():
    print("\n--- Starting Export via Hotkey ---")
    if icon:
        icon.notify('Export process started...', 'Export for AI')

    try:
        with open(UI_CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not read ui_config.json: {e}")
        if icon:
            icon.notify(f'Error reading config: {e}', 'Export Failed')
        return

    export_destination = config.get("export_destination")
    repositories = config.get("repositories", [])
    assets_to_copy = config.get("assets_to_copy", [])

    if not export_destination or not os.path.isdir(export_destination):
        error_msg = f"Export destination '{export_destination}' is not a valid directory."
        print(f"[ERROR] {error_msg}")
        if icon:
            icon.notify(error_msg, 'Export Failed')
        return

    app_main.setup_logging()
    for repo_path in repositories:
        print(f"Processing repository: {repo_path}")
        md_file_path = app_main.process_single_repository(repo_path)
        if md_file_path:
            try:
                shutil.copy(md_file_path, export_destination)
                print(f"  -> Copied '{os.path.basename(md_file_path)}' to destination.")
                shutil.rmtree(os.path.dirname(md_file_path))
            except Exception as e:
                print(f"[ERROR] Failed to copy or clean up for '{repo_path}': {e}")

    for asset_path in assets_to_copy:
        print(f"Copying asset: {asset_path}")
        try:
            dest_name = os.path.basename(asset_path)
            destination_path = os.path.join(export_destination, dest_name)
            if os.path.isdir(asset_path):
                shutil.copytree(asset_path, destination_path, dirs_exist_ok=True)
            else:
                shutil.copy2(asset_path, destination_path)
            print(f"  -> Copied '{dest_name}'.")
        except Exception as e:
            print(f"[ERROR] Failed to copy asset '{asset_path}': {e}")

    print(f"--- Export complete. Opening folder: {export_destination} ---")
    if icon:
        icon.notify('Export complete! Opening destination folder.', 'Export for AI')
    webbrowser.open(os.path.realpath(export_destination))


def on_export_activate():
    print("Export hotkey activated. Starting process in background...")
    export_thread = threading.Thread(target=run_export_and_open_folder)
    export_thread.daemon = True
    export_thread.start()


def on_quit(icon_instance, item):
    print("Quit command received. Shutting down.")
    if server_instance:
        server_instance.should_exit = True
    icon_instance.stop()
    sys.exit(0)


def main():
    global icon
    icon_image = create_icon_image()
    menu = pystray.Menu(
        pystray.MenuItem("Open UI", open_ui, default=True),
        pystray.MenuItem("Run Export", on_export_activate),
        pystray.MenuItem("Quit", on_quit)
    )
    icon = pystray.Icon("export_for_ai", icon_image, "Export for AI", menu)

    def run_hotkey_listener():
        print("Hotkey listener started in background. Press Ctrl+Shift+Q to open UI, Ctrl+Shift+E to run export.")
        hotkeys = {
            '<ctrl>+<shift>+q': open_ui,
            '<ctrl>+<shift>+e': on_export_activate
        }
        with keyboard.GlobalHotKeys(hotkeys) as h:
            h.join()

    listener_thread = threading.Thread(target=run_hotkey_listener)
    listener_thread.daemon = True
    listener_thread.start()

    icon.run()


if __name__ == "__main__":
    main()