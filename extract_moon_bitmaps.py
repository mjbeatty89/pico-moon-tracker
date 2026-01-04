#!/usr/bin/env python3
"""
Extract moon phase bitmaps from the Instructables fontLunar.c file.
Converts C hex arrays to Python bytes format for MicroPython e-ink display.

The original font file contains 155x152 pixel moon phase bitmaps stored as:
- 152 rows per image
- 20 bytes per row (155 pixels / 8 = 19.375, rounded up to 20)
- Each character is a complete moon phase image

Phase mapping (from Arduino code):
- ' ' (space, ASCII 32) = Full Moon
- '!' (ASCII 33) = New Moon
- '%' (ASCII 37) = Waxing Crescent
- '(' (ASCII 40) = Last Quarter (Waning Half)
- '*' (ASCII 42) = Waxing Gibbous
- '3' (ASCII 51) = Waning Gibbous
- '5' (ASCII 53) = First Quarter (Waxing Half)
- '7' (ASCII 55) = Waning Crescent
"""

import re

def extract_bitmaps():
    """Extract moon phase bitmaps from fontLunar.c"""
    
    # Read the source file
    with open('F9ECFA7JGSG75F7/EPD-master/fontLunar.c', 'r') as f:
        content = f.read()
    
    # Split into lines for processing
    lines = content.split('\n')
    
    # Find all character markers
    char_starts = []
    for i, line in enumerate(lines):
        if '@' in line and 'pixels wide' in line:
            # Extract character code
            match = re.search(r"'(.)'", line)
            if match:
                char = match.group(1)
                char_starts.append((i, char, line))
    
    print(f"Found {len(char_starts)} characters in font file")
    
    # Characters we need for moon phases
    needed_chars = {' ': 'Full', '!': 'New', '%': 'WaxingCrescent', '(': 'LastQuarter',
                   '*': 'WaxingGibbous', '3': 'WaningGibbous', '5': 'FirstQuarter', '7': 'WaningCrescent'}
    
    extracted = {}
    
    # Extract bitmap data for each needed character
    for char, phase_name in needed_chars.items():
        print(f"\nSearching for character '{char}' (ASCII {ord(char)}) - {phase_name}")
        
        # Find this character in the font
        found_idx = None
        for idx, (line_num, found_char, line_text) in enumerate(char_starts):
            if found_char == char:
                found_idx = idx
                print(f"  Found at line {line_num}")
                break
        
        if found_idx is None:
            print(f"  WARNING: Character '{char}' not found in font file!")
            continue
        
        # Extract 152 lines of hex data starting from the marker
        start_line = char_starts[found_idx][0] + 1
        end_line = char_starts[found_idx + 1][0] if found_idx + 1 < len(char_starts) else len(lines)
        
        # Parse hex bytes from lines
        bitmap_bytes = []
        for line_idx in range(start_line, min(start_line + 152, end_line)):
            line = lines[line_idx]
            # Extract hex values: 0xAB, 0xCD, ...
            hex_values = re.findall(r'0x([0-9A-Fa-f]{2})', line)
            if hex_values:
                # Take only first 20 bytes per row (155 pixels / 8 bits = 19.375 -> 20 bytes)
                for hex_val in hex_values[:20]:
                    bitmap_bytes.append(int(hex_val, 16))
        
        print(f"  Extracted {len(bitmap_bytes)} bytes ({len(bitmap_bytes)//20} rows)")
        extracted[phase_name] = bytes(bitmap_bytes)
    
    return extracted

def write_python_module(bitmaps):
    """Write extracted bitmaps to lunar_graphics.py module"""
    
    with open('lunar_graphics.py', 'w') as f:
        f.write('''"""
Moon Phase Bitmap Graphics for Pico 2W E-ink Display
Extracted from Instructables Lunar Phase Tracker project.

Each bitmap is 155 pixels wide x 152 pixels tall (20 bytes x 152 rows = 3040 bytes).
Format: 1-bit monochrome, MSB first, row-major order.

Original source: https://www.instructables.com/Lunar-Phase-Tracker/
"""

BITMAP_WIDTH = 155  # pixels
BITMAP_HEIGHT = 152  # pixels
BYTES_PER_ROW = 20  # (155 + 7) // 8

''')
        
        # Write each bitmap
        for phase_name, bitmap_data in sorted(bitmaps.items()):
            f.write(f"\n# {phase_name} Moon\n")
            f.write(f"BITMAP_{phase_name.upper()} = bytes([\n")
            
            # Write bytes in rows of 20 for readability
            for row in range(0, len(bitmap_data), 20):
                row_bytes = bitmap_data[row:row+20]
                hex_str = ', '.join(f'0x{b:02X}' for b in row_bytes)
                f.write(f"    {hex_str},\n")
            
            f.write("])\n")
        
        # Write lookup function
        f.write('''
def get_phase_bitmap(phase_name):
    """
    Get bitmap for a moon phase.
    
    Args:
        phase_name: One of 'Full', 'New', 'Waxing Crescent', 'First Quarter',
                   'Waxing Gibbous', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent'
    
    Returns:
        bytes object containing the bitmap data (3040 bytes)
    """
    phase_map = {
        'Full': BITMAP_FULL,
        'Full Moon': BITMAP_FULL,
        'New': BITMAP_NEW,
        'New Moon': BITMAP_NEW,
        'Waxing Crescent': BITMAP_WAXINGCRESCENT,
        'First Quarter': BITMAP_FIRSTQUARTER,
        'Waxing Half': BITMAP_FIRSTQUARTER,  # Alias
        'Waxing Gibbous': BITMAP_WAXINGGIBBOUS,
        'Waning Gibbous': BITMAP_WANINGGIBBOUS,
        'Last Quarter': BITMAP_LASTQUARTER,
        'Waning Half': BITMAP_LASTQUARTER,  # Alias
        'Waning Crescent': BITMAP_WANINGCRESCENT,
    }
    
    return phase_map.get(phase_name)
''')

    print(f"\nWrote lunar_graphics.py with {len(bitmaps)} moon phase bitmaps")

if __name__ == '__main__':
    print("Extracting moon phase bitmaps from fontLunar.c...")
    bitmaps = extract_bitmaps()
    
    if bitmaps:
        write_python_module(bitmaps)
        print("\n✓ Complete! Generated lunar_graphics.py")
        
        # Calculate total size
        total_bytes = sum(len(b) for b in bitmaps.values())
        print(f"  Total size: {total_bytes} bytes ({total_bytes/1024:.1f} KB)")
    else:
        print("\n✗ Failed to extract bitmaps")
