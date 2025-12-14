"""
Main verification module for solar panel installation
"""

import os
import cv2
import numpy as np
from datetime import datetime
from image_processor import ImageProcessor
import config


class SolarPanelVerifier:
    """Main verifier class for solar panel installations"""

    def __init__(self):
        """Initialize the verifier"""
        self.processor = ImageProcessor()
        self.create_output_dirs()

    def create_output_dirs(self):
        """Create output directories if they don't exist"""
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        os.makedirs(config.TEMP_DIR, exist_ok=True)

    def verify_installation(self, user_image_path, satellite_image_path=None):
        """
        Main verification method
        
        Args:
            user_image_path: Path to user-uploaded home image
            satellite_image_path: Path to satellite image (optional)
        
        Returns:
            Dictionary with verification results
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'status': 'PROCESSING',
            'user_image_path': user_image_path,
            'satellite_image_path': satellite_image_path,
            'solar_detected': False,
            'solar_coverage': 0,
            'similarity_score': 0,
            'verification_status': 'REJECTED',
            'confidence': 0,
            'output_image_path': None,
            'message': ''
        }

        try:
            # Load user image
            user_image = self.processor.load_image(user_image_path)
            if user_image is None:
                results['status'] = 'ERROR'
                results['message'] = 'Failed to load user image'
                return results

            # Preprocess image
            processed_image = self.processor.preprocess_image(user_image)

            # Detect solar panels
            solar_panels, mask = self.processor.detect_solar_panels(processed_image)
            
            if len(solar_panels) == 0:
                results['solar_detected'] = False
                results['solar_coverage'] = 0
                results['verification_status'] = 'REJECTED'
                results['message'] = 'No solar panels detected in the image'
                results['status'] = 'COMPLETED'
                return results

            results['solar_detected'] = True

            # Calculate solar coverage
            coverage = self.processor.calculate_solar_coverage(mask)
            results['solar_coverage'] = round(coverage, 2)

            # If satellite image provided, compare
            if satellite_image_path and os.path.exists(satellite_image_path):
                satellite_image = self.processor.load_image(satellite_image_path)
                if satellite_image is not None:
                    similarity = self.processor.compare_images(user_image, satellite_image)
                    results['similarity_score'] = round(similarity, 3)
                else:
                    results['similarity_score'] = 0

            # Determine verification status
            confidence = self._calculate_confidence(
                results['solar_coverage'],
                results['similarity_score'],
                len(solar_panels)
            )

            results['confidence'] = round(confidence, 3)

            if confidence >= config.MIN_CONFIDENCE_THRESHOLD:
                results['verification_status'] = 'APPROVED'
                results['message'] = f'Solar installation verified successfully (Confidence: {confidence:.1%})'
            else:
                results['verification_status'] = 'REJECTED'
                results['message'] = f'Solar installation verification failed (Confidence: {confidence:.1%})'

            # Generate output image
            output_image_path = self._generate_output_image(
                user_image, processed_image, solar_panels, mask, results
            )
            results['output_image_path'] = output_image_path

            results['status'] = 'COMPLETED'

        except Exception as e:
            results['status'] = 'ERROR'
            results['message'] = str(e)

        return results

    def _calculate_confidence(self, coverage, similarity, panel_count):
        """
        Calculate confidence score for verification
        
        Args:
            coverage: Solar panel coverage percentage
            similarity: Image similarity score (0-1)
            panel_count: Number of panels detected
        
        Returns:
            Confidence score between 0 and 1
        """
        # Weight factors
        coverage_weight = 0.4
        similarity_weight = 0.3
        panel_weight = 0.3

        # Normalize coverage (0-10% gives 0, >5% gives higher score)
        coverage_score = min(1.0, coverage / 10.0)

        # Panel detection score
        panel_score = min(1.0, panel_count / 5.0)

        # Calculate weighted confidence
        confidence = (
            coverage_score * coverage_weight +
            similarity * similarity_weight +
            panel_score * panel_weight
        )

        return confidence

    def _generate_output_image(self, original, processed, panels, mask, results):
        """
        Generate output image with annotations
        
        Returns:
            Path to output image
        """
        # Draw solar panels
        annotated = self.processor.draw_solar_panels(original, panels)

        # Create composite image
        height, width = annotated.shape[:2]
        output = np.zeros((height, width + 300, 3), dtype=np.uint8)
        output[:, :width] = annotated

        # Add text information
        info_x = width + 10
        info_y = 30
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_color = (255, 255, 255)
        line_height = 30

        # Status color
        status_color = (0, 255, 0) if results['verification_status'] == 'APPROVED' else (0, 0, 255)

        cv2.rectangle(output, (width, 0), (width + 300, height), (50, 50, 50), -1)
        
        cv2.putText(output, 'VERIFICATION REPORT', (info_x, info_y), font, 0.7, (255, 255, 0), 1)
        
        info_y += line_height
        cv2.putText(output, f"Status: {results['verification_status']}", (info_x, info_y), font, font_scale, status_color, 1)
        
        info_y += line_height
        cv2.putText(output, f"Coverage: {results['solar_coverage']:.2f}%", (info_x, info_y), font, font_scale, font_color, 1)
        
        info_y += line_height
        cv2.putText(output, f"Confidence: {results['confidence']:.1%}", (info_x, info_y), font, font_scale, font_color, 1)
        
        info_y += line_height
        cv2.putText(output, f"Panels: {len(panels)}", (info_x, info_y), font, font_scale, font_color, 1)

        # Save output image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(
            config.OUTPUT_DIR,
            f"verification_{timestamp}.png"
        )

        cv2.imwrite(output_path, output)
        return output_path
