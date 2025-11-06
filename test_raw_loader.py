#!/usr/bin/env python3
"""
Test script for raw_loader module.

This script tests the raw_loader functionality with various image formats
found in the repository.
"""

import os
import tempfile
from raw_loader import load_raw_image, get_bayer_channels


def test_png_loading():
    """Test loading a PNG file."""
    print("=" * 60)
    print("Test 1: Loading PNG file")
    print("=" * 60)
    
    filepath = 'template1.png'
    if not os.path.exists(filepath):
        print(f"SKIP: {filepath} not found")
        return
    
    try:
        image = load_raw_image(filepath)
        print(f"✓ Successfully loaded: {filepath}")
        print(f"  Shape: {image.shape}")
        print(f"  Data type: {image.dtype}")
        print(f"  Value range: [{image.min()}, {image.max()}]")
    except Exception as e:
        print(f"✗ Failed: {e}")


def test_cr2_raw_loading():
    """Test loading a CR2 file as raw Bayer data."""
    print("\n" + "=" * 60)
    print("Test 2: Loading CR2 file (raw Bayer data)")
    print("=" * 60)
    
    filepath = '00137_11_00100_0.01_Outdoor.cr2'
    if not os.path.exists(filepath):
        print(f"SKIP: {filepath} not found")
        return
    
    try:
        raw_image, metadata = load_raw_image(filepath, return_rgb=False)
        print(f"✓ Successfully loaded: {filepath}")
        print(f"  Shape: {raw_image.shape}")
        print(f"  Data type: {raw_image.dtype}")
        print(f"  Value range: [{raw_image.min()}, {raw_image.max()}]")
        print(f"  Bayer pattern: {metadata['raw_pattern']}")
        print(f"  Color description: {metadata['color_desc']}")
        print(f"  Number of colors: {metadata['num_colors']}")
        
        # Test Bayer channel extraction
        print("\n  Extracting Bayer channels:")
        channels = get_bayer_channels(raw_image, metadata['raw_pattern'])
        for key, val in channels.items():
            print(f"    {key}: shape={val.shape}, mean={val.mean():.2f}, std={val.std():.2f}")
            
    except Exception as e:
        print(f"✗ Failed: {e}")


def test_cr2_rgb_loading():
    """Test loading a CR2 file as processed RGB."""
    print("\n" + "=" * 60)
    print("Test 3: Loading CR2 file (processed RGB)")
    print("=" * 60)
    
    filepath = '00137_11_00100_0.01_Outdoor.cr2'
    if not os.path.exists(filepath):
        print(f"SKIP: {filepath} not found")
        return
    
    try:
        rgb_image = load_raw_image(filepath, return_rgb=True)
        print(f"✓ Successfully loaded: {filepath}")
        print(f"  Shape: {rgb_image.shape}")
        print(f"  Data type: {rgb_image.dtype}")
        print(f"  Value range: [{rgb_image.min()}, {rgb_image.max()}]")
        print(f"  RGB channels: {rgb_image.shape[2] if len(rgb_image.shape) == 3 else 'N/A'}")
    except Exception as e:
        print(f"✗ Failed: {e}")


def test_raw_loading():
    """Test loading a generic .raw file."""
    print("\n" + "=" * 60)
    print("Test 4: Loading generic RAW file")
    print("=" * 60)
    
    filepath = 'Image__2024-09-04__18-13-43.raw'
    if not os.path.exists(filepath):
        print(f"SKIP: {filepath} not found")
        return
    
    try:
        raw_data = load_raw_image(filepath)
        print(f"✓ Successfully loaded: {filepath}")
        print(f"  Shape: {raw_data.shape}")
        print(f"  Data type: {raw_data.dtype}")
        print(f"  Value range: [{raw_data.min()}, {raw_data.max()}]")
        print(f"  Note: Generic .raw files need manual reshaping based on image dimensions")
    except Exception as e:
        print(f"✗ Failed: {e}")


def test_error_handling():
    """Test error handling for non-existent files."""
    print("\n" + "=" * 60)
    print("Test 5: Error handling")
    print("=" * 60)
    
    try:
        load_raw_image('nonexistent.cr2')
        print("✗ Should have raised FileNotFoundError")
    except FileNotFoundError as e:
        print(f"✓ Correctly raised FileNotFoundError")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    # Test unsupported format (create a temporary file with unsupported extension)
    try:
        with tempfile.NamedTemporaryFile(suffix='.unsupported', delete=False) as f:
            temp_path = f.name
            f.write(b'test')
        
        try:
            load_raw_image(temp_path)
            print("✗ Should have raised ValueError for unsupported format")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError for unsupported format")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
        finally:
            os.unlink(temp_path)
    except Exception as e:
        print(f"✗ Could not test unsupported format: {e}")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("RAW IMAGE LOADER TEST SUITE")
    print("=" * 60)
    
    test_png_loading()
    test_cr2_raw_loading()
    test_cr2_rgb_loading()
    test_raw_loading()
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
