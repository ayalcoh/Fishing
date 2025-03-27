import cv2
import numpy as np
import pyautogui
import time
import keyboard
import random
from mss import mss

class WoWFishingBot:
    def __init__(self):
        # Configuration parameters
        self.fishing_key = '1'  # Key bound to fishing in WoW
        self.screen_region = {'top': 0, 'left': 0, 'width': 2560, 'height': 1440}  # Adjusted for 2560x1440
        self.detection_region = {'top': 500, 'left': 1000, 'width': 1000, 'height': 500} 
        self.threshold_white_pixels = 160  # Minimum white pixels to trigger a bite
        self.bobber_template = None
        self.running = False
        
        # Try to load the template
        try:
            self.bobber_template = cv2.imread('bobber_template.png', 0)
            print("Bobber template loaded successfully")
        except:
            print("No bobber template found. You'll need to create one.")
    
    def create_bobber_template(self):
        """Capture a template of the fishing bobber"""
        print("Position your cursor over the bobber and press 'T' to capture template")
        while not keyboard.is_pressed('t'):
            time.sleep(0.1)
        
        with mss() as sct:
            # Capture around mouse position
            x, y = pyautogui.position()
            template_region = {'top': y-25, 'left': x-25, 'width': 50, 'height': 50}
            template = np.array(sct.grab(template_region))
            
            # Convert to grayscale
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            
            # Save template
            cv2.imwrite('bobber_template.png', template_gray)
            self.bobber_template = template_gray
            print("Template captured and saved!")
    
    def capture_screen(self):
        """Capture the specified region of the screen"""
        with mss() as sct:
            screenshot = np.array(sct.grab(self.detection_region))
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            return gray
    
    def find_bobber(self, screenshot):
        """Find the bobber in the screenshot using template matching"""
        if self.bobber_template is None:
            print("No bobber template available. Please create one first.")
            return None
        
        result = cv2.matchTemplate(screenshot, self.bobber_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # If confidence is high enough, return the center position
        if max_val > 0.6:
            h, w = self.bobber_template.shape
            center_x = max_loc[0] + w // 2 + self.detection_region['left']
            center_y = max_loc[1] + h // 2 + self.detection_region['top']
            return (center_x, center_y)
        
        return None
    
    def detect_splash(self, screenshot):
        """Detect if there's a splash (white pixels) in the bobber area"""
        # Apply threshold to isolate bright areas
        _, thresh = cv2.threshold(screenshot, 200, 255, cv2.THRESH_BINARY)
        
        # Count white pixels
        white_pixel_count = np.sum(thresh == 255)
        
        return white_pixel_count > self.threshold_white_pixels
    
    def cast_fishing_rod(self):
        """Press the fishing key to cast the rod"""
        pyautogui.press(self.fishing_key)
        
        # Wait for the casting animation
        time.sleep(1.5)
    
    def click_bobber(self, position):
        """Click on the bobber position with improved reliability"""
        # Add a slight random offset for more human-like behavior
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        
        target_x = position[0] + offset_x
        target_y = position[1] + offset_y
        
        print(f"Moving mouse to position: {target_x}, {target_y}")
        
        # Separate the movement from the click - critical for game recognition
        pyautogui.moveTo(target_x, target_y, duration=0.2)
        
        # Wait for the mouse to settle at the position
        time.sleep(0.3)
        
        # First click attempt
        print("First click attempt")
        pyautogui.click(button='right')
        
        # Short wait
        time.sleep(0.2)
        
        # Second click attempt for reliability
        print("Second click attempt")
        pyautogui.click(button='right')
        
        # Wait for the loot window
        time.sleep(1)
        
        # For more reliable operation, can add a third click attempt
        print("Third click attempt")
        pyautogui.click(button='right')
        
        print("Clicking complete!")
    
    def run(self):
        """Main bot loop"""
        print("Starting WoW Fishing Bot")
        print("Press 'S' to stop the bot")
        
        self.running = True
        
        while self.running:
            if keyboard.is_pressed('s'):
                self.running = False
                print("Stopping bot...")
                break
            
            print("Casting fishing rod...")
            self.cast_fishing_rod()
            
            # Find the bobber
            bobber_position = None
            find_attempts = 0
            max_attempts = 10
            
            while bobber_position is None and find_attempts < max_attempts:
                screenshot = self.capture_screen()
                bobber_position = self.find_bobber(screenshot)
                find_attempts += 1
                time.sleep(0.1)
            
            if bobber_position is None:
                print("Could not find bobber. Recasting...")
                continue
            
            print(f"Bobber found at position: {bobber_position}")
            
            # Wait for a splash
            splash_detected = False
            timeout = time.time() + 25  # 20 second timeout for a bite
            
            while not splash_detected and time.time() < timeout:
                screenshot = self.capture_screen()
                splash_detected = self.detect_splash(screenshot)
                
                if keyboard.is_pressed('s'):
                    self.running = False
                    break
                
                time.sleep(0.1)
            
            if splash_detected:
                print("Splash detected! Clicking bobber...")
                self.click_bobber(bobber_position)
                
                # Wait a bit before next cast
                wait_time = random.uniform(1.0, 2.0)
                time.sleep(wait_time)
            else:
                print("No bite detected, recasting...")
        
        print("Bot stopped")

if __name__ == "__main__":
    bot = WoWFishingBot()
    
    # Check if template exists, if not create one
    if bot.bobber_template is None:
        bot.create_bobber_template()
    
    print("Bot initialized. Press 'R' to start fishing, 'S' to stop.")
    while not keyboard.is_pressed('r'):
        time.sleep(0.1)
    
    bot.run()