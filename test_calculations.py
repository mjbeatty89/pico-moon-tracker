"""
Test Script for Moon Calculations
Run this on your development machine (not on Pico) to validate calculations

Note: This won't work directly on MicroPython due to some library differences,
but the core logic is the same. Use this for development validation.
"""

import time
import math

def test_moon_calculations():
    """Test the moon calculation algorithms"""
    
    print("=" * 60)
    print("Testing Moon Phase Calculations")
    print("=" * 60)
    
    # Current time
    current_timestamp = time.time()
    
    # Test data from known moon phases (approximate)
    test_cases = [
        # (timestamp, expected_phase, description)
        (1735689600, "Waxing Crescent", "January 1, 2025 - Known Waxing Crescent"),
        # Add more test cases as needed
    ]
    
    # Julian date conversion
    jd = (current_timestamp / 86400.0) + 2440587.5
    print(f"\nCurrent Julian Date: {jd:.2f}")
    
    # Moon age calculation
    known_new_moon_jd = 2451550.26
    synodic_month = 29.53058867
    days_since_known = jd - known_new_moon_jd
    age = days_since_known % synodic_month
    
    print(f"Moon Age: {age:.2f} days")
    
    # Illumination
    phase_angle = (age / synodic_month) * 2 * math.pi
    illumination = (1 - math.cos(phase_angle)) / 2 * 100
    
    print(f"Illumination: {illumination:.2f}%")
    
    # Phase name
    phase = age / synodic_month
    
    if phase < 0.033 or phase > 0.967:
        phase_name = "New Moon"
    elif 0.033 <= phase < 0.216:
        phase_name = "Waxing Crescent"
    elif 0.216 <= phase < 0.283:
        phase_name = "First Quarter"
    elif 0.283 <= phase < 0.467:
        phase_name = "Waxing Gibbous"
    elif 0.467 <= phase < 0.533:
        phase_name = "Full Moon"
    elif 0.533 <= phase < 0.717:
        phase_name = "Waning Gibbous"
    elif 0.717 <= phase < 0.783:
        phase_name = "Last Quarter"
    else:
        phase_name = "Waning Crescent"
    
    print(f"Phase Name: {phase_name}")
    
    # Moon emoji
    phase_emojis = {
        "New Moon": "🌑",
        "Waxing Crescent": "🌒",
        "First Quarter": "🌓",
        "Waxing Gibbous": "🌔",
        "Full Moon": "🌕",
        "Waning Gibbous": "🌖",
        "Last Quarter": "🌗",
        "Waning Crescent": "🌘"
    }
    
    emoji = phase_emojis.get(phase_name, "🌙")
    print(f"Visual: {emoji}")
    
    # Approximate rise/set times
    base_rise = 6.0
    base_set = 18.0
    time_shift = (age * 50) / 60
    
    moonrise_hour = (base_rise + time_shift) % 24
    moonset_hour = (base_set + time_shift) % 24
    
    def format_time(hour_decimal):
        hours = int(hour_decimal)
        minutes = int((hour_decimal - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"
    
    print(f"Moonrise (approx): {format_time(moonrise_hour)}")
    print(f"Moonset (approx): {format_time(moonset_hour)}")
    
    print("\n" + "=" * 60)
    print("Calculation test complete!")
    print("=" * 60)

def simulate_display_output():
    """Simulate what will appear on the e-Paper display"""
    print("\n" + "=" * 60)
    print("Simulated E-Paper Display Output")
    print("=" * 60)
    print()
    print("  Ann Arbor, MI")
    print(f"  {time.strftime('%m/%d/%Y %H:%M')}")
    print()
    print(" " * 20 + "🌙")
    print(" " * 15 + "[MOON PHASE]")
    print()
    print("  Waxing Crescent")
    print("  Illumination: 23.4%")
    print("  Rise: 09:15  Set: 22:45")
    print()
    print("=" * 60)

if __name__ == "__main__":
    test_moon_calculations()
    print()
    simulate_display_output()
    
    print("\n💡 Tip: Compare these results with:")
    print("   - https://www.timeanddate.com/moon/phases/")
    print("   - Your RapidAPI Moon Phase endpoint")
