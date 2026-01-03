# Deployment Checklist

Use this checklist when setting up a new Pico 2W Moon Tracker.

## Pre-Deployment Setup

### Hardware Assembly
- [ ] Pico 2W received and tested
- [ ] Waveshare 4.2" e-Paper display received
- [ ] Display seated firmly on Pico headers
- [ ] (Optional) Battery and PowerBoost 500C installed
- [ ] USB cable connected, Pico powers on

### Software Preparation
- [ ] MicroPython firmware downloaded for Pico 2W
- [ ] Thonny IDE installed on computer
- [ ] Waveshare `epd4in2.py` driver downloaded
- [ ] RapidAPI account created
- [ ] Moon Phase API key obtained (free tier)

## Configuration

### Create Config File
- [ ] Copy `config.py.example` to `config.py`
- [ ] Set `WIFI_SSID` to recipient's WiFi name
- [ ] Set `WIFI_PASSWORD` to WiFi password
- [ ] Set `RAPIDAPI_KEY` to your API key
- [ ] Verify `LATITUDE` and `LONGITUDE` for location
- [ ] Set `LOCATION_NAME` (e.g., "Ann Arbor, MI")
- [ ] Set `TIMEZONE_OFFSET` (EST=-5, EDT=-4, etc.)
- [ ] Set `DEBUG = False` for quiet operation
- [ ] Set `ENABLE_DEEP_SLEEP = True` if battery powered

### Example Config Values
```python
# Ann Arbor, MI
LATITUDE = 42.2808
LONGITUDE = -83.7430
TIMEZONE_OFFSET = -5  # EST

# Los Angeles, CA
LATITUDE = 34.0522
LONGITUDE = -118.2437
TIMEZONE_OFFSET = -8  # PST

# New York, NY
LATITUDE = 40.7128
LONGITUDE = -74.0060
TIMEZONE_OFFSET = -5  # EST
```

## Pico 2W Setup

### Flash MicroPython
- [ ] Hold BOOTSEL button on Pico
- [ ] Connect USB cable
- [ ] Drag MicroPython .uf2 file to RPI-RP2 drive
- [ ] Wait for Pico to reboot
- [ ] Verify Pico shows up in Thonny

### Upload Files to Pico
- [ ] Open Thonny, connect to Pico
- [ ] Upload `config.py` (with your settings)
- [ ] Upload `main.py`
- [ ] Upload `moon_calc.py`
- [ ] Upload `display_manager.py`
- [ ] Upload `wifi_manager.py`
- [ ] Upload `api_client.py`
- [ ] Upload `storage.py`

### Install Display Driver
- [ ] Create `lib` folder on Pico
- [ ] Upload `epd4in2.py` to `lib/` folder
- [ ] Verify file is in `/lib/epd4in2.py` on Pico

## Testing

### Initial Boot Test
- [ ] Reset Pico (or run main.py)
- [ ] Watch console output
- [ ] Verify WiFi connection message appears
- [ ] Verify NTP time sync successful
- [ ] Verify moon phase calculated
- [ ] Check for any error messages

### Display Test
- [ ] Display should update within 30 seconds
- [ ] Verify location name appears
- [ ] Verify date/time looks correct
- [ ] Verify moon phase name shown
- [ ] Verify illumination percentage displayed
- [ ] Check moonrise/moonset times are reasonable

### API Test (Optional)
If `DEBUG = True` in config:
- [ ] Watch for "Testing API connection" message
- [ ] Verify API call successful
- [ ] Compare API data with local calculation
- [ ] Should be within a few percent

## 24-Hour Soak Test

### Leave Running
- [ ] Let Pico run for 24+ hours
- [ ] Check periodically for errors
- [ ] Verify display updates hourly
- [ ] Verify daily API sync occurs
- [ ] Check WiFi reconnection after sleep

### Battery Test (if applicable)
- [ ] Unplug USB power
- [ ] Verify runs on battery
- [ ] Check battery life over 24 hours
- [ ] Verify charging works when plugged in
- [ ] Monitor for any power issues

## Final Preparation (Gift)

### Cosmetic Setup
- [ ] Clean display with soft cloth
- [ ] Tidy up any loose wires
- [ ] Mount in frame or enclosure (optional)
- [ ] Add rubber feet or stand
- [ ] Prepare USB cable with strain relief

### Documentation Package
- [ ] Print or include README.md
- [ ] Include WiFi change instructions
- [ ] Note API key info (if sharing)
- [ ] Include troubleshooting tips
- [ ] Add your contact info for support

### Gift Presentation
- [ ] Box or wrap thoughtfully
- [ ] Include setup instructions if WiFi needs changing
- [ ] Add personal note about moon significance
- [ ] Maybe include moon calendar or astronomy book
- [ ] Test one final time before gifting

## Troubleshooting Quick Reference

### Won't Connect to WiFi
```python
# Common fixes in config.py:
WIFI_SSID = "correct_network_name"  # Case sensitive!
# Ensure 2.4GHz network (not 5GHz)
```

### Wrong Time Displayed
```python
# Adjust timezone in config.py:
TIMEZONE_OFFSET = -5  # Your timezone offset from UTC
```

### Display Not Updating
- Check `lib/epd4in2.py` is present
- Verify display seated properly
- Try reset (unplug/replug USB)
- Check console for errors

### Battery Dies Too Fast
```python
# Enable deep sleep in config.py:
ENABLE_DEEP_SLEEP = True
SLEEP_DURATION = 3600  # 1 hour
```

## Support Resources

- **GitHub Issues**: Report bugs or ask questions
- **Waveshare Wiki**: Display technical documentation
- **MicroPython Forum**: General programming help
- **RapidAPI Dashboard**: Monitor API usage

## Post-Deployment Notes

Location: _________________
WiFi Network: _________________
Deployed Date: _________________
API Key Used: ________-_____ (last 5 digits)
Battery Installed: Yes / No
Special Configuration: _________________

---

**Pro Tip**: Take a photo of the working display before gifting - shows you care and helps troubleshooting later!
