#!/usr/bin/env python3
"""
Pi Day Challenge Circle Drawer - Auto Detection Version

Enhanced version that attempts to automatically detect the canvas position
using image recognition, making it easier to use.
"""

import pyautogui
import math
import time
import sys


class AutoCircleDrawer:
    def __init__(self):
        """Initialize the circle drawer with game parameters."""
        # Canvas dimensions (from game analysis)
        self.canvas_width = 350
        self.canvas_height = 350
        
        # Optimal circle parameters
        self.center_x = self.canvas_width / 2  # 175
        self.center_y = self.canvas_height / 2  # 175
        self.radius = min(self.canvas_width, self.canvas_height) / 2 * 0.85  # ~148
        # Increased to 720 points (0.5 degree increments) for higher precision
        self.num_points = 720
        
        # Canvas position
        self.canvas_left = None
        self.canvas_top = None
        
        # Safety settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0  # No pause between actions for maximum smoothness
    
    def find_canvas_by_color(self):
        """
        Attempt to find canvas by looking for the characteristic
        black border of the canvas element.
        """
        print("Attempting to find canvas automatically...")
        print("Make sure the game page is fully visible.")
        time.sleep(1)
        
        # Take a screenshot
        screenshot = pyautogui.screenshot()
        width, height = screenshot.size
        
        # Look for black border (RGB ~0,0,0) which indicates canvas edge
        # This is a simplified approach - in practice, you might use
        # more sophisticated image recognition
        print("Scanning screenshot for canvas...")
        
        # For now, fall back to manual detection
        return None, None
    
    def detect_canvas_manual(self):
        """Manual canvas detection with better instructions."""
        print("\n" + "=" * 60)
        print("CANVAS POSITION DETECTION")
        print("=" * 60)
        print("\nThe canvas is a 350x350 pixel square with a black border.")
        print("Please follow these steps:")
        print("1. Look at the drawing canvas on the game page")
        print("2. Position your mouse cursor at the TOP-LEFT corner")
        print("   (where the black border starts, inside the canvas)")
        print("3. Press ENTER when ready")
        print("\nTIP: You can use the canvas border as a reference point.")
        print("=" * 60 + "\n")
        
        input("Press ENTER when your mouse is at the canvas top-left corner...")
        
        self.canvas_left, self.canvas_top = pyautogui.position()
        print(f"\n✓ Canvas position detected: ({self.canvas_left}, {self.canvas_top})")
        
        # Verify by showing where we think the center is
        center_screen_x = self.canvas_left + self.center_x
        center_screen_y = self.canvas_top + self.center_y
        print(f"  Circle center will be at screen position: ({center_screen_x:.0f}, {center_screen_y:.0f})")
        
        confirm = input("\nDoes this look correct? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Let's try again...")
            return self.detect_canvas_manual()
        
        return self.canvas_left, self.canvas_top
    
    def calculate_circle_points(self):
        """Calculate all points along the circle circumference."""
        points = []
        
        for i in range(self.num_points):
            angle = (2 * math.pi * i) / self.num_points
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            points.append((x, y))
        
        return points
    
    def canvas_to_screen(self, canvas_x, canvas_y):
        """Convert canvas coordinates to screen coordinates."""
        if self.canvas_left is None or self.canvas_top is None:
            raise ValueError("Canvas position not detected.")
        
        screen_x = self.canvas_left + canvas_x
        screen_y = self.canvas_top + canvas_y
        return screen_x, screen_y
    
    def draw_circle(self, delay_before_start=3):
        """Draw the circle with smooth mouse movements."""
        if self.canvas_left is None or self.canvas_top is None:
            raise ValueError("Canvas position not detected.")
        
        print(f"\n{'=' * 60}")
        print("CIRCLE DRAWING PARAMETERS")
        print(f"{'=' * 60}")
        print(f"Center: ({self.center_x:.2f}, {self.center_y:.2f})")
        print(f"Radius: {self.radius:.2f} pixels")
        print(f"Points: {self.num_points}")
        print(f"Circumference: {2 * math.pi * self.radius:.2f} pixels")
        print(f"{'=' * 60}\n")
        
        print(f"Starting in {delay_before_start} seconds...")
        print("Move mouse to screen corner to cancel (failsafe).\n")
        
        for i in range(delay_before_start, 0, -1):
            print(f"  {i}...", end='\r')
            time.sleep(1)
        print("  Drawing now!     ")
        
        points = self.calculate_circle_points()
        
        # Move to starting point
        start_x, start_y = self.canvas_to_screen(points[0][0], points[0][1])
        pyautogui.moveTo(start_x, start_y, duration=0.1)
        time.sleep(0.1)
        
        # Click and hold to start drawing (this activates the canvas)
        pyautogui.mouseDown(button='left')
        time.sleep(0.15)  # Longer delay to ensure click is fully registered
        
        # Draw circle using ultra-smooth batched motion
        start_time = time.time()
        total_drawing_time = 10.0  # 10 seconds for full circle (adjustable)
        
        # Group points into small batches for smooth interpolation
        batch_size = 5  # Points per batch
        num_batches = (len(points) + batch_size - 1) // batch_size
        batch_duration = total_drawing_time / num_batches
        
        start_point = points[0]
        point_idx = 1  # Start from second point
        
        for batch_idx in range(num_batches):
            # Calculate which point to target for this batch
            end_idx = min(point_idx + batch_size - 1, len(points) - 1)
            
            # For the last batch, target the start point to close the circle
            if end_idx >= len(points) - 1:
                target_canvas_x, target_canvas_y = start_point
            else:
                target_canvas_x, target_canvas_y = points[end_idx]
            
            target_screen_x, target_screen_y = self.canvas_to_screen(target_canvas_x, target_canvas_y)
            
            # Smooth drag with linear interpolation
            pyautogui.dragTo(
                target_screen_x, 
                target_screen_y, 
                duration=batch_duration, 
                button='left',
                tween=pyautogui.linear  # Linear = perfectly smooth
            )
            
            point_idx = end_idx + 1
            
            # Progress updates
            if (batch_idx + 1) % (num_batches // 10) == 0 or batch_idx == num_batches - 1:
                progress = ((batch_idx + 1) / num_batches) * 100
                elapsed = time.time() - start_time
                print(f"  Progress: {progress:.1f}% ({elapsed:.2f}s)", end='\r')
        
        # Final check: ensure we're exactly at the start point
        current_pos = pyautogui.position()
        start_x, start_y = self.canvas_to_screen(start_point[0], start_point[1])
        if abs(current_pos[0] - start_x) > 1 or abs(current_pos[1] - start_y) > 1:
            pyautogui.dragTo(start_x, start_y, duration=batch_duration * 0.5, button='left', tween=pyautogui.linear)
        
        # Small pause before releasing to ensure closure is registered
        time.sleep(0.1)
        
        pyautogui.mouseUp(button='left')
        
        elapsed = time.time() - start_time
        print(f"\n✓ Circle complete! (took {elapsed:.2f} seconds)")
        print("\nNow click 'Calculate Pi' in the game to see your score!")


def main():
    """Main function."""
    print("=" * 60)
    print("Pi Day Challenge - Perfect Circle Drawer (Auto Version)")
    print("=" * 60)
    print("\nThis program draws a mathematically perfect circle")
    print("for maximum score in the Pi Day Challenge.\n")
    
    drawer = AutoCircleDrawer()
    
    try:
        # Detect canvas position
        drawer.detect_canvas_manual()
        
        # Draw circle
        drawer.draw_circle(delay_before_start=3)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Operation cancelled.")
        pyautogui.mouseUp(button='left')
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        pyautogui.mouseUp(button='left')
        sys.exit(1)


if __name__ == "__main__":
    main()

