# Contributing to Pico Moon Tracker

Thanks for your interest in improving this project! Contributions are welcome from everyone.

## Ways to Contribute

### 🐛 Report Bugs
Open an issue on GitHub with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your hardware setup (Pico version, display model)
- MicroPython version
- Console output or error messages

### 💡 Suggest Features
Ideas for enhancements:
- Better moon phase graphics/bitmaps
- More accurate rise/set calculations
- Additional astronomical data (planets, meteor showers)
- Home Assistant / MQTT integration
- Web interface for configuration
- Multiple timezone support
- Weather overlay
- 3D printable enclosure designs

### 📝 Improve Documentation
- Fix typos or unclear instructions
- Add troubleshooting tips
- Translate documentation
- Create tutorial videos
- Share your build photos

### 🔧 Submit Code
- Bug fixes
- New features
- Performance improvements
- Code cleanup and refactoring

## Development Setup

### Local Testing
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/pico-moon-tracker.git
cd pico-moon-tracker

# Create config for testing
cp config.py.example config.py
# Edit config.py with your settings

# Test calculations (on your Mac/PC)
python3 test_calculations.py
```

### Hardware Testing
- Test on actual Pico 2W hardware when possible
- Verify both USB and battery operation
- Check display updates work correctly
- Test WiFi connection/disconnection scenarios

## Code Style Guidelines

### Python/MicroPython
- Follow PEP 8 style guide (mostly)
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic

### Comments
- Explain *why*, not *what*
- Use clear, beginner-friendly language
- Remember: this is a gift project, make it maintainable

### Example
```python
def calculate_illumination(age_days):
    """
    Calculate moon illumination percentage based on age
    
    Uses simple cosine approximation: accurate to ~1%
    Args:
        age_days: Days since new moon (0-29.5)
    Returns:
        Illumination percentage (0-100)
    """
    synodic_month = 29.53058867
    phase_angle = (age_days / synodic_month) * 2 * math.pi
    illumination = (1 - math.cos(phase_angle)) / 2 * 100
    return illumination
```

## Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clear commit messages
   - Test thoroughly on hardware if possible
   - Update documentation as needed

4. **Commit with co-author line**
   ```bash
   git commit -m "Add feature: description
   
   Detailed explanation of changes
   
   Co-Authored-By: Your Name <your.email@example.com>"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Describe what changed and why
   - Reference any related issues
   - Include screenshots for visual changes
   - Note if you tested on real hardware

## Testing Checklist

Before submitting a PR:
- [ ] Code runs without errors
- [ ] Tested on actual Pico 2W (if hardware changes)
- [ ] Documentation updated
- [ ] No secrets or API keys committed
- [ ] Comments added for complex code
- [ ] Follows existing code style

## Project Goals

Keep these in mind when contributing:
- **Beginner-friendly**: Code should be easy to understand
- **Gift-worthy**: Reliable, polished, well-documented
- **Educational**: Help people learn MicroPython and astronomy
- **Standalone**: Minimize dependencies on external services

## Areas Needing Help

### High Priority
- [ ] Better moon phase bitmap images (8 phases, 100x100px)
- [ ] More accurate moonrise/moonset calculations
- [ ] 3D printable enclosure design
- [ ] Battery life optimization

### Medium Priority
- [ ] Web-based configuration interface
- [ ] Auto-detect timezone/DST
- [ ] Historical moon phase lookup
- [ ] Moon phase predictions

### Nice to Have
- [ ] Support for other e-Paper sizes
- [ ] Lunar eclipse notifications
- [ ] Multiple location profiles
- [ ] Phase change notifications

## Questions?

Feel free to open an issue with the `question` label if you're unsure about anything!

## Code of Conduct

Be kind, respectful, and helpful. This is a community project - let's keep it welcoming for everyone, especially beginners.

---

**Thank you for contributing!** 🌙
