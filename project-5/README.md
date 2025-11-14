# Pi Day Challenge - Perfect Circle Drawer

A Python program that draws a near-perfect circle in the [Pi Day Challenge game](https://yage.ai/genai/pi.html) to achieve a high rank.

## Overview

The Pi Day Challenge game evaluates how well you can draw a circle. This program calculates the optimal center point and radius, then simulates precise mouse movements to draw a mathematically perfect circle.

## Features

- **Two Versions Available**:
  - **Playwright Version** (Recommended): Direct browser control for perfectly smooth circles with no zigzag artifacts
  - **PyAutoGUI Version**: Mouse simulation for manual browser control
- **Optimal Circle Calculation**: Automatically calculates the best center point (canvas center) and radius (85% of canvas size) for maximum score
- **High Precision**: Uses 1000 points (Playwright) or 720 points (PyAutoGUI) for ultra-smooth, near-perfect circles
- **Adjustable Drawing Speed**: Configurable drawing speed (default 10 seconds) - slower speeds improve accuracy
- **Perfect Circle Closure**: Ensures the circle closes perfectly at the starting point for accurate Pi calculation
- **Smooth Drawing**: Playwright's built-in interpolation creates perfectly smooth curves
- **Auto Browser Control**: Playwright version automatically opens browser and navigates to the game

## Requirements

- Python 3.7 or higher
- `pyautogui` library (for PyAutoGUI version)
- `playwright` library (for Playwright version)
- Chromium browser (installed via `playwright install chromium` for Playwright version)

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd project-5
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers (for Playwright version):**
   ```bash
   playwright install chromium
   ```
   Note: This is only needed if you want to use the Playwright version (`pi_circle_drawer_playwright.py`)

## Usage

1. **Open the game in your browser:**
   - Navigate to https://yage.ai/genai/pi.html
   - Make sure the browser window is visible and the canvas is accessible

2. **Run the program:**
   
   **Option A: Playwright version (Recommended - Smoothest):**
   ```bash
   python pi_circle_drawer_playwright.py
   ```
   This version uses Playwright to directly control the browser and draw on the canvas, providing the smoothest circles with no zigzag artifacts.
   
   **Option B: PyAutoGUI version:**
   ```bash
   python pi_circle_drawer.py
   ```
   This version uses mouse simulation and requires you to position your mouse at the canvas corner.

3. **Follow the prompts:**
   - When prompted, position your mouse over the **top-left corner** of the canvas
   - Press ENTER to confirm the canvas position
   - The program will wait 3 seconds, then start drawing
   - Move your mouse to the top-left corner of your screen to cancel (failsafe)

4. **After drawing:**
   - Click the "Calculate Pi" button in the game to see your score
   - You should achieve a high rank with the near-perfect circle!

## How It Works

1. **Canvas Detection**: The program asks you to position your mouse at the canvas top-left corner to detect its position on screen

2. **Circle Calculation**:
   - Center: (175, 175) - the exact center of the 350x350 canvas
   - Radius: ~148 pixels (85% of half the canvas size)
   - Points: 720 points evenly distributed around the circle (0.5 degree increments)
   - Drawing Speed: 10 seconds per full circle (adjustable for accuracy)

3. **Coordinate Conversion**: Converts canvas coordinates (0-350) to screen coordinates based on detected canvas position

4. **Drawing**: Simulates mouse movements by:
   - Moving to the starting point
   - Pressing mouse button down
   - Moving through all 360 points smoothly
   - Returning to start point to close the circle
   - Releasing mouse button

## Technical Details

- **Canvas Size**: 350x350 pixels (detected from game)
- **Optimal Center**: (175, 175) - maximizes symmetry
- **Optimal Radius**: ~148 pixels - maximizes area while avoiding edge clipping
- **Point Density**: 360 points for maximum smoothness
- **Drawing Speed**: ~0.005 seconds per point for natural movement

## Tips for Best Results

1. **Window Position**: Keep the browser window in a consistent position
2. **Screen Resolution**: The program accounts for your screen resolution automatically
3. **Don't Move Mouse**: Keep your mouse still during the 3-second countdown
4. **Clear Canvas First**: Use the "Clear Canvas" button if you need to redraw
5. **Multiple Attempts**: You can run the program multiple times to try different parameters

## Customization

You can modify the circle parameters in the `CircleDrawer` class or when calling `draw_circle()`:

```python
# In pi_circle_drawer.py, modify these values in __init__:
self.center_x = 175  # X coordinate of circle center
self.center_y = 175  # Y coordinate of circle center
self.radius = 148    # Circle radius in pixels
self.num_points = 720 # Number of points (more = smoother)

# Or adjust drawing speed when calling draw_circle():
drawer.draw_circle(delay_before_start=3, drawing_speed=12.0)  # Slower = more accurate
```

**Tips for Better Accuracy:**
- Increase `drawing_speed` to 12-15 seconds for maximum accuracy (slower drawing)
- Ensure the canvas position is detected accurately
- Make sure the browser window is fully visible and not minimized

## Troubleshooting

- **"Canvas position not detected"**: Make sure you positioned your mouse correctly and pressed ENTER
- **Circle drawn in wrong location**: Re-run the program and carefully position mouse at canvas top-left corner
- **Drawing too fast/slow**: Adjust `pyautogui.PAUSE` and `duration` parameters in the code
- **Failsafe triggered**: Move mouse away from screen corners before running

## Safety

- The program includes a failsafe: move your mouse to the top-left corner of your screen to cancel
- The program will automatically release the mouse button if interrupted
- All movements are smooth and controlled to avoid erratic behavior

## License

This project is provided as-is for educational and personal use.

