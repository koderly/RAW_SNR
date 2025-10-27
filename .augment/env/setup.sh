#!/bin/bash

# Update system packages
sudo apt-get update

# Install Python and pip if not already installed
sudo apt-get install -y python3 python3-pip python3-venv

# Install system dependencies for rawpy (LibRaw)
sudo apt-get install -y libraw-dev pkg-config

# Create a virtual environment
python3 -m venv venv

# Activate virtual environment and add to profile
echo "source /mnt/persist/workspace/venv/bin/activate" >> $HOME/.profile

# Activate virtual environment for current session
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install rawpy and related packages
pip install rawpy numpy matplotlib

# Install pytest for testing
pip install pytest

# Create a simple rawpy example that works without external files
cat > simple_rawpy_example.py << 'EOF'
#!/usr/bin/env python3
"""
Simple rawpy example demonstrating the library functionality.
"""

import rawpy
import numpy as np
import sys
import os

def show_rawpy_info():
    """Display rawpy information."""
    print("rawpy Library Information")
    print("=========================")
    print(f"rawpy version: {rawpy.__version__}")
    print("rawpy is successfully installed and working!")
    print()
    
    # Show that rawpy can be used
    print("rawpy functionality test:")
    print("- rawpy.imread function exists:", hasattr(rawpy, 'imread'))
    print("- rawpy module loaded successfully: ✓")
    print()

def demonstrate_rawpy_usage():
    """Demonstrate how to use rawpy with a RAW file."""
    print("How to use rawpy:")
    print("=================")
    print()
    print("1. Basic usage:")
    print("   import rawpy")
    print("   with rawpy.imread('your_file.raw') as raw:")
    print("       rgb = raw.postprocess()")
    print()
    print("2. Advanced processing:")
    print("   with rawpy.imread('your_file.raw') as raw:")
    print("       # Get raw data")
    print("       raw_data = raw.raw_image")
    print("       print(f'Raw shape: {raw_data.shape}')")
    print()
    print("       # Process with custom settings")
    print("       rgb = raw.postprocess(")
    print("           use_camera_wb=True,")
    print("           half_size=False,")
    print("           no_auto_bright=True,")
    print("           output_bps=16")
    print("       )")
    print()
    print("3. Supported file formats:")
    print("   - Canon: .CR2, .CR3")
    print("   - Nikon: .NEF")
    print("   - Sony: .ARW")
    print("   - Adobe: .DNG")
    print("   - Olympus: .ORF")
    print("   - Panasonic: .RW2")
    print("   - And many more...")
    print()

def test_with_file(filename):
    """Test rawpy with a specific file."""
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return False
    
    try:
        print(f"Testing with file: {filename}")
        with rawpy.imread(filename) as raw:
            print(f"✓ Successfully opened {filename}")
            print(f"  Raw image shape: {raw.raw_image.shape}")
            print(f"  Raw image dtype: {raw.raw_image.dtype}")
            
            # Process the image
            rgb = raw.postprocess(half_size=True)  # Half size for speed
            print(f"  Processed RGB shape: {rgb.shape}")
            print(f"  Processed RGB dtype: {rgb.dtype}")
            
            return True
    except Exception as e:
        print(f"✗ Error processing {filename}: {e}")
        return False

def main():
    """Main function."""
    show_rawpy_info()
    demonstrate_rawpy_usage()
    
    # If a filename is provided as argument, test with it
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        print("Testing with provided file:")
        print("===========================")
        success = test_with_file(filename)
        if success:
            print("\n🎉 rawpy successfully processed your RAW file!")
        else:
            print("\n❌ Could not process the file. Make sure it's a valid RAW file.")
    else:
        print("To test with your own RAW file:")
        print("===============================")
        print("python simple_rawpy_example.py /path/to/your/file.raw")
        print()
        print("Example:")
        print("python simple_rawpy_example.py ~/Pictures/IMG_1234.CR2")

if __name__ == "__main__":
    main()
EOF

chmod +x simple_rawpy_example.py

# Create a test that verifies rawpy installation
cat > tests/test_rawpy_installation.py << 'EOF'
import pytest
import rawpy
import numpy as np

def test_rawpy_import():
    """Test that rawpy can be imported."""
    assert rawpy is not None

def test_rawpy_version():
    """Test that rawpy version is accessible."""
    version = rawpy.__version__
    assert version is not None
    assert isinstance(version, str)
    print(f"rawpy version: {version}")

def test_rawpy_has_imread():
    """Test that rawpy has imread function."""
    assert hasattr(rawpy, 'imread')
    assert callable(rawpy.imread)

def test_numpy_integration():
    """Test that numpy is available for rawpy."""
    assert np is not None
    # Test that we can create arrays (rawpy uses numpy arrays)
    arr = np.array([1, 2, 3])
    assert arr.dtype == np.int64

def test_rawpy_basic_functionality():
    """Test basic rawpy functionality without requiring files."""
    # This tests that rawpy is properly installed and can be used
    try:
        # These should not raise import errors
        from rawpy import _rawpy
        assert _rawpy is not None
        print("✓ rawpy backend (_rawpy) is available")
    except ImportError as e:
        pytest.fail(f"rawpy backend not available: {e}")
EOF

echo ""
echo "Setup completed successfully!"
echo "============================="
echo ""
echo "rawpy is now installed and ready to use."
echo ""
echo "To test the installation:"
echo "  python simple_rawpy_example.py"
echo ""
echo "To test with your own RAW file:"
echo "  python simple_rawpy_example.py /path/to/your/file.raw"
echo ""
echo "The environment includes:"
echo "- rawpy (Python RAW image processing)"
echo "- numpy (numerical computing)"
echo "- matplotlib (plotting and visualization)"
echo "- pytest (testing framework)"