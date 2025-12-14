"""
Tkinter-based GUI for Solar Panel Verification System
Lightweight alternative GUI using built-in Tkinter
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import scrolledtext
import os
from PIL import Image, ImageTk
import threading
from verifier import SolarPanelVerifier
import config


class SolarPanelVerificationGUI:
    """Tkinter-based GUI for Solar Panel Verification"""

    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("Solar Panel Installation Verification System")
        self.root.geometry("1000x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize verifier
        self.verifier = SolarPanelVerifier()
        self.current_user_image = None
        self.current_satellite_image = None
        self.current_results = None
        
        # Configure styles
        self.setup_styles()
        
        # Create GUI
        self.create_widgets()

    def setup_styles(self):
        """Setup GUI styles"""
        self.root.option_add('*Font', 'Arial 10')
        
        # Colors
        self.primary_color = '#2E8B57'
        self.danger_color = '#DC143C'
        self.bg_color = '#f0f0f0'
        self.text_bg = '#ffffff'

    def create_widgets(self):
        """Create GUI widgets"""
        # Title
        title_frame = tk.Frame(self.root, bg=self.primary_color)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(
            title_frame,
            text="🔆 SOLAR PANEL INSTALLATION VERIFICATION SYSTEM",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg=self.primary_color,
            pady=10
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="PM Surya Ghar Yojana Verification Tool",
            font=('Arial', 9),
            fg='#FFD700',
            bg=self.primary_color
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Main content frame with scrollbar
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # User image section
        self.create_section(main_frame, "STEP 1: Upload Home Image", 0)
        
        user_image_frame = tk.Frame(main_frame, bg=self.text_bg, relief=tk.SUNKEN, bd=2)
        user_image_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=5, padx=5)
        
        user_button_frame = tk.Frame(user_image_frame, bg=self.text_bg)
        user_button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(user_button_frame, text="📁 Browse User Image", 
                 command=self.load_user_image,
                 bg=self.primary_color, fg='white',
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.user_image_label = tk.Label(user_button_frame, text="No image selected",
                                        bg=self.text_bg, fg='gray')
        self.user_image_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # User image preview
        self.user_image_preview = tk.Label(user_image_frame, bg='#e0e0e0', 
                                          width=40, height=15,
                                          text="Image Preview")
        self.user_image_preview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Satellite image section
        self.create_section(main_frame, "STEP 2: Upload Satellite Image (Optional)", 2)
        
        sat_image_frame = tk.Frame(main_frame, bg=self.text_bg, relief=tk.SUNKEN, bd=2)
        sat_image_frame.grid(row=3, column=0, columnspan=2, sticky='nsew', pady=5, padx=5)
        
        sat_button_frame = tk.Frame(sat_image_frame, bg=self.text_bg)
        sat_button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(sat_button_frame, text="📁 Browse Satellite Image", 
                 command=self.load_satellite_image,
                 bg=self.primary_color, fg='white',
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.sat_image_label = tk.Label(sat_button_frame, text="No image selected",
                                       bg=self.text_bg, fg='gray')
        self.sat_image_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Satellite image preview
        self.sat_image_preview = tk.Label(sat_image_frame, bg='#e0e0e0',
                                         width=40, height=15,
                                         text="Image Preview")
        self.sat_image_preview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg=self.bg_color)
        buttons_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=10)
        
        tk.Button(buttons_frame, text="✓ VERIFY INSTALLATION",
                 command=self.verify_installation,
                 bg=self.primary_color, fg='white',
                 font=('Arial', 11, 'bold'),
                 padx=20, pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="🔄 Clear",
                 command=self.clear_all,
                 bg='#4169E1', fg='white',
                 font=('Arial', 10),
                 padx=15, pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="❌ Exit",
                 command=self.root.quit,
                 bg=self.danger_color, fg='white',
                 font=('Arial', 10),
                 padx=15, pady=10).pack(side=tk.LEFT, padx=5)
        
        # Results section
        self.create_section(main_frame, "VERIFICATION RESULTS", 5)
        
        # Output text area
        output_frame = tk.Frame(main_frame, bg=self.text_bg, relief=tk.SUNKEN, bd=2)
        output_frame.grid(row=6, column=0, columnspan=2, sticky='nsew', pady=5, padx=5)
        
        scrollbar = ttk.Scrollbar(output_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=15,
            width=100,
            bg=self.text_bg,
            fg='#2d2d2d',
            font=('Courier', 9),
            yscrollcommand=scrollbar.set
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.config(command=self.output_text.yview)
        
        # Configure grid weights
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_rowconfigure(6, weight=2)
        main_frame.grid_columnconfigure(0, weight=1)

    def create_section(self, parent, title, row):
        """Create a section title"""
        section_label = tk.Label(
            parent,
            text=title,
            font=('Arial', 11, 'bold'),
            bg=self.bg_color,
            fg=self.primary_color
        )
        section_label.grid(row=row, column=0, columnspan=2, sticky='w', pady=(10, 5), padx=5)

    def load_user_image(self):
        """Load user image"""
        file_path = filedialog.askopenfilename(
            title="Select Home Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.current_user_image = file_path
            self.user_image_label.config(text=os.path.basename(file_path), fg='black')
            self.display_image_preview(file_path, self.user_image_preview)
            self.output_text.insert(tk.END, f"✓ User image loaded: {os.path.basename(file_path)}\n")
            self.output_text.see(tk.END)

    def load_satellite_image(self):
        """Load satellite image"""
        file_path = filedialog.askopenfilename(
            title="Select Satellite Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.current_satellite_image = file_path
            self.sat_image_label.config(text=os.path.basename(file_path), fg='black')
            self.display_image_preview(file_path, self.sat_image_preview)
            self.output_text.insert(tk.END, f"✓ Satellite image loaded: {os.path.basename(file_path)}\n")
            self.output_text.see(tk.END)

    def display_image_preview(self, image_path, label_widget):
        """Display image preview"""
        try:
            image = Image.open(image_path)
            # Resize image to fit preview
            image.thumbnail((300, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            label_widget.config(image=photo, text="")
            label_widget.image = photo  # Keep a reference
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image preview: {str(e)}")

    def verify_installation(self):
        """Verify installation"""
        if not self.current_user_image:
            messagebox.showerror("Error", "Please upload a home image first")
            return
        
        # Disable verify button during processing
        self.output_text.insert(tk.END, "\n⏳ Verifying installation... Please wait.\n")
        self.output_text.see(tk.END)
        self.root.update()
        
        try:
            # Perform verification
            results = self.verifier.verify_installation(
                self.current_user_image,
                self.current_satellite_image
            )
            self.current_results = results
            
            # Display results
            self.output_text.insert(tk.END, "\n" + "="*70 + "\n")
            self.output_text.insert(tk.END, "VERIFICATION RESULTS\n")
            self.output_text.insert(tk.END, "="*70 + "\n\n")
            
            if results['status'] == 'COMPLETED':
                status_symbol = "✅" if results['verification_status'] == 'APPROVED' else "❌"
                self.output_text.insert(tk.END, f"{status_symbol} Status: {results['verification_status']}\n")
                self.output_text.insert(tk.END, f"Solar Detected: {'Yes' if results['solar_detected'] else 'No'}\n")
                self.output_text.insert(tk.END, f"Solar Coverage: {results['solar_coverage']:.2f}%\n")
                self.output_text.insert(tk.END, f"Confidence Level: {results['confidence']:.1%}\n")
                self.output_text.insert(tk.END, f"Similarity Score: {results['similarity_score']:.3f}\n")
                self.output_text.insert(tk.END, f"\nMessage: {results['message']}\n")
                
                if results['output_image_path']:
                    self.output_text.insert(tk.END, f"\n📸 Output Image: {results['output_image_path']}\n")
            else:
                self.output_text.insert(tk.END, f"Error: {results['message']}\n")
            
            self.output_text.insert(tk.END, "\n" + "="*70 + "\n")
            self.output_text.see(tk.END)
            
        except Exception as e:
            self.output_text.insert(tk.END, f"\n❌ Error: {str(e)}\n")
            self.output_text.see(tk.END)

    def clear_all(self):
        """Clear all data"""
        self.current_user_image = None
        self.current_satellite_image = None
        self.current_results = None
        
        self.user_image_label.config(text="No image selected", fg='gray')
        self.sat_image_label.config(text="No image selected", fg='gray')
        self.user_image_preview.config(image='', text="Image Preview")
        self.sat_image_preview.config(image='', text="Image Preview")
        self.output_text.delete(1.0, tk.END)
        
        messagebox.showinfo("Cleared", "All data has been cleared")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SolarPanelVerificationGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
