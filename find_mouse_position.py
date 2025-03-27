import pyautogui
import time
import keyboard

print("=== Mouse Position Tracker ===")
print("1. Click in World of Warcraft to record positions")
print("2. Position your cursor and press 'C' to record coordinates")
print("3. Press Ctrl+C in the terminal to exit when done")
print("\nCoordinates will be recorded when you press the 'C' key...")

top_left = None
bottom_right = None

def record_position():
    x, y = pyautogui.position()
    print(f"Position recorded: X: {x}, Y: {y}")
    
    global top_left, bottom_right
    if top_left is None:
        top_left = (x, y)
        print("Top-left corner recorded. Now move to the bottom-right corner and press 'C'.")
    elif bottom_right is None:
        bottom_right = (x, y)
        
        # Calculate the detection region parameters
        left = top_left[0]
        top = top_left[1]
        width = bottom_right[0] - top_left[0]
        height = bottom_right[1] - top_left[1]
        
        print("\n=== Detection Region Parameters ===")
        print(f"self.detection_region = {{'top': {top}, 'left': {left}, 'width': {width}, 'height': {height}}}")
        
        # Reset for another set of measurements if needed
        top_left = None
        bottom_right = None
        print("\nYou can measure another region. Move to a new top-left corner and press 'C'.")

# Register keyboard event for 'C' key
keyboard.on_press_key('c', lambda e: record_position())

try:
    print("Press 'C' to capture cursor position, Ctrl+C to exit.")
    while True:
        time.sleep(0.1)  # Low CPU usage while waiting
except KeyboardInterrupt:
    print("\nExiting program.")