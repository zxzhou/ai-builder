#!/usr/bin/env python3
"""
Pi Day Challenge Circle Drawer

This program draws a near-perfect circle in the Pi Day Challenge game
by calculating optimal center and radius, then simulating mouse movements.

The game evaluates circles based on how close they are to perfect circles,
so precision in center point and radius calculation is crucial for high rank.
"""

import pyautogui
import math
import time
import sys


class CircleDrawer:
    def __init__(self):
        """Initialize the circle drawer with game parameters."""
        # Canvas dimensions (from game analysis)
        self.canvas_width = 350
        self.canvas_height = 350
        
        # Optimal circle parameters for maximum score
        # Center should be at canvas center for best results
        self.center_x = self.canvas_width / 2  # 175
        self.center_y = self.canvas_height / 2  # 175
        
        # Radius: Use ~80% of the smaller dimension to maximize area
        # while leaving margin to avoid edge clipping
        max_radius = min(self.canvas_width, self.canvas_height) / 2
        self.radius = max_radius * 0.85  # ~148.75, using 148 for precision
        
        # Number of points for smooth circle (more points = smoother and more accurate)
        # Increased to 720 points (0.5 degree increments) for higher precision
        self.num_points = 720  # Half-degree increments for maximum smoothness
        
        # Canvas position on screen (will be detected)
        self.canvas_left = None
        self.canvas_top = None
        
        # Safety settings for pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0  # No pause between actions for maximum smoothness
    
    def detect_canvas_position(self):
        """
        Detect the canvas position on screen.
        This accounts for window position and screen resolution.
        """
        print("Please position your mouse over the TOP-LEFT corner of the canvas,")
        print("then press ENTER. The program will detect the canvas position.")
        input("Press ENTER when ready...")
        
        # Get current mouse position as canvas top-left
        self.canvas_left, self.canvas_top = pyautogui.position()
        print(f"Canvas position detected: ({self.canvas_left}, {self.canvas_top})")
        
        return self.canvas_left, self.canvas_top
    
    def calculate_circle_points(self):
        """
        Calculate all points along the circle circumference.
        Returns list of (x, y) tuples in canvas coordinates.
        """
        points = []
        
        for i in range(self.num_points):
            # Calculate angle in radians
            angle = (2 * math.pi * i) / self.num_points
            
            # Calculate point on circle
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            
            points.append((x, y))
        
        return points
    
    def canvas_to_screen(self, canvas_x, canvas_y):
        """
        Convert canvas coordinates to screen coordinates.
        
        Args:
            canvas_x: X coordinate in canvas space (0-350)
            canvas_y: Y coordinate in canvas space (0-350)
        
        Returns:
            (screen_x, screen_y) tuple
        """
        if self.canvas_left is None or self.canvas_top is None:
            raise ValueError("Canvas position not detected. Call detect_canvas_position() first.")
        
        # Convert to screen coordinates
        screen_x = self.canvas_left + canvas_x
        screen_y = self.canvas_top + canvas_y
        
        return screen_x, screen_y
    
    def draw_circle(self, delay_before_start=3, drawing_speed=8.0):
        """
        Draw the circle by moving the mouse along calculated points.
        
        Args:
            delay_before_start: Seconds to wait before starting (to position window)
            drawing_speed: Total time in seconds to complete the circle (slower = more accurate)
        """
        if self.canvas_left is None or self.canvas_top is None:
            raise ValueError("Canvas position not detected. Call detect_canvas_position() first.")
        
        print(f"\nDrawing circle with:")
        print(f"  Center: ({self.center_x:.2f}, {self.center_y:.2f})")
        print(f"  Radius: {self.radius:.2f}")
        print(f"  Points: {self.num_points}")
        print(f"  Drawing speed: {drawing_speed} seconds per circle")
        print(f"\nStarting in {delay_before_start} seconds...")
        print("Move your mouse to the top-left corner of the canvas to cancel (failsafe).")
        
        time.sleep(delay_before_start)
        
        # Calculate all circle points
        points = self.calculate_circle_points()
        
        # Store the exact starting point for perfect closure
        start_point = points[0]
        
        # Move to starting point (first point)
        start_x, start_y = self.canvas_to_screen(start_point[0], start_point[1])
        pyautogui.moveTo(start_x, start_y, duration=0.1)
        time.sleep(0.15)  # Slightly longer pause to ensure position is set
        
        # Click and hold to start drawing (this activates the canvas)
        pyautogui.mouseDown(button='left')
        time.sleep(0.15)  # Longer delay to ensure click is fully registered
        
        # Draw circle using ultra-smooth continuous motion
        print("Drawing circle...")
        total_drawing_time = drawing_speed
        
        # Group points into small batches for smooth interpolation
        # Each batch will be drawn as a single smooth drag
        batch_size = 5  # Points per batch - small enough for smoothness, large enough for efficiency
        num_batches = (len(points) + batch_size - 1) // batch_size
        batch_duration = total_drawing_time / num_batches
        
        # Draw all points in smooth batches
        point_idx = 1  # Start from second point (first is start position)
        
        for batch_idx in range(num_batches):
            # Calculate which point to target for this batch
            end_idx = min(point_idx + batch_size - 1, len(points) - 1)
            
            # For the last batch, target the start point to close the circle
            if end_idx >= len(points) - 1:
                target_canvas_x, target_canvas_y = start_point
            else:
                target_canvas_x, target_canvas_y = points[end_idx]
            
            target_screen_x, target_screen_y = self.canvas_to_screen(target_canvas_x, target_canvas_y)
            
            # Smooth drag through this batch of points
            # Linear tween ensures perfectly smooth, consistent motion
            pyautogui.dragTo(
                target_screen_x, 
                target_screen_y, 
                duration=batch_duration, 
                button='left',
                tween=pyautogui.linear  # Linear interpolation = no acceleration, perfectly smooth
            )
            
            point_idx = end_idx + 1
            
            # Progress indicator
            if (batch_idx + 1) % (num_batches // 10) == 0 or batch_idx == num_batches - 1:
                progress = ((batch_idx + 1) / num_batches) * 100
                print(f"  Progress: {progress:.1f}%")
        
        # Final check: ensure we're exactly at the start point
        current_pos = pyautogui.position()
        start_x, start_y = self.canvas_to_screen(start_point[0], start_point[1])
        # Only drag if we're not already at the start point (within 1 pixel)
        if abs(current_pos[0] - start_x) > 1 or abs(current_pos[1] - start_y) > 1:
            pyautogui.dragTo(
                start_x, 
                start_y, 
                duration=batch_duration * 0.5, 
                button='left',
                tween=pyautogui.linear
            )
        
        # Small pause before releasing to ensure the closure is registered
        time.sleep(0.1)
        
        # Release mouse button
        pyautogui.mouseUp(button='left')
        
        print("Circle drawing complete!")
        print("\nYou can now click 'Calculate Pi' button to see your score.")
    
    def auto_detect_canvas(self):
        """
        Attempt to automatically detect canvas position by searching for
        the canvas element. This requires the browser window to be active.
        """
        print("Attempting to auto-detect canvas position...")
        print("Make sure the game page is visible and active.")
        time.sleep(2)
        
        # This is a fallback - user should manually position
        # In a real implementation, you might use image recognition
        # or browser automation to find the canvas
        print("Auto-detection not fully implemented.")
        print("Please use manual detection instead.")
        self.detect_canvas_position()


def main():
    """Main function to run the circle drawer."""
    print("=" * 60)
    print("Pi Day Challenge - Perfect Circle Drawer")
    print("=" * 60)
    print("\nThis program will help you draw a near-perfect circle")
    print("in the Pi Day Challenge game for a high rank.\n")
    
    drawer = CircleDrawer()
    
    # Detect canvas position
    try:
        drawer.detect_canvas_position()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    
    # Draw the circle
    # Note: You can adjust drawing_speed (default 8.0 seconds)
    # Slower speeds (10-12 seconds) may improve accuracy but take longer
    try:
        drawer.draw_circle(delay_before_start=3, drawing_speed=10.0)
    except KeyboardInterrupt:
        print("\n\nDrawing cancelled by user.")
        pyautogui.mouseUp(button='left')  # Release mouse if still pressed
        sys.exit(0)
    except Exception as e:
        print(f"\nError during drawing: {e}")
        pyautogui.mouseUp(button='left')  # Release mouse if still pressed
        sys.exit(1)


if __name__ == "__main__":
    main()

