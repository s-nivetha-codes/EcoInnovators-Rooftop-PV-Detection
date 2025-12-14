"""
Launcher for Solar Panel Verification System
Choose between GUI and Command-Line interface
"""

import sys
import os


def main():
    """Main launcher"""
    print("="*60)
    print("SOLAR PANEL INSTALLATION VERIFICATION SYSTEM")
    print("="*60)
    print()
    print("Choose an interface:")
    print()
    print("  1. GUI (Tkinter) - User-friendly graphical interface")
    print("  2. GUI (PySimpleGUI) - Modern graphical interface")
    print("  3. Command-Line - Terminal-based interface")
    print()
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == '1':
        print("\nLaunching Tkinter GUI...")
        os.system("python gui_tkinter.py")
    elif choice == '2':
        print("\nLaunching PySimpleGUI...")
        os.system("python gui_app.py")
    elif choice == '3':
        print("\nUsage: python main.py <image_path> [--satellite-image <path>]")
        print()
        print("Example:")
        print('  python main.py "C:\\Users\\amith\\Downloads\\home.jpg"')
        print()
    else:
        print("Invalid choice. Please run the launcher again.")


if __name__ == '__main__':
    main()
