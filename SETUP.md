# Setup and Installation Guide

## Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- Webcam
- 4GB RAM minimum
- Good lighting environment

### 2. Installation Steps

```bash
# Clone the repository
git clone https://github.com/sumanjd/fireball-hand-gesture.git
cd fireball-hand-gesture

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python main.py
```

## Troubleshooting

### Camera Not Detected
- Check if your webcam is connected
- Try changing `CAMERA_INDEX` in `config.py` (0 for default, 1 for second camera)
- Ensure no other application is using the camera

### Hand Not Detected
- Improve lighting (avoid shadows)
- Keep your entire hand visible
- Move closer to camera (30cm - 1m range)
- Increase `HAND_DETECTION_CONFIDENCE` in `config.py` (0.5-0.9)

### Low FPS
- Close other applications
- Reduce camera resolution in `config.py`
- Lower `TARGET_FPS` value

### ImportError: No module named 'mediapipe'
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version is 3.8+: `python --version`

## Performance Optimization

### For Better Detection:
- Increase lighting in your room
- Use a high-quality webcam
- Ensure hand is not blurry
- Adjust confidence thresholds in `config.py`

### For Better Performance:
- Lower camera resolution
- Reduce max active fireballs
- Disable debug info (press D key)
- Close unnecessary applications

## Configuration

Edit `config.py` to customize:
- Camera resolution and FPS
- Hand detection sensitivity
- Fireball physics and effects
- Visual styling and colors

## File Structure

```
fireball-hand-gesture/
├── main.py                 # Main application entry point
├── hand_detector.py        # Hand detection and tracking
├── fireball.py            # Fireball physics and animations
├── effects.py             # Visual effects (particles, explosions)
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── SETUP.md              # This file
└── README.md             # Project documentation
```

## Advanced Usage

### Gesture Calibration
Adjust these in `config.py`:
- `THROW_VELOCITY_THRESHOLD` - How fast hand must move to trigger throw
- `HAND_OPEN_THRESHOLD` - Distance threshold for hand open detection

### Visual Customization
Modify colors in `config.py`:
- `COLOR_FIREBALL` - Main fireball color
- `COLOR_EXPLOSION` - Explosion particle color
- `COLOR_BACKGROUND` - Background color

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed: `pip list`
3. Try with a different camera or lighting
4. Check system resources (CPU/RAM)

## Next Steps

After setup, try:
1. Open your hand and see fireball appear
2. Make quick throwing gestures
3. Watch fireballs travel across screen
4. See explosion effects on impact
5. Try to beat your high score!

Enjoy! 🔥
