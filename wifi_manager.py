"""
WiFi Manager - Handles WiFi connection and NTP time synchronization
"""
import network
import time
import ntptime
from machine import RTC

class WiFiManager:
    def __init__(self, ssid, password, timeout=10):
        self.ssid = ssid
        self.password = password
        self.timeout = timeout
        self.wlan = network.WLAN(network.STA_IF)
        self.rtc = RTC()
        
    def connect(self):
        """Connect to WiFi network"""
        if self.is_connected():
            print(f"Already connected to {self.ssid}")
            return True
        
        print(f"Connecting to WiFi: {self.ssid}")
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        
        # Wait for connection
        start_time = time.time()
        while not self.wlan.isconnected():
            if time.time() - start_time > self.timeout:
                print("WiFi connection timeout")
                return False
            time.sleep(0.5)
            print(".", end="")
        
        print(f"\nConnected! IP: {self.wlan.ifconfig()[0]}")
        return True
    
    def disconnect(self):
        """Disconnect from WiFi to save power"""
        if self.wlan.isconnected():
            self.wlan.disconnect()
        self.wlan.active(False)
        print("WiFi disconnected")
    
    def is_connected(self):
        """Check if WiFi is connected"""
        return self.wlan.isconnected()
    
    def sync_time_ntp(self, retries=3):
        """
        Synchronize time with NTP server
        Returns: timestamp if successful, None if failed
        """
        if not self.is_connected():
            print("Cannot sync NTP: not connected to WiFi")
            return None
        
        for attempt in range(retries):
            try:
                print(f"Syncing time with NTP (attempt {attempt + 1}/{retries})...")
                ntptime.settime()
                
                # Get current time from RTC
                current_time = time.time()
                print(f"NTP sync successful! Current time: {time.localtime(current_time)}")
                return current_time
                
            except Exception as e:
                print(f"NTP sync failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2)
        
        return None
    
    def get_rssi(self):
        """Get WiFi signal strength (RSSI)"""
        if self.is_connected():
            # Note: RSSI method may not be available on all MicroPython versions
            try:
                return self.wlan.status('rssi')
            except:
                return None
        return None
    
    def scan_networks(self):
        """Scan for available WiFi networks"""
        self.wlan.active(True)
        networks = self.wlan.scan()
        return networks
