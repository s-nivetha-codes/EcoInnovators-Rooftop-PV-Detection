"""
Quick Start Guide for Solar Panel Verification System
"""

def print_quick_start():
    """Print quick start guide"""
    guide = """
╔════════════════════════════════════════════════════════════════════╗
║     SOLAR PANEL INSTALLATION VERIFICATION SYSTEM - QUICK START    ║
║              PM Surya Ghar Yojana Verification Tool              ║
╚════════════════════════════════════════════════════════════════════╝

📋 QUICK START GUIDE
═══════════════════════════════════════════════════════════════════

1️⃣  INSTALLATION (First Time Only)
─────────────────────────────────────────────────────────────────
  
  Step 1: Open PowerShell/Terminal
  Step 2: Navigate to project directory:
    cd "e:\\jr project\\solar-verification-system"
  
  Step 3: Install dependencies (if not done):
    pip install -r requirements.txt
    or
    py -m pip install -r requirements.txt


2️⃣  RUNNING THE APPLICATION
─────────────────────────────────────────────────────────────────

  OPTION A: GUI Interface (Recommended for Users)
  ───────────────────────────────────────────────
  
  For Tkinter GUI (Simple, Built-in):
    python gui_tkinter.py
    
  For PySimpleGUI (Modern):
    python gui_app.py
    
  For Interactive Launcher:
    python launcher.py


  OPTION B: Command-Line Interface (For Developers)
  ──────────────────────────────────────────────────
  
  Basic usage:
    python main.py "C:\\Users\\amith\\Downloads\\home.jpg"
    
  With satellite image:
    python main.py "C:\\path\\to\\home.jpg" --satellite-image "C:\\path\\to\\satellite.jpg"


3️⃣  USING THE GUI APPLICATION
─────────────────────────────────────────────────────────────────

  Step 1: Launch the GUI
    python gui_tkinter.py
    
  Step 2: Upload Home Image
    • Click "📁 Browse User Image"
    • Select a clear photo of your home with solar panels
    • Image appears in the preview area
    
  Step 3: (Optional) Upload Satellite Image
    • Click "📁 Browse Satellite Image"
    • Select matching satellite image
    • Good for verification accuracy
    
  Step 4: Verify Installation
    • Click "✓ VERIFY INSTALLATION"
    • Wait for processing (5-10 seconds)
    
  Step 5: View Results
    • ✅ APPROVED - Solar installation verified
    • ❌ REJECTED - Installation not verified
    • See detailed metrics in results box


4️⃣  UNDERSTANDING THE RESULTS
─────────────────────────────────────────────────────────────────

  ✅ APPROVED means:
     • Solar panels detected in image
     • Coverage percentage sufficient
     • Confidence score ≥ 45%
     → Ready for subsidy approval
     
  ❌ REJECTED means:
     • No panels detected, OR
     • Insufficient coverage, OR
     • Confidence score too low
     → Request better image or manual verification


5️⃣  IMPORTANT TIPS FOR BEST RESULTS
─────────────────────────────────────────────────────────────────

  📸 Image Tips:
     • Take photo in good daylight
     • Ensure solar panels are clearly visible
     • Include full panel area in frame
     • Use camera or smartphone (good quality)
     • Avoid shadows and glare
     
  📍 Location Tips:
     • Photograph from ground level facing roof/terrace
     • Include roofline and surroundings
     • Try different angles if first attempt fails
     
  🛰️ Satellite Image:
     • Use Google Maps satellite view
     • Download matching location image
     • Helps improve verification accuracy


6️⃣  OUTPUT FILES
─────────────────────────────────────────────────────────────────

  After verification, files are saved in:
  
  📁 verification_results/
     ├── verification_YYYYMMDD_HHMMSS.png    (Annotated image)
     └── latest_results.json                  (Detailed report)
     
  📁 test_images/                             (Sample test images)


7️⃣  TROUBLESHOOTING
─────────────────────────────────────────────────────────────────

  Problem: GUI doesn't open
  → Ensure Python 3.8+ is installed
  → Run: python --version
  
  Problem: "Module not found" error
  → Reinstall packages:
    pip install -r requirements.txt --force-reinstall
  
  Problem: Image not detecting panels
  → Try different photo angle
  → Ensure good lighting
  → Verify panels are clearly visible
  → Check image file format (JPG/PNG/BMP)
  
  Problem: Low confidence score
  → Take clearer, higher resolution photo
  → Ensure panels fill more of the image
  → Reduce shadow/glare
  
  Problem: Verification takes too long
  → Normal (5-10 seconds)
  → Check system resources
  → Try with smaller image file


8️⃣  USEFUL COMMANDS
─────────────────────────────────────────────────────────────────

  Run tests (verify system working):
    python test_system.py
    
  Launch Tkinter GUI:
    python gui_tkinter.py
    
  Launch PySimpleGUI:
    python gui_app.py
    
  Interactive launcher:
    python launcher.py
    
  Command-line verification:
    python main.py "path\\to\\image.jpg"
    
  Check Python version:
    python --version
    
  Check installed packages:
    pip list


9️⃣  PROJECT INFORMATION
─────────────────────────────────────────────────────────────────

  Project: Solar Panel Installation Verification System
  Purpose: Verify solar installations under PM Surya Ghar Yojana
  Version: 1.0
  Language: Python 3.8+
  
  Features:
    ✓ Solar panel detection
    ✓ Coverage analysis
    ✓ Image comparison
    ✓ Confidence scoring
    ✓ Multiple interfaces (GUI & CLI)
    ✓ JSON reporting
    ✓ Visual annotations


🔟  GETTING HELP
─────────────────────────────────────────────────────────────────

  1. Check README.md for detailed documentation
  2. Review test_system.py for examples
  3. Examine config.py for tunable parameters
  4. Check verification_results/ for past results
  5. Look at error messages for specific issues


═══════════════════════════════════════════════════════════════════

🎯 NEXT STEPS:

1. Close this guide
2. Run: python gui_tkinter.py
3. Upload your solar panel image
4. Click "✓ VERIFY INSTALLATION"
5. View your results!

═══════════════════════════════════════════════════════════════════
"""
    print(guide)


if __name__ == '__main__':
    print_quick_start()
