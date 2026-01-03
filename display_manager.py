"""
Display Manager - Handles Waveshare 4.2" e-Paper display rendering
Requires Waveshare epd4in2 driver in lib/ directory
"""

# Note: This uses Waveshare's V2 MicroPython driver from lib/Pico_ePaper_4_2_V2.py
# The V2 driver is newer (2023) with improved performance and bug fixes

class DisplayManager:
    def __init__(self):
        """Initialize the e-Paper display"""
        self.width = 400
        self.height = 300
        self.epd = None
        self.initialized = False
        
        try:
            # Import Waveshare V2 driver (must be in lib/)
            import sys
            sys.path.append('/lib')  # Ensure lib is in path
            from Pico_ePaper_4_2_V2 import EPD_4in2
            # Note: EPD_4in2() initializes automatically in __init__
            self.epd = EPD_4in2()
            self.initialized = True
            print("Display initialized successfully (V2 driver)")
        except ImportError as ie:
            print(f"WARNING: Pico_ePaper_4_2_V2 driver not found: {ie}")
            print("Running in simulation mode.")
            print("To use real display, ensure lib/Pico_ePaper_4_2_V2.py exists")
            self.initialized = False
        except Exception as e:
            print(f"Display initialization error: {e}")
            self.initialized = False
    
    def clear(self):
        """Clear the display to white"""
        if not self.initialized:
            print("[DISPLAY] Clear (simulated)")
            return
        
        try:
            self.epd.EPD_4IN2_V2_Clear()
            print("Display cleared")
        except Exception as e:
            print(f"Error clearing display: {e}")
    
    def draw_moon_data(self, moon_data, location_name, last_update):
        """
        Draw moon phase information on the display
        
        Args:
            moon_data: dict with moon phase info
            location_name: string for location
            last_update: timestamp of last update
        """
        if not self.initialized:
            self._simulate_display(moon_data, location_name, last_update)
            return
        
        try:
            # Use the driver's built-in framebuffer
            import time
            
            # Clear the built-in framebuffer
            self.epd.image1Gray.fill(0xff)  # 0xff = white
            
            # Draw content directly on the driver's framebuffer
            self._draw_layout(self.epd.image1Gray, moon_data, location_name, last_update)
            
            # Send to display using driver's method
            self.epd.EPD_4IN2_V2_Display(self.epd.buffer_1Gray)
            print("Display updated successfully")
            
        except Exception as e:
            print(f"Error updating display: {e}")
    
    def _draw_layout(self, fb, moon_data, location_name, last_update):
        """
        Draw the complete layout on the framebuffer
        
        Layout:
        - Top: Location and date
        - Center: Large moon phase graphic
        - Bottom: Phase name, illumination, rise/set times
        """
        import time
        
        # Extract data
        phase_name = moon_data.get('phase_name', 'Unknown')
        illumination = moon_data.get('illumination', 0)
        moonrise = moon_data.get('moonrise', 'N/A')
        moonset = moon_data.get('moonset', 'N/A')
        
        # Format current date
        current_time = time.localtime(last_update)
        date_str = f"{current_time[1]:02d}/{current_time[2]:02d}/{current_time[0]}"
        time_str = f"{current_time[3]:02d}:{current_time[4]:02d}"
        
        # Draw header (location and date)
        self._draw_text(fb, location_name, 10, 10, 2)
        self._draw_text(fb, date_str + " " + time_str, 10, 35, 1)
        
        # Draw large moon phase graphic in center
        moon_y = 80
        self._draw_moon_phase_graphic(fb, phase_name, 200, moon_y)
        
        # Draw phase information at bottom
        info_y = 220
        self._draw_text(fb, phase_name, 10, info_y, 2)
        self._draw_text(fb, f"Illumination: {illumination:.1f}%", 10, info_y + 30, 1)
        self._draw_text(fb, f"Rise: {moonrise}  Set: {moonset}", 10, info_y + 50, 1)
    
    def _draw_text(self, fb, text, x, y, scale=1):
        """
        Draw text on framebuffer
        Note: MicroPython's framebuf has basic text support (8x8 font)
        """
        try:
            fb.text(text, x, y, 1)
        except Exception as e:
            print(f"Error drawing text: {e}")
    
    def _draw_moon_phase_graphic(self, fb, phase_name, center_x, center_y):
        """
        Draw a simple moon phase graphic
        For a real implementation, you'd load pre-rendered bitmaps
        """
        radius = 50
        
        # Draw moon circle outline
        self._draw_circle(fb, center_x, center_y, radius, filled=False)
        
        # For simplicity, we'll use text representation
        # In production, load actual moon phase images
        phase_symbols = {
            "New Moon": "●",
            "Waxing Crescent": ")",
            "First Quarter": "◐",
            "Waxing Gibbous": "◑",
            "Full Moon": "○",
            "Waning Gibbous": "◒",
            "Last Quarter": "◓",
            "Waning Crescent": "("
        }
        
        symbol = phase_symbols.get(phase_name, "?")
        # This is a placeholder - actual implementation would use images
        self._draw_text(fb, symbol, center_x - 4, center_y - 4, 3)
    
    def _draw_circle(self, fb, x0, y0, radius, filled=False):
        """
        Draw a circle using Bresenham's algorithm
        """
        x = radius
        y = 0
        err = 0
        
        while x >= y:
            if filled:
                fb.hline(x0 - x, y0 + y, 2 * x, 1)
                fb.hline(x0 - x, y0 - y, 2 * x, 1)
                fb.hline(x0 - y, y0 + x, 2 * y, 1)
                fb.hline(x0 - y, y0 - x, 2 * y, 1)
            else:
                fb.pixel(x0 + x, y0 + y, 1)
                fb.pixel(x0 + y, y0 + x, 1)
                fb.pixel(x0 - y, y0 + x, 1)
                fb.pixel(x0 - x, y0 + y, 1)
                fb.pixel(x0 - x, y0 - y, 1)
                fb.pixel(x0 - y, y0 - x, 1)
                fb.pixel(x0 + y, y0 - x, 1)
                fb.pixel(x0 + x, y0 - y, 1)
            
            if err <= 0:
                y += 1
                err += 2 * y + 1
            
            if err > 0:
                x -= 1
                err -= 2 * x + 1
    
    def _simulate_display(self, moon_data, location_name, last_update):
        """Simulate display output for testing without hardware"""
        import time
        
        print("\n" + "=" * 50)
        print("DISPLAY OUTPUT (Simulated)")
        print("=" * 50)
        print(f"Location: {location_name}")
        
        current_time = time.localtime(last_update)
        print(f"Date: {current_time[1]:02d}/{current_time[2]:02d}/{current_time[0]} " +
              f"{current_time[3]:02d}:{current_time[4]:02d}")
        
        print("\n" + " " * 20 + "[MOON GRAPHIC]")
        print(" " * 20 + "     🌙")
        
        print(f"\nPhase: {moon_data.get('phase_name', 'Unknown')}")
        print(f"Illumination: {moon_data.get('illumination', 0):.1f}%")
        print(f"Moonrise: {moon_data.get('moonrise', 'N/A')}")
        print(f"Moonset: {moon_data.get('moonset', 'N/A')}")
        print("=" * 50 + "\n")
    
    def sleep(self):
        """Put display to sleep to save power"""
        if not self.initialized:
            print("[DISPLAY] Sleep (simulated)")
            return
        
        try:
            self.epd.Sleep()
            print("Display sleeping")
        except Exception as e:
            print(f"Error sleeping display: {e}")
    
    def wake(self):
        """Wake display from sleep"""
        if not self.initialized:
            print("[DISPLAY] Wake (simulated)")
            return
        
        try:
            # Re-initialize the display after sleep
            self.epd.EPD_4IN2_V2_Init()
            print("Display awake")
        except Exception as e:
            print(f"Error waking display: {e}")
