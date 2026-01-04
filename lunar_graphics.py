"""
Moon Phase Graphics for Pico 2W E-ink Display
Programmatically renders moon phase graphics to match the original Instructables project aesthetic.

Renders 8 moon phases with accurate illumination patterns.
"""

import framebuf
import math

MOON_SIZE = 140  # Diameter in pixels (fits well in 155x152 area)

def draw_circle_filled(fb, x, y, r, color):
    """Draw a filled circle using Bresenham's algorithm"""
    for dy in range(-r, r + 1):
        dx = int(math.sqrt(r * r - dy * dy))
        fb.hline(x - dx, y + dy, 2 * dx + 1, color)

def draw_circle_outline(fb, x, y, r, color):
    """Draw a circle outline"""
    f = 1 - r
    ddF_x = 0
    ddF_y = -2 * r
    x1 = 0
    y1 = r
    
    fb.pixel(x, y + r, color)
    fb.pixel(x, y - r, color)
    fb.pixel(x + r, y, color)
    fb.pixel(x - r, y, color)
    
    while x1 < y1:
        if f >= 0:
            y1 -= 1
            ddF_y += 2
            f += ddF_y
        x1 += 1
        ddF_x += 2
        f += ddF_x + 1
        
        fb.pixel(x + x1, y + y1, color)
        fb.pixel(x - x1, y + y1, color)
        fb.pixel(x + x1, y - y1, color)
        fb.pixel(x - x1, y - y1, color)
        fb.pixel(x + y1, y + x1, color)
        fb.pixel(x - y1, y + x1, color)
        fb.pixel(x + y1, y - x1, color)
        fb.pixel(x - y1, y - x1, color)

def draw_crescent(fb, center_x, center_y, radius, illumination, waxing=True, color=1):
    """
    Draw a crescent moon by drawing two circles and using their overlap.
    
    Args:
        fb: framebuffer to draw on
        center_x, center_y: center of the moon
        radius: radius of the moon
        illumination: percentage illuminated (0-100)
        waxing: True for waxing (right side lit), False for waning (left side lit)
        color: color to draw (1=black, 0=white for most e-ink)
    """
    # Draw full circle outline
    draw_circle_outline(fb, center_x, center_y, radius, color)
    
    # For crescent and gibbous, we need to draw the terminator (shadow line)
    # Calculate the x-offset of the terminator from center
    # illumination 0% = -radius (new moon, terminator at left edge)
    # illumination 50% = 0 (half moon, terminator at center)
    # illumination 100% = +radius (full moon, terminator at right edge)
    
    # Map illumination (0-100) to terminator position (-radius to +radius)
    terminator_x_offset = int((illumination / 50.0 - 1.0) * radius)
    
    if not waxing:
        terminator_x_offset = -terminator_x_offset
    
    # Draw the lit portion (fill from edge to terminator)
    if illumination < 50:  # Crescent
        # Draw the crescent by filling pixels
        for dy in range(-radius, radius + 1):
            y = center_y + dy
            # Calculate the x extent of the circle at this y
            dx_circle = int(math.sqrt(max(0, radius * radius - dy * dy)))
            
            if waxing:
                # Light on right side
                x_start = center_x + terminator_x_offset
                x_end = center_x + dx_circle
            else:
                # Light on left side
                x_start = center_x - dx_circle
                x_end = center_x + terminator_x_offset
            
            if x_end > x_start:
                fb.hline(x_start, y, x_end - x_start + 1, color)
    else:  # Gibbous or full
        # Fill most of circle, leave shadow
        draw_circle_filled(fb, center_x, center_y, radius, color)
        
        if illumination < 100:
            # Draw shadow crescent on opposite side
            for dy in range(-radius, radius + 1):
                y = center_y + dy
                dx_circle = int(math.sqrt(max(0, radius * radius - dy * dy)))
                
                if waxing:
                    # Shadow on left
                    x_start = center_x - dx_circle
                    x_end = center_x + terminator_x_offset
                else:
                    # Shadow on right
                    x_start = center_x + terminator_x_offset
                    x_end = center_x + dx_circle
                
                if x_end > x_start:
                    fb.hline(x_start, y, x_end - x_start + 1, 0)  # 0 = white (shadow)

def render_moon_phase(phase_name):
    """
    Render a moon phase graphic as a framebuffer.
    
    Args:
        phase_name: One of 'New', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous',
                   'Full', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent'
    
    Returns:
        framebuffer.FrameBuffer object (155x152, MONO_HLSB format)
    """
    # Create framebuffer (155x152 pixels, 1-bit monochrome)
    width, height = 155, 152
    buffer = bytearray((width * height) // 8 + 1)
    fb = framebuf.FrameBuffer(buffer, width, height, framebuf.MONO_HLSB)
    
    # Clear to white
    fb.fill(0)
    
    # Moon center and radius
    center_x = width // 2
    center_y = height // 2
    radius = MOON_SIZE // 2
    
    # Render based on phase
    phase_lower = phase_name.lower()
    
    if 'new' in phase_lower:
        # New moon - just outline
        draw_circle_outline(fb, center_x, center_y, radius, 1)
        
    elif 'full' in phase_lower:
        # Full moon - filled circle
        draw_circle_filled(fb, center_x, center_y, radius, 1)
        draw_circle_outline(fb, center_x, center_y, radius, 1)
        
    elif 'first' in phase_lower or 'waxing half' in phase_lower:
        # First quarter - right half lit
        draw_crescent(fb, center_x, center_y, radius, 50, waxing=True)
        
    elif 'last' in phase_lower or 'waning half' in phase_lower or 'third' in phase_lower:
        # Last quarter - left half lit
        draw_crescent(fb, center_x, center_y, radius, 50, waxing=False)
        
    elif 'waxing crescent' in phase_lower:
        # Waxing crescent - ~25% lit, right side
        draw_crescent(fb, center_x, center_y, radius, 25, waxing=True)
        
    elif 'waxing gibbous' in phase_lower:
        # Waxing gibbous - ~75% lit, right side
        draw_crescent(fb, center_x, center_y, radius, 75, waxing=True)
        
    elif 'waning gibbous' in phase_lower:
        # Waning gibbous - ~75% lit, left side
        draw_crescent(fb, center_x, center_y, radius, 75, waxing=False)
        
    elif 'waning crescent' in phase_lower:
        # Waning crescent - ~25% lit, left side
        draw_crescent(fb, center_x, center_y, radius, 25, waxing=False)
    
    else:
        # Unknown phase - draw full moon as fallback
        draw_circle_filled(fb, center_x, center_y, radius, 1)
        draw_circle_outline(fb, center_x, center_y, radius, 1)
    
    return fb, buffer

# Pre-render common phases for faster access (optional)
def get_phase_buffer(phase_name):
    """
    Get a pre-rendered moon phase buffer.
    
    Args:
        phase_name: Phase name (e.g., 'Full', 'New', 'Waxing Crescent', etc.)
    
    Returns:
        tuple: (framebuffer, buffer_bytes)
    """
    return render_moon_phase(phase_name)
