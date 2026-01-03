# Pico 2W Moon Phase Tracker

A standalone lunar phase tracker using Raspberry Pi Pico 2W and Waveshare 4.2" e-Paper display. Perfect as a desk decoration or gift for astronomy enthusiasts!

![Moon Tracker](docs/moon_tracker_demo.jpg)

## Features

- 🌙 **8 Moon Phases**: New, Waxing Crescent, First Quarter, Waxing Gibbous, Full, Waning Gibbous, Last Quarter, Waning Crescent
- 📊 **Illumination Percentage**: Real-time calculation of visible moon surface
- ⏰ **Moonrise/Moonset Times**: Local times for your location
- 🔌 **Low Power**: E-ink display holds image without power
- 📡 **Mostly Offline**: Local calculations with optional daily API verification
- 🔋 **Battery Ready**: Optional LiPo battery with charging circuit

## Hardware Requirements

### Required
- Raspberry Pi Pico 2W (RP2350 with WiFi)
- Waveshare Pico-ePaper-4.2 (400x300 black/white display)
- Micro USB cable for power/programming

### Optional (Battery Operation)
- Adafruit PowerBoost 500C charger/booster
- 3.7V LiPo battery (1000-5000mAh recommended)
- Micro USB cable for charging

## Software Requirements

- MicroPython 1.23+ for RP2350
- Waveshare e-Paper driver (see installation below)
- RapidAPI Moon Phase API key (free tier: 25 calls/month)

## Installation

### 1. Install MicroPython on Pico 2W

Download the latest MicroPython firmware for Pico 2W from [micropython.org](https://micropython.org/download/RPI_PICO2/)

Flash it to your Pico:
1. Hold BOOTSEL button while connecting USB
2. Drag .uf2 file to RPI-RP2 drive
3. Pico will reboot with MicroPython

### 2. Get API Key

1. Sign up at [RapidAPI](https://rapidapi.com/)
2. Subscribe to [Moon Phase API](https://rapidapi.com/MoonAPIcom/api/moon-phase) (free tier)
3. Copy your API key

### 3. Setup Project Files

Copy all project files to your Pico 2W using Thonny IDE or rshell:

```bash
# Core application files
- main.py
- config.py (created from config.py.example)
- moon_calc.py
- display_manager.py
- wifi_manager.py
- api_client.py
- storage.py
```

### 4. Install Waveshare Driver

Download the Waveshare e-Paper MicroPython driver:
1. Visit [Waveshare Wiki](https://www.waveshare.com/wiki/Pico-ePaper-4.2)
2. Download `epd4in2.py` from their MicroPython examples
3. Create a `lib` folder on your Pico
4. Copy `epd4in2.py` to `/lib/` on the Pico

**Note**: If the driver is not found, the code will run in "simulation mode" for testing.

### 5. Configure Settings

1. Copy `config.py.example` to `config.py`
2. Edit `config.py` with your settings:

```python
# WiFi credentials
WIFI_SSID = "YourWiFiName"
WIFI_PASSWORD = "YourWiFiPassword"

# RapidAPI credentials
RAPIDAPI_KEY = "your_api_key_here"

# Your location (default: Ann Arbor, MI)
LATITUDE = 42.2808
LONGITUDE = -83.7430
LOCATION_NAME = "Ann Arbor, MI"

# Timezone offset (EST = -5, EDT = -4)
TIMEZONE_OFFSET = -5
```

### 6. Upload to Pico

Using Thonny IDE:
1. Connect Pico via USB
2. Open each .py file
3. Save to Pico (File → Save As → Raspberry Pi Pico)
4. Reset Pico - `main.py` will auto-start

### 7. Run

The tracker starts automatically on power-up. It will:
1. Connect to WiFi
2. Sync time via NTP
3. Calculate current moon phase
4. Display on e-Paper
5. Update hourly (with daily API verification)

## Usage

### Normal Operation

Just plug in and let it run! The display updates:
- **Hourly**: Local calculation
- **Daily**: API verification + time sync

### Testing Mode

To test without the hardware display, the code runs in simulation mode and prints output to the console.

```python
# In config.py
DEBUG = True  # Enable verbose output
```

### Battery Operation

Enable deep sleep mode for battery operation:

```python
# In config.py
ENABLE_DEEP_SLEEP = True
SLEEP_DURATION = 3600  # 1 hour
```

**Note**: Deep sleep resets the Pico, so state is saved to flash.

## Troubleshooting

### WiFi Won't Connect
- Check SSID and password in `config.py`
- Ensure 2.4GHz WiFi (Pico doesn't support 5GHz)
- Check signal strength (Pico needs good signal)

### API Errors
- Verify API key is correct
- Check RapidAPI subscription status
- Ensure you haven't exceeded 25 calls/month

### Display Not Working
- Check if `lib/epd4in2.py` driver is present
- Ensure display is seated properly on Pico headers
- Try running in simulation mode first

### Time/Date Wrong
- Check `TIMEZONE_OFFSET` in `config.py`
- Verify NTP sync succeeded (check console output)
- Manually adjust if needed for DST

## File Structure

```
pico-moon-tracker/
├── README.md              # This file
├── WARP.md               # Development notes
├── config.py.example     # Configuration template
├── main.py               # Main application loop
├── moon_calc.py          # Astronomical calculations
├── display_manager.py    # E-Paper display driver
├── wifi_manager.py       # WiFi and NTP management
├── api_client.py         # RapidAPI client
├── storage.py            # Persistent storage
└── lib/                  # Libraries
    └── epd4in2.py        # Waveshare driver (download separately)
```

## Power Consumption

- **USB Power**: Always-on, ~150mA average
- **Battery (no sleep)**: ~8-12 hours on 2000mAh
- **Battery (deep sleep)**: Several days to weeks depending on battery

## Enclosure

A 3D-printable enclosure design would be a nice addition! For now, the display can stand alone or be mounted in a simple frame.

## Credits

- Based on the [Wireless Lunar Phase Tracker](https://www.instructables.com/Wireless-Lunar-Phase-Tracker/) by IamTeknik
- Adapted for Raspberry Pi Pico 2W by Matthew Beatty
- Moon calculations based on Jean Meeus "Astronomical Algorithms"
- RapidAPI Moon Phase API for verification

## License

MIT License - Feel free to modify and share!

## Contributing

Improvements welcome! Some ideas:
- Better moon phase graphics/bitmaps
- More accurate rise/set calculations
- Support for multiple locations
- Weather integration
- 3D printable enclosure design

## Support

For issues or questions, check:
- Waveshare Wiki: https://www.waveshare.com/wiki/Pico-ePaper-4.2
- MicroPython Docs: https://docs.micropython.org/
- RapidAPI Moon Phase: https://rapidapi.com/MoonAPIcom/api/moon-phase

---

**Gift Note**: This project makes a thoughtful gift for anyone interested in astronomy, lunar cycles, or just beautiful desk decorations. Consider adding a personal note about the moon's significance!
