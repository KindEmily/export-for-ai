import threading
import webbrowser
import sys
import os

import pystray
from PIL import Image, ImageDraw
from pynput import keyboard
import uvicorn

from web_ui import app

server_instance = None
server_thread = None
icon = None


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


def on_quit(icon_instance, item):
    print("Quit command received. Shutting down.")
    if server_instance:
        server_instance.should_exit = True
    icon_instance.stop()
    # The listener is in a daemon thread, so it will exit with the main app.
    # To be explicit, we can exit the process.
    sys.exit(0)


def main():
    global icon
    icon_image = create_icon_image()
    menu = pystray.Menu(
        pystray.MenuItem("Open UI", open_ui, default=True),
        pystray.MenuItem("Quit", on_quit)
    )
    icon = pystray.Icon("export_for_ai", icon_image, "Export for AI", menu)

    def run_hotkey_listener():
        print("Hotkey listener started in background thread. Press Ctrl+Shift+Q to open the UI.")
        with keyboard.GlobalHotKeys({'<ctrl>+<shift>+q': open_ui}) as h:
            h.join()

    listener_thread = threading.Thread(target=run_hotkey_listener)
    listener_thread.daemon = True
    listener_thread.start()

    # pystray must run in the main thread
    icon.run()


if __name__ == "__main__":
    main()