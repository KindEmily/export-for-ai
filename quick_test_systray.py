# File: quick_test_systray.py
import pystray
from PIL import Image, ImageDraw
import sys

print("Attempting to create a minimal system tray icon...")

def create_image():
    # Create a simple placeholder image
    width = 64
    height = 64
    color1 = "#ff0000" # Red
    color2 = "#ffffff" # White
    image = Image.new("RGB", (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle([(width // 4, height // 4), (width * 3 // 4, height * 3 // 4)], fill=color2)
    return image

def on_quit(icon, item):
    print("Quit clicked!")
    icon.stop()
    sys.exit(0)

try:
    icon_image = create_image()
    menu = pystray.Menu(pystray.MenuItem("Quit", on_quit))
    icon = pystray.Icon("minimal_test", icon_image, "Minimal Test Icon", menu)
    
    print("Icon created. Running... (Press Ctrl+C in this terminal to stop)")
    icon.run()

except Exception as e:
    print("\n--- AN ERROR OCCURRED ---")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit.")