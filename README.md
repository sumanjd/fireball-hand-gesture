# 🔥 Fireball Hand Gesture Detector

An interactive application that detects your hand gestures using your webcam and lets you throw fireballs!

## Features

✨ **Hand Detection** - Real-time hand pose detection using MediaPipe  
🔥 **Fireball Animation** - Animated fireball appears on your open hand  
💥 **Physics** - Fireball travels across the screen following your throwing motion  
⚡ **Visual Effects** - Fiery flash animation on impact  

## Prerequisites

- Python 3.8 or higher
- Webcam
- 4GB RAM (minimum)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sumanjd/fireball-hand-gesture.git
cd fireball-hand-gesture
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main application:
```bash
python main.py
```

## How to Play

1. **Open Your Hand** - Show your palm to the camera
   - A fireball will appear on your hand
   
2. **Throw Motion** - Quickly close and open your hand or make a throwing gesture
   - The fireball will launch from your hand
   
3. **Impact** - Fireball travels across the screen
   - A fiery explosion flash appears when it reaches the edge
   
4. **Exit** - Press `ESC` or `Q` to quit

## Project Structure

```
fireball-hand-gesture/
├── main.py                 # Main application
├── hand_detector.py        # Hand detection logic
├── fireball.py            # Fireball class and physics
├── effects.py             # Visual effects (particles, explosions)
├── assets/                # Images, sounds, etc.
│   ├── fireball/
│   └── effects/
├── requirements.txt       # Python dependencies
└── README.md
```

## Technologies Used

- **MediaPipe** - Hand pose detection
- **OpenCV** - Webcam feed processing
- **Pygame** - Graphics and animation
- **NumPy** - Numerical computations

## Performance Tips

- Ensure good lighting for better hand detection
- Keep your hand visible in the camera frame
- Close unnecessary applications for smooth performance

## Troubleshooting

**No hand detected?**
- Ensure adequate lighting
- Keep your entire hand visible
- Move closer to the camera

**Low FPS?**
- Close other applications
- Lower camera resolution in settings
- Check your CPU/GPU usage

## Future Enhancements

- [ ] Multiple fireballs at once
- [ ] Spell effects (ice, lightning)
- [ ] Sound effects
- [ ] Difficulty levels
- [ ] Score system
- [ ] Multiplayer support

## License

MIT License

## Contributing

Feel free to fork and submit pull requests!
