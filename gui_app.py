"""
GUI Application for Solar Panel Installation Verification System
Modern interface for verifying solar panel installations
"""

import PySimpleGUI as sg
import os
import json
from pathlib import Path
from PIL import Image
import io
from verifier import SolarPanelVerifier
import config


# Set theme
sg.theme('DarkBlue3')
sg.set_options(element_padding=(10, 10))


class SolarPanelGUI:
    """GUI Application for Solar Panel Verification"""

    def __init__(self):
        """Initialize the GUI"""
        self.verifier = SolarPanelVerifier()
        self.current_results = None
        self.current_user_image = None
        self.current_satellite_image = None

    def get_image_thumbnail(self, image_path, size=(300, 300)):
        """Get thumbnail of image for display"""
        try:
            if not os.path.exists(image_path):
                return None
            
            img = Image.open(image_path)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Convert to bytes for PySimpleGUI
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            return bio.getvalue()
        except Exception as e:
            print(f"Error loading thumbnail: {e}")
            return None

    def create_verification_window(self):
        """Create the main verification window"""
        layout = [
            [sg.Text("🔆 SOLAR PANEL INSTALLATION VERIFICATION SYSTEM", 
                    font=('Arial', 16, 'bold'), text_color='#FFD700')],
            [sg.Text("PM Surya Ghar Yojana Verification Tool", 
                    font=('Arial', 10), text_color='#87CEEB')],
            [sg.Separator()],
            
            # Upload section
            [sg.Text("STEP 1: Upload Home Image", font=('Arial', 12, 'bold'))],
            [sg.Text("Select an image of your home with solar panels:")],
            [sg.InputText(key='-USER-IMAGE-', size=(50, 1), disabled=True),
             sg.FileBrowse(button_text='Browse', file_types=(("Image Files", "*.jpg *.jpeg *.png *.bmp"),))],
            [sg.Button('🔍 Load Image', key='-LOAD-USER-')],
            
            [sg.Column([
                [sg.Image(data=None, size=(300, 300), key='-USER-IMAGE-DISPLAY-', background_color='#1e1e1e')]
            ], vertical_alignment='top', element_justification='center')],
            
            [sg.Separator()],
            
            # Optional satellite image
            [sg.Text("STEP 2: Upload Satellite Image (Optional)", font=('Arial', 12, 'bold'))],
            [sg.Text("Select a satellite image of the same location for comparison:")],
            [sg.InputText(key='-SAT-IMAGE-', size=(50, 1), disabled=True),
             sg.FileBrowse(button_text='Browse', file_types=(("Image Files", "*.jpg *.jpeg *.png *.bmp"),))],
            [sg.Button('🔍 Load Image', key='-LOAD-SAT-')],
            
            [sg.Column([
                [sg.Image(data=None, size=(300, 300), key='-SAT-IMAGE-DISPLAY-', background_color='#1e1e1e')]
            ], vertical_alignment='top', element_justification='center')],
            
            [sg.Separator()],
            
            # Verification button
            [sg.Button('✓ VERIFY INSTALLATION', key='-VERIFY-', size=(30, 2), button_color=('white', '#2E8B57')),
             sg.Button('Clear', key='-CLEAR-', size=(15, 2)),
             sg.Button('Exit', size=(15, 2))],
            
            [sg.Separator()],
            
            # Status section
            [sg.Text("VERIFICATION RESULTS", font=('Arial', 12, 'bold'))],
            [sg.Multiline(size=(80, 20), key='-OUTPUT-', disabled=True, background_color='#2d2d2d', text_color='#00FF00')],
        ]

        window = sg.Window('Solar Panel Verification System', layout, finalize=True, size=(900, 1100))
        return window

    def run(self):
        """Run the GUI application"""
        window = self.create_verification_window()

        while True:
            event, values = window.read(timeout=100)

            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break

            # Load user image
            if event == '-LOAD-USER-':
                user_image_path = values['-USER-IMAGE-']
                if user_image_path and os.path.exists(user_image_path):
                    self.current_user_image = user_image_path
                    thumbnail_data = self.get_image_thumbnail(user_image_path)
                    if thumbnail_data:
                        window['-USER-IMAGE-DISPLAY-'].update(data=thumbnail_data)
                        window['-OUTPUT-'].print(f"✓ User image loaded: {os.path.basename(user_image_path)}")
                else:
                    sg.popup_error('Error', 'Please select a valid image file')

            # Load satellite image
            if event == '-LOAD-SAT-':
                sat_image_path = values['-SAT-IMAGE-']
                if sat_image_path and os.path.exists(sat_image_path):
                    self.current_satellite_image = sat_image_path
                    thumbnail_data = self.get_image_thumbnail(sat_image_path)
                    if thumbnail_data:
                        window['-SAT-IMAGE-DISPLAY-'].update(data=thumbnail_data)
                        window['-OUTPUT-'].print(f"✓ Satellite image loaded: {os.path.basename(sat_image_path)}")
                else:
                    sg.popup_error('Error', 'Please select a valid image file')

            # Verify installation
            if event == '-VERIFY-':
                if not self.current_user_image:
                    sg.popup_error('Error', 'Please upload a home image first')
                    continue

                window['-OUTPUT-'].print("⏳ Verifying installation...")
                window.refresh()

                try:
                    results = self.verifier.verify_installation(
                        self.current_user_image,
                        self.current_satellite_image
                    )
                    self.current_results = results

                    # Display results
                    window['-OUTPUT-'].print('\n' + '='*70)
                    window['-OUTPUT-'].print('VERIFICATION RESULTS')
                    window['-OUTPUT-'].print('='*70 + '\n')
                    
                    if results['status'] == 'COMPLETED':
                        status_color = '✅ APPROVED' if results['verification_status'] == 'APPROVED' else '❌ REJECTED'
                        window['-OUTPUT-'].print(f"Status: {status_color}")
                        window['-OUTPUT-'].print(f"Verification: {results['verification_status']}")
                        window['-OUTPUT-'].print(f"Solar Detected: {'Yes' if results['solar_detected'] else 'No'}")
                        window['-OUTPUT-'].print(f"Solar Coverage: {results['solar_coverage']:.2f}%")
                        window['-OUTPUT-'].print(f"Confidence Level: {results['confidence']:.1%}")
                        window['-OUTPUT-'].print(f"Similarity Score: {results['similarity_score']:.3f}")
                        window['-OUTPUT-'].print(f"\nMessage: {results['message']}")
                        
                        if results['output_image_path']:
                            window['-OUTPUT-'].print(f"\nOutput Image: {results['output_image_path']}")
                            output_img = self.get_image_thumbnail(results['output_image_path'])
                            if output_img:
                                window['-OUTPUT-'].print("\n[Output image preview]")
                    else:
                        window['-OUTPUT-'].print(f"Error: {results['message']}")
                    
                    window['-OUTPUT-'].print('\n' + '='*70)

                except Exception as e:
                    window['-OUTPUT-'].print(f"❌ Error during verification: {str(e)}")

            # Clear all
            if event == '-CLEAR-':
                self.current_user_image = None
                self.current_satellite_image = None
                self.current_results = None
                window['-USER-IMAGE-DISPLAY-'].update(data=None)
                window['-SAT-IMAGE-DISPLAY-'].update(data=None)
                window['-OUTPUT-'].update('')
                window['-USER-IMAGE-'].update('')
                window['-SAT-IMAGE-'].update('')

        window.close()


def main():
    """Main entry point"""
    try:
        app = SolarPanelGUI()
        app.run()
    except Exception as e:
        sg.popup_error('Fatal Error', f"An error occurred: {str(e)}")


if __name__ == '__main__':
    main()
