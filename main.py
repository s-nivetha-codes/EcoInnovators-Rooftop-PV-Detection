"""
Main application for Solar Panel Installation Verification System
"""

import os
import json
import argparse
from verifier import SolarPanelVerifier
from pathlib import Path


def verify_solar_installation(user_image_path, satellite_image_path=None):
    """
    Main function to verify solar panel installation
    
    Args:
        user_image_path: Path to user's home image
        satellite_image_path: Optional path to satellite image
    
    Returns:
        Verification results as dictionary
    """
    print("=" * 60)
    print("SOLAR PANEL INSTALLATION VERIFICATION SYSTEM")
    print("=" * 60)
    print()

    # Validate input image
    if not os.path.exists(user_image_path):
        print(f"ERROR: User image not found at {user_image_path}")
        return None

    print(f"User Image: {user_image_path}")
    if satellite_image_path:
        print(f"Satellite Image: {satellite_image_path}")
    print()
    print("Processing image...")
    print()

    # Initialize verifier
    verifier = SolarPanelVerifier()

    # Perform verification
    results = verifier.verify_installation(user_image_path, satellite_image_path)

    # Display results
    print("=" * 60)
    print("VERIFICATION RESULTS")
    print("=" * 60)
    print()
    print(f"Status: {results['status']}")
    print(f"Verification Result: {results['verification_status']}")
    print(f"Solar Panels Detected: {results['solar_detected']}")
    print(f"Solar Coverage: {results['solar_coverage']:.2f}%")
    print(f"Similarity Score: {results['similarity_score']:.3f}")
    print(f"Confidence Level: {results['confidence']:.1%}")
    print()
    print(f"Message: {results['message']}")
    print()

    if results['output_image_path']:
        print(f"Output Image: {results['output_image_path']}")
        print()

    # Save results to JSON
    results_path = os.path.join('verification_results', 'latest_results.json')
    with open(results_path, 'w') as f:
        # Convert to serializable format
        serializable_results = {k: v for k, v in results.items() if k not in ['solar_image_path']}
        json.dump(serializable_results, f, indent=2)

    print(f"Results saved to: {results_path}")
    print()
    print("=" * 60)

    return results


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Solar Panel Installation Verification System'
    )
    parser.add_argument(
        'user_image',
        help='Path to user-uploaded home image'
    )
    parser.add_argument(
        '--satellite-image',
        help='Path to satellite image (optional)',
        default=None
    )

    args = parser.parse_args()

    # Verify installation
    results = verify_solar_installation(args.user_image, args.satellite_image)

    # Exit with appropriate code
    if results and results['verification_status'] == 'APPROVED':
        exit(0)
    else:
        exit(1)


if __name__ == '__main__':
    main()
