"""
Storage Manager - Handles persistent data on flash storage
Stores last sync times, time offsets, and other state data
"""
import json
import os

STORAGE_FILE = "moon_tracker_data.json"

class Storage:
    def __init__(self):
        self.data = self._load()
    
    def _load(self):
        """Load data from flash storage"""
        try:
            with open(STORAGE_FILE, 'r') as f:
                return json.load(f)
        except (OSError, ValueError):
            # File doesn't exist or is corrupted, return defaults
            return {
                'last_ntp_sync': 0,
                'last_api_sync': 0,
                'time_offset': 0,
                'boot_time': 0,
            }
    
    def save(self):
        """Save data to flash storage"""
        try:
            with open(STORAGE_FILE, 'w') as f:
                json.dump(self.data, f)
            return True
        except OSError as e:
            print(f"Error saving storage: {e}")
            return False
    
    def get(self, key, default=None):
        """Get a value from storage"""
        return self.data.get(key, default)
    
    def set(self, key, value):
        """Set a value in storage and save"""
        self.data[key] = value
        return self.save()
    
    def get_last_ntp_sync(self):
        """Get the timestamp of the last NTP sync"""
        return self.data.get('last_ntp_sync', 0)
    
    def set_last_ntp_sync(self, timestamp):
        """Record NTP sync time"""
        return self.set('last_ntp_sync', timestamp)
    
    def get_last_api_sync(self):
        """Get the timestamp of the last API sync"""
        return self.data.get('last_api_sync', 0)
    
    def set_last_api_sync(self, timestamp):
        """Record API sync time"""
        return self.set('last_api_sync', timestamp)
    
    def get_boot_time(self):
        """Get the boot timestamp for time tracking"""
        return self.data.get('boot_time', 0)
    
    def set_boot_time(self, timestamp):
        """Record boot time for offline time calculation"""
        return self.set('boot_time', timestamp)
    
    def clear_all(self):
        """Clear all stored data"""
        self.data = {
            'last_ntp_sync': 0,
            'last_api_sync': 0,
            'time_offset': 0,
            'boot_time': 0,
        }
        return self.save()
