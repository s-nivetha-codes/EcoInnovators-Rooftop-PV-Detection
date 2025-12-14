# Solar Panel Installation Verification System

A comprehensive Python-based system to verify solar panel installations by analyzing home images and comparing them with satellite imagery. This system supports the PM Surya Ghar Yojana verification process with both GUI and command-line interfaces.

## 🌟 Features

- **Solar Panel Detection**: Advanced computer vision to accurately detect solar panels in images
- **Image Comparison**: Compares user-uploaded images with satellite imagery
- **Coverage Analysis**: Calculates solar panel coverage percentage
- **Confidence Scoring**: Provides confidence level for verification
- **Visual Report**: Generates annotated output images with verification results
- **JSON Results**: Saves detailed verification results
- **Multiple Interfaces**: GUI (Tkinter/PySimpleGUI) and Command-line options
- **Real-time Verification**: Fast and accurate verification process

## 💻 System Requirements

- Python 3.8+
- Windows/Linux/macOS
- Webcam or image files (JPG, PNG, BMP)

## 📦 Installation

### Step 1: Set up Python Environment

```bash
cd "e:\jr project\solar-verification-system"
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Option 1: GUI Interface (Recommended for Users)

#### Tkinter GUI (Built-in, No Extra Installation)
```bash
python gui_tkinter.py
```

#### PySimpleGUI (Modern Interface)
```bash
python gui_app.py
```

### Option 2: Command-Line Interface (For Developers)

```bash
python main.py "path/to/home/image.jpg"
```

With satellite image:
```bash
python main.py "path/to/home/image.jpg" --satellite-image "path/to/satellite/image.jpg"
```

### Option 3: Launcher (Choose Interface)

```bash
python launcher.py
```

This will prompt you to choose between:
1. Tkinter GUI
2. PySimpleGUI
3. Command-Line

## 📊 Example Usage

```bash
# Using Tkinter GUI (Recommended)
python gui_tkinter.py

# Then:
# 1. Click "📁 Browse User Image" to select home image
# 2. Optionally select satellite image
# 3. Click "✓ VERIFY INSTALLATION"
# 4. View results
```

## 📊 Output

The system generates:

1. **Verification Result**: ✅ APPROVED or ❌ REJECTED
2. **Output Image**: Annotated image with solar panel detection (saved in `verification_results/`)
3. **JSON Report**: Detailed results in `verification_results/latest_results.json`

### Output Information

| Field | Description |
|-------|-------------|
| **Status** | Processing status (COMPLETED, ERROR, etc.) |
| **Verification Result** | APPROVED or REJECTED |
| **Solar Detected** | Whether solar panels were found |
| **Solar Coverage** | Percentage of image with solar panels |
| **Similarity Score** | Match score between images (0-1) |
| **Confidence Level** | Overall confidence of verification |

## ✅ Verification Criteria

The system **APPROVES** installations when:

1. ✓ Solar panels are detected in the image
2. ✓ Coverage is sufficient (typically > 5%)
3. ✓ Confidence score is above threshold (default: 45%)
4. ✓ Panels have rectangular shape characteristics

The system **REJECTS** installations when:

1. ✗ No solar panels detected
2. ✗ Insufficient coverage
3. ✗ Confidence below threshold
4. ✗ Detected objects don't match panel characteristics

## ⚙️ Configuration

Edit `config.py` to adjust:

```python
MIN_CONFIDENCE_THRESHOLD = 0.45    # Minimum confidence for approval
SOLAR_PANEL_COLOR_RANGE = {        # Color detection range
    'blue': (100, 150),
    'hue': (100, 130)
}
```

## 📁 Project Structure

```
solar-verification-system/
├── main.py                 # Command-line entry point
├── gui_tkinter.py         # Tkinter GUI (Recommended)
├── gui_app.py             # PySimpleGUI interface
├── launcher.py            # Interface selector
├── verifier.py            # Core verification logic
├── image_processor.py     # Image processing module
├── config.py              # Configuration settings
├── test_system.py         # Test suite
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
├── verification_results/  # Output results directory
└── test_images/          # Test images directory
```

## 🔄 How It Works

1. **Image Loading**: Loads home image
2. **Preprocessing**: Enhances image quality for analysis
3. **Solar Panel Detection**: Identifies blue/dark rectangular objects (solar panels)
4. **Coverage Calculation**: Computes solar panel area percentage
5. **Image Comparison**: Compares with satellite image (if provided)
6. **Confidence Calculation**: Determines verification confidence score
7. **Report Generation**: Creates annotated output and JSON results

## 📈 Results Interpretation

### ✅ APPROVED
- Solar panels successfully detected
- Coverage meets minimum requirements
- Confidence score ≥ 45%
- **Next Step**: Grant subsidy/verification approval

### ❌ REJECTED  
- No solar panels detected, OR
- Insufficient coverage, OR
- Confidence score < 45%
- **Next Step**: Request resubmission or manual verification

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Image not loading | Ensure file exists and format is JPG/PNG/BMP |
| Panels not detected | Ensure good lighting, clear image, panels visible |
| Low confidence score | Improve image quality, ensure clear panel visibility |
| GUI not launching | Verify Python and all dependencies are installed |
| Slow verification | This is normal; processing takes 5-10 seconds |

## 📝 Example Output

```
======================================================================
VERIFICATION RESULTS
======================================================================

✅ Status: APPROVED
Solar Detected: Yes
Solar Coverage: 67.86%
Confidence Level: 64.0%
Similarity Score: 0.850

Message: Solar installation verified successfully (Confidence: 64.0%)
Output Image: verification_results\verification_20251214_153039.png

======================================================================
```

## 🔧 For Developers

### Run Tests
```bash
python test_system.py
```

### Run with Different Confidence Threshold
Edit `config.py`:
```python
MIN_CONFIDENCE_THRESHOLD = 0.5  # Stricter verification
```

### Extend Solar Panel Detection
Modify `image_processor.py`:
```python
# Adjust color range for different lighting conditions
lower_blue = np.array([80, 50, 20])
upper_blue = np.array([140, 255, 150])
```

## 📜 License

This project is developed for the **EcoInnovators Ideathon 2026** organized by the Global Learning Council in partnership with IIT Madras, Infosys, and other stakeholders.

## 👥 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure image files are valid and accessible
4. Review test results with `python test_system.py`

---

**Developed for PM Surya Ghar Yojana Solar Installation Verification**
