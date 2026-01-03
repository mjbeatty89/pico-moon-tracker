# Hardware Setup Guide

## Components List

### Required Components
- **Raspberry Pi Pico 2W** - RP2350 microcontroller with WiFi
- **Waveshare Pico-ePaper-4.2** - 400x300 pixel e-Paper display module
- **Micro USB Cable** - For power and programming

### Optional (Battery Operation)
- **Adafruit PowerBoost 500C** - LiPo charger and 5V booster
- **3.7V LiPo Battery** - 1000-5000mAh (larger = longer runtime)
- **JST Connector** - For battery connection

### Tools Needed
- Soldering iron (if adding battery option)
- Micro USB cable
- Computer with Thonny IDE

## Assembly Instructions

### Basic Setup (USB Powered)

The Waveshare Pico-ePaper-4.2 is designed to plug directly onto the Pico 2W - no wiring required!

1. **Inspect the Display Module**
   - The display has female headers on the bottom
   - It's designed to sandwich directly onto the Pico

2. **Align the Headers**
   - The display should sit on top of the Pico
   - All 40 GPIO pins should line up perfectly
   - Double-check alignment before pressing down

3. **Seat the Display**
   - Gently press the display onto the Pico headers
   - Ensure all pins are fully inserted
   - The display should sit flush and stable

4. **Connect Power**
   - Plug micro USB into the Pico
   - Power can come from computer or USB wall adapter
   - Display will initialize on first boot

**That's it for basic setup!** The display connects via SPI using these pins:
- **BUSY** → GP13
- **RST** → GP12
- **DC** → GP8
- **CS** → GP9
- **CLK** → GP10
- **DIN** → GP11
- **GND** → GND
- **VCC** → 3.3V

*(These connections are built into the display module)*

### Battery-Powered Setup (Optional)

For a truly portable moon tracker, add a LiPo battery with the PowerBoost 500C.

#### Components Needed
- Adafruit PowerBoost 500C (~$20)
- 3.7V LiPo battery with JST connector (2000mAh+ recommended)
- Wire and solder

#### Wiring Diagram
```
LiPo Battery (JST) → PowerBoost 500C Battery Input
PowerBoost 5V Out  → Pico VBUS (pin 40)
PowerBoost GND     → Pico GND (pin 38)
Micro USB          → PowerBoost USB (for charging)
```

#### Assembly Steps

1. **Solder Headers to PowerBoost** (if not pre-soldered)
   - Solder male headers to the output pins
   - You need: 5V, GND

2. **Connect Battery**
   - Plug JST connector into PowerBoost battery input
   - Check polarity! (Red = +, Black = -)

3. **Wire to Pico**
   - PowerBoost 5V → Pico VBUS (pin 40)
   - PowerBoost GND → Pico GND (pin 38)
   - *Alternative*: Cut a micro USB cable and wire directly

4. **Test Charging**
   - Plug USB into PowerBoost
   - Yellow LED should light (charging)
   - Green LED when fully charged

5. **Enable Deep Sleep**
   - In `config.py`, set `ENABLE_DEEP_SLEEP = True`
   - This extends battery life significantly

#### Battery Life Estimates
- **2000mAh without deep sleep**: 8-12 hours
- **2000mAh with hourly deep sleep**: 3-5 days
- **5000mAh with hourly deep sleep**: 1-2 weeks

## Pin Reference (Waveshare Display)

The Waveshare display uses these Pico 2W pins:

| Function | Pico Pin | GPIO | Description |
|----------|----------|------|-------------|
| BUSY     | Pin 17   | GP13 | Display busy signal |
| RST      | Pin 16   | GP12 | Reset |
| DC       | Pin 11   | GP8  | Data/Command select |
| CS       | Pin 12   | GP9  | SPI Chip Select |
| CLK      | Pin 14   | GP10 | SPI Clock |
| DIN      | Pin 15   | GP11 | SPI Data In (MOSI) |
| GND      | Pin 18/23| GND  | Ground |
| VCC      | Pin 36   | 3.3V | Power (3.3V) |

## Mounting / Enclosure

### Simple Frame Mount
The easiest approach is to mount the assembly in a picture frame:
1. Find a shallow frame (5x7" or similar)
2. Cut cardboard backing to fit
3. Secure Pico+Display to backing with standoffs or hot glue
4. Route USB cable through frame edge

### 3D Printed Enclosure
Consider designing a custom enclosure with:
- Window for display
- Cavity for Pico and battery
- Cable routing
- Desk stand or wall mount

*(STL files coming soon - contributions welcome!)*

## Power Considerations

### USB-Powered (Recommended for Gifts)
- Simple, reliable, always-on
- No battery maintenance
- Ideal for desk/shelf placement
- ~150mA draw (minimal cost: <$2/year)

### Battery-Powered
- Portable, can go anywhere
- Requires periodic charging
- Best with deep sleep enabled
- Ideal for travel or off-grid

## Safety Notes

⚠️ **LiPo Battery Safety**:
- Never puncture or crush batteries
- Don't over-discharge (PowerBoost has protection)
- Store at 50% charge if not using long-term
- Keep away from extreme heat
- Use proper LiPo charging circuit (like PowerBoost 500C)

## Troubleshooting

### Display Not Showing Anything
- Check display is firmly seated on all pins
- Verify power LED on Pico is lit
- Check console output for driver errors
- Try simulation mode first to test code

### Display Shows Garbage
- Reset the Pico (unplug/replug)
- Check Waveshare driver is correctly installed to `lib/`
- Verify MicroPython firmware is latest version

### Battery Drains Too Fast
- Enable `ENABLE_DEEP_SLEEP` in config
- Use larger capacity battery
- Check for WiFi constantly connected (should disconnect between syncs)
- Verify e-Paper isn't refreshing too often

### Won't Charge
- Check USB cable is data-capable (not just power)
- Verify PowerBoost charging LED lights up
- Test battery voltage with multimeter (should be 3.7V)
- Check polarity on JST connector

## Next Steps

Once hardware is assembled:
1. Follow QUICKSTART.md to install software
2. Test in simulation mode first
3. Verify display updates correctly
4. Adjust settings for your environment

## Resources

- **Pico 2W Datasheet**: https://datasheets.raspberrypi.com/pico/pico-2-w-datasheet.pdf
- **Waveshare Wiki**: https://www.waveshare.com/wiki/Pico-ePaper-4.2
- **PowerBoost 500C Guide**: https://learn.adafruit.com/adafruit-powerboost-500-plus-charger
- **MicroPython Docs**: https://docs.micropython.org/
