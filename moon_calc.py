"""
Moon Calculations - Local astronomical algorithms for moon phase calculations
Based on Jean Meeus "Astronomical Algorithms" and simplified formulas
"""
import math
import time

class MoonCalculator:
    def __init__(self, latitude, longitude, timezone_offset):
        self.latitude = latitude
        self.longitude = longitude
        self.timezone_offset = timezone_offset  # Hours from UTC
    
    def calculate_moon_phase(self, timestamp=None):
        """
        Calculate current moon phase using astronomical algorithms
        Returns: dict with phase information
        """
        if timestamp is None:
            timestamp = time.time()
        
        # Convert to Julian Date
        jd = self._timestamp_to_julian(timestamp)
        
        # Calculate moon age in days since new moon
        age_days = self._calculate_moon_age(jd)
        
        # Calculate illumination percentage
        illumination = self._calculate_illumination(age_days)
        
        # Determine phase name
        phase_name = self._get_phase_name(age_days)
        
        # Calculate moonrise and moonset times
        moonrise, moonset = self._calculate_rise_set(jd)
        
        return {
            'phase_name': phase_name,
            'illumination': round(illumination, 2),
            'age_days': round(age_days, 2),
            'moonrise': moonrise,
            'moonset': moonset,
            'timestamp': timestamp
        }
    
    def _timestamp_to_julian(self, timestamp):
        """Convert Unix timestamp to Julian Date"""
        # Unix epoch (1970-01-01) is JD 2440587.5
        return (timestamp / 86400.0) + 2440587.5
    
    def _calculate_moon_age(self, jd):
        """
        Calculate moon's age in days since last new moon
        Uses a simplified formula accurate to about 1 day
        """
        # Known new moon: January 6, 2000, 18:14 UTC (JD 2451550.26)
        known_new_moon_jd = 2451550.26
        
        # Synodic month (new moon to new moon) = 29.53058867 days
        synodic_month = 29.53058867
        
        # Calculate days since known new moon
        days_since_known = jd - known_new_moon_jd
        
        # Calculate age within current cycle
        age = days_since_known % synodic_month
        
        return age
    
    def _calculate_illumination(self, age_days):
        """
        Calculate moon illumination percentage based on age
        0% = New Moon, 100% = Full Moon
        """
        synodic_month = 29.53058867
        
        # Phase angle (0 to 2*pi)
        phase_angle = (age_days / synodic_month) * 2 * math.pi
        
        # Illumination formula: (1 - cos(angle)) / 2
        illumination = (1 - math.cos(phase_angle)) / 2 * 100
        
        return illumination
    
    def _get_phase_name(self, age_days):
        """
        Determine moon phase name based on age in days
        """
        synodic_month = 29.53058867
        
        # Normalize to 0-1 range
        phase = age_days / synodic_month
        
        # Define phase boundaries
        if phase < 0.033 or phase > 0.967:
            return "New Moon"
        elif 0.033 <= phase < 0.216:
            return "Waxing Crescent"
        elif 0.216 <= phase < 0.283:
            return "First Quarter"
        elif 0.283 <= phase < 0.467:
            return "Waxing Gibbous"
        elif 0.467 <= phase < 0.533:
            return "Full Moon"
        elif 0.533 <= phase < 0.717:
            return "Waning Gibbous"
        elif 0.717 <= phase < 0.783:
            return "Last Quarter"
        else:  # 0.783 <= phase < 0.967
            return "Waning Crescent"
    
    def _calculate_rise_set(self, jd):
        """
        Calculate moonrise and moonset times (simplified approximation)
        Returns times in HH:MM format (local time)
        """
        # This is a very simplified calculation
        # For production, consider using a proper ephemeris library
        
        age_days = self._calculate_moon_age(jd)
        synodic_month = 29.53058867
        
        # Moon rises approximately 50 minutes later each day
        # At new moon, rises/sets with sun (~6am/6pm)
        # At full moon, rises at sunset and sets at sunrise
        
        # Base times (in hours, 24h format)
        base_rise = 6.0  # 6 AM for new moon
        base_set = 18.0  # 6 PM for new moon
        
        # Shift based on moon age (50 minutes per day = 0.833 hours)
        time_shift = (age_days * 50) / 60  # Convert minutes to hours
        
        moonrise_hour = (base_rise + time_shift) % 24
        moonset_hour = (base_set + time_shift) % 24
        
        # Apply timezone offset
        moonrise_hour = (moonrise_hour + self.timezone_offset) % 24
        moonset_hour = (moonset_hour + self.timezone_offset) % 24
        
        # Format as HH:MM
        moonrise = self._format_time(moonrise_hour)
        moonset = self._format_time(moonset_hour)
        
        return moonrise, moonset
    
    def _format_time(self, hour_decimal):
        """Convert decimal hours to HH:MM format"""
        hours = int(hour_decimal)
        minutes = int((hour_decimal - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"
    
    def get_phase_emoji(self, phase_name):
        """
        Get emoji representation of moon phase
        Useful for simple displays
        """
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
        return phase_emojis.get(phase_name, "🌙")
    
    def compare_with_api(self, local_data, api_data):
        """
        Compare local calculation with API data
        Returns: dict with comparison results
        """
        if not api_data:
            return None
        
        illumination_diff = abs(local_data['illumination'] - api_data['illumination'])
        age_diff = abs(local_data['age_days'] - api_data['age_days'])
        
        comparison = {
            'illumination_match': illumination_diff < 5.0,  # Within 5%
            'illumination_diff': round(illumination_diff, 2),
            'age_match': age_diff < 0.5,  # Within 12 hours
            'age_diff': round(age_diff, 2),
            'phase_name_match': local_data['phase_name'] == api_data['phase_name']
        }
        
        return comparison
