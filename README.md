# WoW Fishing Bot

An automated fishing bot for World of Warcraft that uses computer vision to detect and click on fishing bobbers.

## Features

- Automatically casts your fishing rod
- Uses computer vision to find the fishing bobber
- Detects when a fish bites by monitoring for splash animations
- Right-clicks the bobber when a bite is detected
- Includes a utility script to help configure detection regions

## Requirements

- Python 3.6+
- The following Python packages:
  - opencv-python
  - numpy
  - pyautogui
  - keyboard
  - mss
  - time
  - random

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/ayalcoh/Fishing.git
   cd Fishing
   ```

2. Install the required packages:
   ```
   pip install opencv-python numpy pyautogui keyboard mss
   ```

## Setup

1. Configure the bot by adjusting the following parameters in `wow-fishing-bot.py`:
   - `fishing_key`: The key bound to your fishing ability in WoW (default is '1')
   - `screen_region`: Your screen resolution (default is set for 2560x1440)
   - `detection_region`: The area where the bot will look for the bobber
   - `threshold_white_pixels`: Sensitivity for bite detection

2. Use the included `find_mouse_position.py` utility to help determine the correct detection region:
   ```
   python find_mouse_position.py
   ```

3. Follow the on-screen instructions to record the top-left and bottom-right corners of your desired detection region.

## Usage

1. Start the bot with:
   ```
   python wow-fishing-bot.py
   ```

2. When prompted, position your cursor over the bobber and press 'T' to capture a template (only needed the first time).

3. Press 'R' to start fishing.

4. Press 'S' at any time to stop the bot.

## How It Works

1. The bot presses your configured fishing key to cast your rod.
2. It uses template matching to locate the bobber on screen.
3. Once found, it monitors the area for white pixels that indicate a splash.
4. When a splash is detected, it right-clicks on the bobber to catch the fish.
5. The process repeats until you stop it.

## Customization

- For different WoW UI layouts or screen resolutions, you may need to adjust the detection region.
- If the bot has trouble finding the bobber, you can recreate the bobber template by deleting the existing template file.

## Disclaimer

Using automation tools may violate the World of Warcraft Terms of Service. Use at your own risk. This project is for educational purposes only.


## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.
