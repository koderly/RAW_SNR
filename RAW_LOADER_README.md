# RAW Image Loader

A Python module for loading raw images in various formats including Canon CR2, generic RAW files, and standard image formats.

## Features

- **Multiple Format Support**: Load CR2, RAW, PNG, JPEG, TIFF, and BMP files
- **Flexible Output**: Get raw Bayer data or processed RGB images from CR2 files
- **Bayer Channel Extraction**: Easily extract R, G1, G2, B channels from raw Bayer images
- **Error Handling**: Comprehensive error messages for missing files and unsupported formats
- **Type Hints**: Full type annotations for better IDE support

## Installation

Required dependencies:
```bash
pip install numpy opencv-python rawpy matplotlib
```

## Usage

### Basic Usage

```python
from raw_loader import load_raw_image

# Load a PNG file
image = load_raw_image('image.png')

# Load a CR2 file as raw Bayer data
raw_image, metadata = load_raw_image('image.cr2', return_rgb=False)
print(metadata['raw_pattern'])  # Bayer pattern information

# Load a CR2 file as processed RGB
rgb_image = load_raw_image('image.cr2', return_rgb=True)
```

### Extracting Bayer Channels

```python
from raw_loader import load_raw_image, get_bayer_channels

# Load CR2 file
raw_image, metadata = load_raw_image('image.cr2', return_rgb=False)

# Extract individual color channels
channels = get_bayer_channels(raw_image, metadata['raw_pattern'])

# Access individual channels
red_channel = channels['R']
green1_channel = channels['G1']
green2_channel = channels['G2']
blue_channel = channels['B']

# Calculate statistics
print(f"Red mean: {red_channel.mean():.2f}")
print(f"Red std: {red_channel.std():.2f}")
```

### Command Line Usage

You can also use the module from the command line:

```bash
python raw_loader.py image.cr2
python raw_loader.py image.png
python raw_loader.py image.raw
```

## Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| Canon RAW | `.cr2` | Returns raw Bayer data or processed RGB |
| PNG | `.png` | Standard image format |
| JPEG | `.jpg`, `.jpeg` | Standard image format |
| TIFF | `.tif`, `.tiff` | Standard image format |
| BMP | `.bmp` | Standard image format |
| Generic RAW | `.raw` | Returns raw binary data (requires manual reshaping) |

## Function Reference

### `load_raw_image(filepath, return_rgb=False)`

Load a raw image file in various formats.

**Parameters:**
- `filepath` (str): Path to the image file
- `return_rgb` (bool): If True and loading CR2, returns processed RGB (default: False)

**Returns:**
- For CR2 with `return_rgb=False`: `(np.ndarray, dict)` - raw image and metadata
- For CR2 with `return_rgb=True`: `np.ndarray` - processed RGB image
- For other formats: `np.ndarray` - image array

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If format is unsupported or file can't be loaded
- `ImportError`: If required libraries are not installed

### `get_bayer_channels(raw_image, bayer_pattern)`

Extract individual Bayer color channels from a raw image.

**Parameters:**
- `raw_image` (np.ndarray): Raw Bayer pattern image (2D array)
- `bayer_pattern` (np.ndarray): Bayer pattern array (typically 2x2)

**Returns:**
- `dict`: Dictionary with keys 'R', 'G1', 'G2', 'B' containing channel arrays

## Testing

Run the test suite:

```bash
python test_raw_loader.py
```

The test suite validates:
- PNG file loading
- CR2 raw Bayer data loading
- CR2 RGB processing
- Generic RAW file loading
- Error handling for missing/unsupported files
- Bayer channel extraction

## Examples

### Example 1: Calculate SNR from RAW Image

```python
from raw_loader import load_raw_image, get_bayer_channels
import numpy as np

# Load raw CR2 file
raw_image, metadata = load_raw_image('image.cr2', return_rgb=False)

# Extract channels
channels = get_bayer_channels(raw_image, metadata['raw_pattern'])

# Calculate SNR for each channel
for channel_name, channel_data in channels.items():
    mean = channel_data.mean()
    std = channel_data.std()
    snr = mean / std if std > 0 else 0
    print(f"{channel_name} SNR: {snr:.2f}")
```

### Example 2: Visualize Raw Image

```python
from raw_loader import load_raw_image
import matplotlib.pyplot as plt

# Load and display
image = load_raw_image('image.png')
plt.imshow(image, cmap='gray')
plt.title('Raw Image')
plt.show()
```

## Integration with Existing Code

This module replaces scattered image loading code throughout the repository:

**Before:**
```python
import rawpy
import imageio

with rawpy.imread(path) as raw:
    rgb = raw.postprocess()
```

**After:**
```python
from raw_loader import load_raw_image

rgb = load_raw_image(path, return_rgb=True)
```

## License

This module is part of the RAW_SNR repository.
