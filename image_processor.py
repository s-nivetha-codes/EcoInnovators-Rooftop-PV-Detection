"""
Image processing module for solar panel detection
"""

import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from skimage import exposure
import config


class ImageProcessor:
    """Handles image processing and solar panel detection"""

    @staticmethod
    def load_image(image_path):
        """Load image from file path"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image from {image_path}")
            return image
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    @staticmethod
    def preprocess_image(image):
        """Preprocess image for analysis"""
        # Resize if too large
        height, width = image.shape[:2]
        if width > 2048 or height > 2048:
            scale = min(2048 / width, 2048 / height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height))
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Apply histogram equalization
        hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])
        
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    @staticmethod
    def detect_solar_panels(image):
        """
        Detect solar panels in the image
        Solar panels typically have dark blue/black colors and rectangular shape
        """
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Solar panels are very dark with blue hue (not brown/red)
        # Define range for dark blue color (solar panel specific)
        lower_blue1 = np.array([80, 50, 20])      # Blue range lower
        upper_blue1 = np.array([140, 255, 150])   # Blue range upper
        
        # Create mask for dark blue colors
        mask1 = cv2.inRange(hsv, lower_blue1, upper_blue1)
        
        # Exclude brown/red colors (roof material)
        lower_brown = np.array([0, 40, 30])
        upper_brown = np.array([25, 255, 180])
        mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
        
        lower_brown2 = np.array([160, 40, 30])
        upper_brown2 = np.array([180, 255, 180])
        mask_brown2 = cv2.inRange(hsv, lower_brown2, upper_brown2)
        
        # Combine brown masks
        mask_brown_combined = cv2.bitwise_or(mask_brown, mask_brown2)
        
        # Remove brown regions from blue mask
        mask = cv2.bitwise_and(mask1, cv2.bitwise_not(mask_brown_combined))
        
        # Apply morphological operations to improve mask
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area and shape (solar panels should be rectangular)
        solar_panels = []
        image_area = image.shape[0] * image.shape[1]
        min_area = image_area * 0.002  # At least 0.2% of image
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Check area
            if area < min_area:
                continue
            
            # Check if contour is roughly rectangular
            perimeter = cv2.arcLength(contour, True)
            if perimeter > 0:
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
                
                # Solar panels should have 4 sides (rectangle)
                if len(approx) >= 4:  # Allow more than 4 for irregular rectangles
                    # Check aspect ratio (should be close to rectangular)
                    x, y, w, h = cv2.boundingRect(contour)
                    if h > 0:
                        aspect_ratio = float(w) / h
                        
                        # Accept if aspect ratio is reasonable (not too extreme)
                        if 0.2 < aspect_ratio < 5.0:
                            solar_panels.append(contour)
        
        return solar_panels, mask

    @staticmethod
    def calculate_solar_coverage(mask):
        """Calculate percentage of solar panels detected"""
        total_pixels = mask.size
        solar_pixels = np.count_nonzero(mask)
        coverage_percentage = (solar_pixels / total_pixels) * 100
        return coverage_percentage

    @staticmethod
    def compare_images(image1, image2):
        """
        Compare two images for similarity
        Returns similarity score between 0 and 1
        """
        # Resize images to same size
        height = min(image1.shape[0], image2.shape[0])
        width = min(image1.shape[1], image2.shape[1])
        
        img1_resized = cv2.resize(image1, (width, height))
        img2_resized = cv2.resize(image2, (width, height))
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1_resized, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)
        
        # Calculate SSIM (Structural Similarity Index)
        similarity_score = ssim(gray1, gray2)
        
        return max(0, min(1, (similarity_score + 1) / 2))  # Normalize to 0-1

    @staticmethod
    def draw_solar_panels(image, solar_panels):
        """Draw detected solar panels on image"""
        output_image = image.copy()
        
        for i, panel in enumerate(solar_panels):
            # Draw contour
            cv2.drawContours(output_image, [panel], 0, (0, 255, 0), 2)
            
            # Draw bounding rectangle
            x, y, w, h = cv2.boundingRect(panel)
            cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        return output_image
