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
            
            # Clear the built-in framebuffer to white
            # For MONO_HLSB: 0x00 = white, 0xff = black
            self.epd.image1Gray.fill(0x00)  # Fill with white background
            
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
        
        Layout (400x300 pixels):
        - Left half (0-200): Text information
        - Right half (200-400): Large centered moon graphic
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
        
        # LEFT SIDE: Text information
        left_x = 10
        
        # Location at top
        self._draw_text(fb, location_name, left_x, 10, 1)
        
        # Date and time
        self._draw_text(fb, date_str, left_x, 30, 1)
        self._draw_text(fb, time_str, left_x, 45, 1)
        
        # Moon phase information
        self._draw_text(fb, "Phase:", left_x, 80, 1)
        self._draw_text(fb, phase_name, left_x, 95, 1)
        
        self._draw_text(fb, "Illumination:", left_x, 130, 1)
        self._draw_text(fb, f"{illumination:.1f}%", left_x, 145, 1)
        
        self._draw_text(fb, "Moonrise:", left_x, 180, 1)
        self._draw_text(fb, moonrise, left_x, 195, 1)
        
        self._draw_text(fb, "Moonset:", left_x, 230, 1)
        self._draw_text(fb, moonset, left_x, 245, 1)
        
        # RIGHT SIDE: Large moon graphic centered
        # Center of right half: x=300, y=150
        moon_center_x = 300
        moon_center_y = 150
        moon_radius = 80  # Larger radius
        self._draw_moon_phase_graphic(fb, phase_name, moon_center_x, moon_center_y, moon_radius)
    
    def _draw_text(self, fb, text, x, y, scale=1):
        """
        Draw text on framebuffer
        Note: MicroPython's framebuf has basic text support (8x8 font)
        For MONO_HLSB: color 1 = black (foreground), 0 = white (background)
        """
        try:
            fb.text(text, x, y, 1)  # Draw black text on white background
        except Exception as e:
            print(f"Error drawing text: {e}")
    
    def _draw_moon_phase_graphic(self, fb, phase_name, center_x, center_y, radius=50):
        """
        Draw a simple moon phase graphic
        For a real implementation, you'd load pre-rendered bitmaps
        
        Args:
            fb: framebuffer
            phase_name: name of the moon phase
            center_x: x coordinate of center
            center_y: y coordinate of center
            radius: radius of the moon circle (default 50)
        """
        # Draw moon circle outline
        self._draw_circle(fb, center_x, center_y, radius, filled=False)
        
        # Draw a filled circle for the moon body
        self._draw_circle(fb, center_x, center_y, radius - 2, filled=True)
        
        # For simplicity, we'll use text representation in the center
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
        # Center the symbol (approximate)
        self._draw_text(fb, symbol, center_x - 4, center_y - 4, 1)
    
    def _draw_circle(self, fb, x0, y0, radius, filled=False):
        """
        Draw a circle using Bresenham's algorithm
        Color 1 = black pixels
        """
        x = radius
        y = 0
        err = 0
        
        while x >= y:
            if filled:
                fb.hline(x0 - x, y0 + y, 2 * x, 1)  # Black fill
                fb.hline(x0 - x, y0 - y, 2 * x, 1)
                fb.hline(x0 - y, y0 + x, 2 * y, 1)
                fb.hline(x0 - y, y0 - x, 2 * y, 1)
            else:
                fb.pixel(x0 + x, y0 + y, 1)  # Black outline
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
