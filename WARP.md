# Pico 2W Moon Phase Tracker - Project Rules

## Project Overview
A standalone lunar phase tracker using Raspberry Pi Pico 2W and Waveshare 4.2" e-Paper display. This is a gift project, so code should be well-documented and easy to maintain.

## Hardware Target
- **MCU**: Raspberry Pi Pico 2W (RP2350 with WiFi)
- **Display**: Waveshare Pico-ePaper-4.2 (400x300, black/white)
- **Power**: USB primary, optional LiPo battery with Adafruit PowerBoost 500C
- **Optional**: DS3231 RTC module for offline timekeeping

## Software Stack
- **Language**: MicroPython (latest stable for RP2350)
- **Display Driver**: Waveshare native MicroPython library
- **Time Sync**: NTP via WiFi
- **Moon Calculations**: Local astronomical algorithms (Meeus formulas)
- **API Verification**: RapidAPI Moon Phase endpoint (once daily, 25/month limit)

## Architecture
1. **Boot sequence**: WiFi connect → NTP sync → store time to flash
2. **Hourly updates**: Calculate moon phase locally → update e-ink display
3. **Daily verification**: API call to RapidAPI → compare with local calculation → sync if drift detected
4. **Offline capable**: Can run without WiFi after initial setup using stored time + elapsed tracking

## API Configuration
- **Provider**: RapidAPI Moon Phase API
- **Endpoint**: `https://moon-phase.p.rapidapi.com/advanced`
- **Location**: Ann Arbor, MI (42.2808° N, 83.7430° W)
- **Rate Limit**: 25 calls/month (use sparingly - daily verification only)
- **Headers Required**: `x-rapidapi-key`, `x-rapidapi-host`

## Display Requirements
- Moon phase graphic (large, centered)
- Phase name (e.g., "Waxing Crescent")
- Illumination percentage
- Moonrise/moonset times (local)
- Current date
- Last update timestamp

## Code Style Guidelines
- Clear comments for beginner understanding
- Modular design (separate concerns)
- Config file for user settings (WiFi, API key, location)
- Error handling with graceful fallbacks
- Logging for debugging

## Power Management
- E-ink only refreshes on phase change or hourly updates
- Consider deep sleep between updates (if battery powered)
- USB-powered: normal operation, no sleep needed
- Battery mode: aggressive power saving

## File Structure
```
pico-moon-tracker/
├── main.py              # Main loop and orchestration
├── moon_calc.py         # Astronomical calculations (local)
├── display_manager.py   # E-ink display abstraction
├── wifi_manager.py      # WiFi connection and NTP sync
├── api_client.py        # RapidAPI Moon Phase client
├── config.py            # User configuration (gitignored)
├── config.py.example    # Template for users
├── storage.py           # Flash storage for persistent data
├── images/              # Moon phase images
└── lib/                 # Waveshare e-Paper drivers
```

## Development Notes
- Test on actual hardware (Pico 2W + Waveshare display)
- Validate moon calculations against known ephemeris data
- API key must be kept secret (not in git)
- Consider time zones for moonrise/set calculations
- E-ink refresh takes ~4 seconds (full refresh)

## Future Enhancements (Not for Initial Gift)
- Home Assistant integration via MQTT
- Multiple location support
- Weather integration
- Meteor shower notifications
- Eclipse predictions

## Testing Checklist
- [ ] NTP sync works on first boot
- [ ] Local moon phase matches API within 1%
- [ ] Display renders all moon phases correctly
- [ ] Handles WiFi disconnection gracefully
- [ ] API rate limiting respected (1 call/day)
- [ ] Time persists across reboots
- [ ] Battery charging circuit works (if implemented)
- [ ] Runs for 24+ hours without errors

## Deployment Steps
1. Copy all `.py` files to Pico 2W
2. Copy Waveshare drivers to `/lib`
3. Copy `config.py.example` to `config.py` and fill in credentials
4. Copy moon phase images to `/images`
5. Reset Pico - should auto-start via `main.py`

## Dependencies
- MicroPython 1.23+ for RP2350
- `urequests` library (HTTP client)
- `ntptime` library (time sync)
- Waveshare `epd4in2` driver
- Standard MicroPython libs: `time`, `machine`, `json`, `math`
