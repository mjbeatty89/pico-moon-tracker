"""
API Client - Fetches moon phase data from RapidAPI
"""
import urequests
import json

class MoonAPIClient:
    def __init__(self, api_key, api_host, latitude, longitude):
        self.api_key = api_key
        self.api_host = api_host
        self.latitude = latitude
        self.longitude = longitude
        self.base_url = "https://moon-phase.p.rapidapi.com/advanced"
    
    def get_moon_data(self):
        """
        Fetch moon phase data from RapidAPI
        Returns: dict with moon data or None if failed
        """
        url = f"{self.base_url}?lat={self.latitude}&lon={self.longitude}"
        
        headers = {
            'x-rapidapi-host': self.api_host,
            'x-rapidapi-key': self.api_key
        }
        
        try:
            print(f"Fetching moon data from API...")
            response = urequests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                response.close()
                print("API call successful")
                return self._parse_response(data)
            else:
                print(f"API error: {response.status_code}")
                response.close()
                return None
                
        except Exception as e:
            print(f"API request failed: {e}")
            return None
    
    def _parse_response(self, data):
        """
        Parse API response and extract relevant moon data
        Returns: dict with standardized moon information
        """
        try:
            # Extract key moon phase information
            moon_data = {
                'phase_name': data.get('phase', {}).get('phase', 'Unknown'),
                'illumination': data.get('phase', {}).get('illumination', 0),
                'age_days': data.get('phase', {}).get('age', 0),
                'distance_km': data.get('distance', {}).get('km', 0),
                'angular_diameter': data.get('angular_diameter', {}).get('degrees', 0),
                'moonrise': data.get('moonrise', 'N/A'),
                'moonset': data.get('moonset', 'N/A'),
                'transit': data.get('transit', 'N/A'),
                'zodiac': data.get('zodiac', {}).get('sign', 'Unknown'),
            }
            
            return moon_data
            
        except Exception as e:
            print(f"Error parsing API response: {e}")
            return None
    
    def test_connection(self):
        """Test API connection and print sample data"""
        print("\n=== Testing API Connection ===")
        data = self.get_moon_data()
        
        if data:
            print("\nMoon Data:")
            for key, value in data.items():
                print(f"  {key}: {value}")
            return True
        else:
            print("API test failed")
            return False
