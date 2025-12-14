"""
Configuration settings for Solar Panel Verification System
"""

# Image processing settings
MIN_CONFIDENCE_THRESHOLD = 0.45
SOLAR_PANEL_COLOR_RANGE = {
    'blue': (100, 150),
    'hue': (100, 130)
}

# Image comparison settings
STRUCTURAL_SIMILARITY_THRESHOLD = 0.5
FEATURE_MATCH_THRESHOLD = 50

# Output settings
OUTPUT_DIR = 'verification_results'
TEMP_DIR = 'temp_images'

# API settings (for satellite imagery)
SATELLITE_API_TIMEOUT = 30
MAX_IMAGE_SIZE = (2048, 2048)
