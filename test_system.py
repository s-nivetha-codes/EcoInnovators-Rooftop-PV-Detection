"""
Test script for Solar Panel Verification System
This script demonstrates how to use the system
"""

import os
import numpy as np
import cv2
from verifier import SolarPanelVerifier
from image_processor import ImageProcessor


def create_demo_image_with_solar_panels():
    """Create a demo image with simulated solar panels for testing"""
    # Create a background image (house/terrace)
    height, width = 600, 800
    image = np.ones((height, width, 3), dtype=np.uint8) * 220  # Light background
    
    # Add sky (light color to avoid confusion with panels)
    image[0:150, :] = [200, 180, 150]  # Light beige sky
    
    # Add building structure (brown roof)
    cv2.rectangle(image, (100, 150), (700, 500), (180, 140, 100), -1)  # Building
    
    # Add roof
    pts = np.array([[100, 150], [400, 50], [700, 150]], np.int32)
    cv2.polylines(image, [pts], True, (100, 100, 100), 3)
    cv2.fillPoly(image, [pts], (150, 140, 130))
    
    # Add solar panels (DARK BLUE rectangles on roof/terrace)
    # Solar panels are very dark blue (30, 60, 100) in BGR
    # Panel 1 - large panel
    cv2.rectangle(image, (120, 180), (280, 320), (100, 60, 30), -1)  # Dark blue BGR
    cv2.rectangle(image, (120, 180), (280, 320), (80, 40, 20), 3)
    
    # Panel 2 - large panel
    cv2.rectangle(image, (320, 180), (480, 320), (100, 60, 30), -1)  # Dark blue BGR
    cv2.rectangle(image, (320, 180), (480, 320), (80, 40, 20), 3)
    
    # Panel 3 - large panel
    cv2.rectangle(image, (520, 180), (680, 320), (100, 60, 30), -1)  # Dark blue BGR
    cv2.rectangle(image, (520, 180), (680, 320), (80, 40, 20), 3)
    
    # Add grid pattern on panels to look realistic
    for i in range(120, 680, 40):
        cv2.line(image, (i, 180), (i, 320), (60, 30, 15), 1)
    for j in range(180, 321, 35):
        cv2.line(image, (120, j), (680, j), (60, 30, 15), 1)
    
    # Add some light noise
    noise = np.random.normal(0, 5, image.shape).astype(np.uint8)
    image = cv2.add(image, noise)
    
    return image


def create_demo_image_without_solar_panels():
    """Create a demo image without solar panels for testing rejection"""
    height, width = 600, 800
    image = np.ones((height, width, 3), dtype=np.uint8) * 220  # Light background
    
    # Add sky
    image[0:150, :] = [200, 180, 150]  # Light beige sky
    
    # Add building structure
    cv2.rectangle(image, (100, 150), (700, 500), (180, 140, 100), -1)  # Building
    
    # Add traditional red-brown roof WITHOUT panels
    pts = np.array([[100, 150], [400, 50], [700, 150]], np.int32)
    cv2.polylines(image, [pts], True, (100, 100, 100), 3)
    cv2.fillPoly(image, [pts], (80, 100, 160))  # Red/brown roof
    
    # Add some texture/tiles to roof
    for i in range(100, 700, 40):
        for j in range(50, 200, 30):
            cv2.line(image, (i, j), (i + 30, j), (70, 90, 150), 1)
            cv2.line(image, (i, j), (i, j + 25), (70, 90, 150), 1)
    
    # Add some light noise
    noise = np.random.normal(0, 5, image.shape).astype(np.uint8)
    image = cv2.add(image, noise)
    
    return image


def run_tests():
    """Run demo tests"""
    print("=" * 70)
    print("SOLAR PANEL VERIFICATION SYSTEM - TEST SUITE")
    print("=" * 70)
    print()
    
    # Create test images
    print("Creating test images...")
    demo_with_panels = create_demo_image_with_solar_panels()
    demo_without_panels = create_demo_image_without_solar_panels()
    
    # Save test images
    os.makedirs('test_images', exist_ok=True)
    with_panels_path = 'test_images/house_with_solar_panels.jpg'
    without_panels_path = 'test_images/house_without_solar_panels.jpg'
    
    cv2.imwrite(with_panels_path, demo_with_panels)
    cv2.imwrite(without_panels_path, demo_without_panels)
    
    print(f"✓ Created: {with_panels_path}")
    print(f"✓ Created: {without_panels_path}")
    print()
    
    # Test 1: Verify house WITH solar panels
    print("-" * 70)
    print("TEST 1: House WITH Solar Panels (Should be APPROVED)")
    print("-" * 70)
    print()
    
    verifier = SolarPanelVerifier()
    results1 = verifier.verify_installation(with_panels_path)
    
    print(f"Status: {results1['status']}")
    print(f"Verification Result: {results1['verification_status']}")
    print(f"Solar Detected: {results1['solar_detected']}")
    print(f"Solar Coverage: {results1['solar_coverage']:.2f}%")
    print(f"Confidence: {results1['confidence']:.1%}")
    print(f"Message: {results1['message']}")
    print(f"Output: {results1['output_image_path']}")
    print()
    
    # Test 2: Verify house WITHOUT solar panels
    print("-" * 70)
    print("TEST 2: House WITHOUT Solar Panels (Should be REJECTED)")
    print("-" * 70)
    print()
    
    results2 = verifier.verify_installation(without_panels_path)
    
    print(f"Status: {results2['status']}")
    print(f"Verification Result: {results2['verification_status']}")
    print(f"Solar Detected: {results2['solar_detected']}")
    print(f"Solar Coverage: {results2['solar_coverage']:.2f}%")
    print(f"Confidence: {results2['confidence']:.1%}")
    print(f"Message: {results2['message']}")
    print(f"Output: {results2['output_image_path']}")
    print()
    
    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    test1_pass = results1['verification_status'] == 'APPROVED'
    test2_pass = results2['verification_status'] == 'REJECTED'
    
    print(f"Test 1 (With Panels): {'✓ PASSED' if test1_pass else '✗ FAILED'}")
    print(f"Test 2 (Without Panels): {'✓ PASSED' if test2_pass else '✗ FAILED'}")
    print()
    
    if test1_pass and test2_pass:
        print("✓ All tests passed successfully!")
    else:
        print("✗ Some tests failed. Check the results above.")
    
    print()
    print("=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print()
    print("To use with your own image:")
    print('  python main.py "path/to/your/image.jpg"')
    print()
    print("Example:")
    print('  python main.py "C:\\Users\\amith\\Downloads\\house.jpg"')
    print()


if __name__ == '__main__':
    run_tests()
