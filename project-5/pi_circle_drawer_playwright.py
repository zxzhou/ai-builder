#!/usr/bin/env python3
"""
Pi Day Challenge Circle Drawer - Playwright Version

This version uses Playwright to directly draw on the canvas using JavaScript,
which provides perfectly smooth circles without any zigzag artifacts.
"""

import asyncio
import math
from playwright.async_api import async_playwright


class PlaywrightCircleDrawer:
    def __init__(self):
        """Initialize the circle drawer with game parameters."""
        # Canvas dimensions
        self.canvas_width = 350
        self.canvas_height = 350
        
        # Optimal circle parameters
        self.center_x = self.canvas_width / 2  # 175
        self.center_y = self.canvas_height / 2  # 175
        max_radius = min(self.canvas_width, self.canvas_height) / 2
        self.radius = max_radius * 0.85  # ~148.75
        
        # High precision: 1000 points for ultra-smooth circle
        self.num_points = 1000
    
    def calculate_circle_points(self):
        """Calculate all points along the circle circumference."""
        points = []
        for i in range(self.num_points):
            angle = (2 * math.pi * i) / self.num_points
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            points.append((x, y))
        return points
    
    async def draw_circle_on_canvas(self, page):
        """
        Draw a perfect circle using Playwright's smooth mouse movements.
        This uses Playwright's built-in smooth interpolation for perfect curves.
        """
        print(f"\nDrawing circle with:")
        print(f"  Center: ({self.center_x:.2f}, {self.center_y:.2f})")
        print(f"  Radius: {self.radius:.2f}")
        print(f"  Points: {self.num_points}")
        print()
        
        # Get canvas element and its position
        canvas = await page.query_selector('canvas')
        if not canvas:
            raise Exception("Canvas element not found!")
        
        canvas_box = await canvas.bounding_box()
        canvas_x = canvas_box['x']
        canvas_y = canvas_box['y']
        
        # Calculate circle points
        points = self.calculate_circle_points()
        
        # Convert to page coordinates
        start_x = canvas_x + points[0][0]
        start_y = canvas_y + points[0][1]
        
        # Move to starting point
        await page.mouse.move(start_x, start_y)
        await asyncio.sleep(0.1)
        
        # Start drawing (mouse down)
        await page.mouse.down()
        await asyncio.sleep(0.05)
        
        print("Drawing circle...")
        
        # Draw through points in smooth segments
        # Playwright's mouse.move() with steps creates perfectly smooth curves
        total_time = 10.0  # 10 seconds for full circle
        segment_size = 10  # Points per segment for smooth interpolation
        num_segments = (len(points) + segment_size - 1) // segment_size
        segment_delay = total_time / num_segments
        
        # Draw through all points in smooth segments
        for segment_idx in range(num_segments):
            start_idx = segment_idx * segment_size
            end_idx = min((segment_idx + 1) * segment_size, len(points))
            
            if end_idx >= len(points):
                # Last segment - go to start point
                target_x = canvas_x + points[0][0]
                target_y = canvas_y + points[0][1]
            else:
                target_x = canvas_x + points[end_idx - 1][0]
                target_y = canvas_y + points[end_idx - 1][1]
            
            # Smooth mouse movement with interpolation
            # Using steps=segment_size creates smooth curve through the segment
            await page.mouse.move(target_x, target_y, steps=segment_size)
            
            # Delay for smooth drawing
            await asyncio.sleep(segment_delay)
            
            # Progress indicator
            if (segment_idx + 1) % (num_segments // 10) == 0 or segment_idx == num_segments - 1:
                progress = ((segment_idx + 1) / num_segments) * 100
                print(f"  Progress: {progress:.1f}%")
        
        # Final closure - return to exact start point
        await page.mouse.move(start_x, start_y, steps=10)
        await asyncio.sleep(0.1)
        
        # Release mouse (mouse up)
        await page.mouse.up()
        
        print("Circle drawing complete!")
        print("\nYou can now click 'Calculate Pi' button to see your score.")
    
    async def run(self, headless=False):
        """Run the Playwright circle drawer."""
        async with async_playwright() as p:
            print("=" * 60)
            print("Pi Day Challenge - Perfect Circle Drawer (Playwright)")
            print("=" * 60)
            print("\nLaunching browser...")
            
            # Launch browser
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720}
            )
            page = await context.new_page()
            
            # Navigate to the game
            print("Navigating to game page...")
            await page.goto('https://yage.ai/genai/pi.html')
            await page.wait_for_load_state('networkidle')
            
            # Wait for canvas to be ready
            await page.wait_for_selector('canvas', timeout=10000)
            await asyncio.sleep(1)  # Give page time to fully load
            
            # Clear canvas if needed (click clear button)
            try:
                clear_button = await page.query_selector('button:has-text("Clear Canvas")')
                if clear_button:
                    await clear_button.click()
                    await asyncio.sleep(0.5)
            except:
                pass
            
            # Draw the circle
            try:
                await self.draw_circle_on_canvas(page)
            except Exception as e:
                print(f"\nError during drawing: {e}")
                raise
            
            # Keep browser open so user can see the result
            print("\nBrowser will stay open for 30 seconds so you can see the result.")
            print("Click 'Calculate Pi' in the game to see your score!")
            await asyncio.sleep(30)
            
            # Close browser
            await browser.close()
            print("\nDone!")


async def main():
    """Main function."""
    drawer = PlaywrightCircleDrawer()
    
    # Set headless=False to see the browser, or True to run in background
    await drawer.run(headless=False)


if __name__ == "__main__":
    asyncio.run(main())

