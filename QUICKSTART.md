# Quick Start Guide

Get your Moon Tracker running in 15 minutes!

## Prerequisites Checklist

- [ ] Raspberry Pi Pico 2W
- [ ] Waveshare Pico-ePaper-4.2 display
- [ ] Micro USB cable
- [ ] WiFi network (2.4GHz)
- [ ] RapidAPI account + Moon Phase API key

## Step-by-Step Setup

### 1. Flash MicroPython (5 minutes)

1. Download MicroPython for Pico 2W: https://micropython.org/download/RPI_PICO2/
2. Hold BOOTSEL button on Pico while plugging in USB
3. Drag .uf2 file to RPI-RP2 drive
4. Pico reboots automatically

### 2. Get API Key (3 minutes)

1. Sign up at https://rapidapi.com/
2. Subscribe to Moon Phase API (free tier)
3. Copy your `x-rapidapi-key`

### 3. Install Thonny IDE (2 minutes)

Download from https://thonny.org/
- Configure: Tools → Options → Interpreter → MicroPython (Raspberry Pi Pico)

### 4. Setup Config (2 minutes)

1. Open `config.py.example`
2. Fill in:
   - WiFi SSID and password
   - RapidAPI key
   - Your location (or use Ann Arbor default)
   - Timezone offset
3. Save as `config.py`

### 5. Upload Files (3 minutes)

In Thonny, for each .py file:
1. Open file
2. File → Save As → Raspberry Pi Pico
3. Save with same name

**Files to upload:**
- config.py
- main.py
- moon_calc.py
- display_manager.py
- wifi_manager.py
- api_client.py
- storage.py

### 6. Download Waveshare Driver

1. Visit: https://github.com/waveshare/Pico_ePaper_Code
2. Navigate to `python/Pico-ePaper-4.2/`
3. Download `epd4in2.py`
4. Create folder `lib` on Pico (in Thonny: right-click → New directory)
5. Upload `epd4in2.py` to `lib/` folder

### 7. Run!

1. Press STOP in Thonny
2. Press RUN
3. Watch console for status messages
4. Display should update with moon phase!

## First Run Checklist

You should see:
- [ ] WiFi connection message
- [ ] NTP time sync
- [ ] API test (if DEBUG=True)
- [ ] Moon phase calculation
- [ ] Display update (or simulation if no driver)

## Quick Test (Without Hardware)

Want to test without the display?

Just skip the Waveshare driver installation. The code will run in "simulation mode" and print the display output to the console.

```
==================================================
DISPLAY OUTPUT (Simulated)
==================================================
Location: Ann Arbor, MI
Date: 01/03/2026 12:34

                    [MOON GRAPHIC]
                         🌙

Phase: Waxing Crescent
Illumination: 23.4%
Moonrise: 09:15
Moonset: 22:45
==================================================
```

## Common Issues

### "config.py not found"
→ You need to create `config.py` from `config.py.example`

### "epd4in2 driver not found"
→ Download Waveshare driver to `lib/` folder (or test in simulation mode first)

### WiFi won't connect
→ Check SSID/password, ensure 2.4GHz network, try moving closer to router

### API errors
→ Verify API key, check RapidAPI dashboard for subscription status

## Next Steps

Once running:
- Adjust `LOCAL_UPDATE_INTERVAL` for refresh frequency
- Set `DEBUG = False` for quieter operation
- Enable `ENABLE_DEEP_SLEEP` for battery mode
- Build or 3D print an enclosure

## Need Help?

Check the full README.md for detailed troubleshooting and configuration options.
