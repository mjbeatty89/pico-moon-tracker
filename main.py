"""
Pico 2W Moon Phase Tracker - Main Application
Displays current moon phase on Waveshare 4.2" e-Paper display
"""
import time
import machine
import gc

# Import our modules
from storage import Storage
from wifi_manager import WiFiManager
from api_client import MoonAPIClient
from moon_calc import MoonCalculator
from display_manager import DisplayManager

# Import config (must be created from config.py.example)
try:
    import config
except ImportError:
    print("ERROR: config.py not found!")
    print("Please copy config.py.example to config.py and fill in your settings.")
    raise

class MoonTracker:
    def __init__(self):
        """Initialize the moon tracker system"""
        print("\n" + "=" * 50)
        print("Pico 2W Moon Phase Tracker")
        print("=" * 50 + "\n")
        
        # Initialize components
        self.storage = Storage()
        self.wifi = WiFiManager(config.WIFI_SSID, config.WIFI_PASSWORD)
        self.api_client = MoonAPIClient(
            config.RAPIDAPI_KEY,
            config.RAPIDAPI_HOST,
            config.LATITUDE,
            config.LONGITUDE
        )
        self.moon_calc = MoonCalculator(
            config.LATITUDE,
            config.LONGITUDE,
            config.TIMEZONE_OFFSET
        )
        self.display = DisplayManager()
        
        self.last_phase_name = None  # Track phase changes
        
        # Setup complete
        print("Initialization complete\n")
    
    def run(self):
        """Main run loop"""
        # Initial setup
        self.initial_sync()
        
        # Main loop
        loop_count = 0
        while True:
            try:
                loop_count += 1
                print(f"\n--- Update Cycle {loop_count} ---")
                
                # Calculate current moon phase locally
                moon_data = self.moon_calc.calculate_moon_phase()
                
                if config.DEBUG:
                    print(f"Local calculation: {moon_data['phase_name']} " +
                          f"({moon_data['illumination']:.1f}%)")
                
                # Check if we need API verification (once per day)
                if self._should_sync_api():
                    self._sync_with_api(moon_data)
                
                # Update display
                self.display.draw_moon_data(
                    moon_data,
                    config.LOCATION_NAME,
                    time.time()
                )
                
                # Store last phase for change detection
                self.last_phase_name = moon_data['phase_name']
                
                # Memory cleanup
                gc.collect()
                
                # Sleep until next update
                print(f"Sleeping for {config.LOCAL_UPDATE_INTERVAL} seconds...")
                
                if config.ENABLE_DEEP_SLEEP:
                    self._deep_sleep(config.LOCAL_UPDATE_INTERVAL)
                else:
                    time.sleep(config.LOCAL_UPDATE_INTERVAL)
                
            except KeyboardInterrupt:
                print("\n\nShutdown requested by user")
                self.shutdown()
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                print("Waiting 60 seconds before retry...")
                time.sleep(60)
    
    def initial_sync(self):
        """Perform initial WiFi and time synchronization"""
        print("=== Initial Setup ===")
        
        # Connect to WiFi
        if self.wifi.connect():
            # Sync time with NTP
            ntp_time = self.wifi.sync_time_ntp()
            if ntp_time:
                self.storage.set_last_ntp_sync(ntp_time)
                self.storage.set_boot_time(ntp_time)
                print(f"Time synced: {time.localtime(ntp_time)}")
            
            # Optional: Do initial API call for verification
            if config.DEBUG:
                print("\nTesting API connection...")
                api_data = self.api_client.get_moon_data()
                if api_data:
                    print("API test successful!")
                    self.storage.set_last_api_sync(time.time())
            
            # Disconnect WiFi to save power (will reconnect for daily sync)
            # self.wifi.disconnect()
        else:
            print("WARNING: WiFi connection failed")
            print("Will use local calculations only")
        
        print("=== Setup Complete ===\n")
    
    def _should_sync_api(self):
        """Check if it's time for daily API verification"""
        last_sync = self.storage.get_last_api_sync()
        current_time = time.time()
        
        # Sync if more than API_UPDATE_INTERVAL has passed
        time_since_sync = current_time - last_sync
        return time_since_sync >= config.API_UPDATE_INTERVAL
    
    def _sync_with_api(self, local_data):
        """Perform API sync and compare with local calculation"""
        print("\n=== Daily API Verification ===")
        
        # Reconnect to WiFi if needed
        if not self.wifi.is_connected():
            if not self.wifi.connect():
                print("WiFi connection failed, skipping API sync")
                return
        
        # Fetch API data
        api_data = self.api_client.get_moon_data()
        
        if api_data:
            # Compare with local calculation
            comparison = self.moon_calc.compare_with_api(local_data, api_data)
            
            if config.DEBUG and comparison:
                print(f"Illumination difference: {comparison['illumination_diff']:.2f}%")
                print(f"Age difference: {comparison['age_diff']:.2f} days")
                print(f"Phase match: {comparison['phase_name_match']}")
            
            # Update last sync time
            self.storage.set_last_api_sync(time.time())
            
            # Also re-sync NTP time while we're connected
            ntp_time = self.wifi.sync_time_ntp()
            if ntp_time:
                self.storage.set_last_ntp_sync(ntp_time)
        
        # Disconnect to save power
        # self.wifi.disconnect()
        
        print("=== API Sync Complete ===\n")
    
    def _deep_sleep(self, duration):
        """
        Enter deep sleep mode (for battery operation)
        Note: Pico will reset on wake from deep sleep
        """
        print("Entering deep sleep mode...")
        self.display.sleep()
        
        # Convert duration to milliseconds
        duration_ms = duration * 1000
        
        # Configure wake timer and enter deep sleep
        machine.deepsleep(duration_ms)
    
    def shutdown(self):
        """Clean shutdown"""
        print("Shutting down...")
        self.display.sleep()
        self.wifi.disconnect()
        print("Goodbye!")

# Main entry point
if __name__ == "__main__":
    try:
        tracker = MoonTracker()
        tracker.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import sys
        sys.print_exception(e)
