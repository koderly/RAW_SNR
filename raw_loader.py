"""
Module for loading raw images in various formats.

This module provides a centralized function to load raw images from different formats
including Canon CR2, generic RAW files, and standard image formats like PNG and JPEG.
"""

import os
import warnings
import numpy as np
from typing import Union, Tuple, Optional


def load_raw_image(filepath: str, return_rgb: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, dict]]:
    """
    Load a raw image file in various formats.
    
    This function handles multiple image formats:
    - Canon CR2 files (using rawpy)
    - Standard image files (PNG, JPEG, etc.) using cv2
    - Generic RAW files (loaded as-is using numpy)
    
    Parameters
    ----------
    filepath : str
        Path to the image file to load.
    return_rgb : bool, optional
        If True and loading a CR2 file, returns the post-processed RGB image.
        If False, returns the raw Bayer pattern data. Default is False.
        
    Returns
    -------
    np.ndarray or tuple
        - For CR2 files with return_rgb=False: Returns the raw Bayer pattern array
        - For CR2 files with return_rgb=True: Returns the post-processed RGB array
        - For standard image files: Returns the image array as loaded by cv2
        - For generic RAW files: Returns the raw data as a numpy array
        
        When loading CR2 files with return_rgb=False, also returns a dict with
        metadata including 'raw_pattern' (Bayer pattern info).
        
    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    ValueError
        If the file format is not supported or cannot be loaded.
    ImportError
        If required libraries (rawpy, cv2) are not installed.
        
    Examples
    --------
    >>> # Load a CR2 file and get raw Bayer data
    >>> raw_data, metadata = load_raw_image('image.cr2', return_rgb=False)
    >>> print(raw_data.shape)
    >>> print(metadata['raw_pattern'])
    
    >>> # Load a CR2 file and get processed RGB
    >>> rgb_image = load_raw_image('image.cr2', return_rgb=True)
    
    >>> # Load a PNG file
    >>> image = load_raw_image('image.png')
    """
    # Check if file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Image file not found: {filepath}")
    
    # Get file extension
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()
    
    # Handle CR2 (Canon RAW) files
    if ext == '.cr2':
        try:
            import rawpy
        except ImportError:
            raise ImportError(
                "rawpy is required to load CR2 files. "
                "Install it with: pip install rawpy"
            )
        
        try:
            with rawpy.imread(filepath) as raw:
                if return_rgb:
                    # Return post-processed RGB image
                    rgb = raw.postprocess()
                    return rgb
                else:
                    # Return raw Bayer pattern data and metadata
                    raw_image = raw.raw_image_visible.copy()
                    metadata = {
                        'raw_pattern': raw.raw_pattern.copy(),
                        'color_desc': raw.color_desc,
                        'num_colors': raw.num_colors,
                        'raw_type': raw.raw_type
                    }
                    return raw_image, metadata
        except Exception as e:
            raise ValueError(f"Failed to load CR2 file {filepath}: {str(e)}")
    
    # Handle standard image formats (PNG, JPEG, etc.) using OpenCV
    elif ext in ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp']:
        try:
            import cv2
        except ImportError:
            # Fallback to matplotlib if cv2 is not available
            try:
                import matplotlib.image as mpimg
                image = mpimg.imread(filepath)
                return image
            except ImportError:
                raise ImportError(
                    "OpenCV (cv2) or matplotlib is required to load image files. "
                    "Install with: pip install opencv-python or pip install matplotlib"
                )
        
        # Load image with cv2
        image = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise ValueError(f"Failed to load image file: {filepath}")
        return image
    
    # Handle generic .raw files (attempt to load as binary)
    elif ext == '.raw':
        # Generic RAW files don't have a standard format
        # We'll load the raw binary data and let the user interpret it
        warnings.warn(
            f"Loading generic .raw file. You may need to reshape the data manually.",
            UserWarning
        )
        try:
            raw_data = np.fromfile(filepath, dtype=np.uint16)
            return raw_data
        except Exception as e:
            raise ValueError(f"Failed to load RAW file {filepath}: {str(e)}")
    
    else:
        raise ValueError(
            f"Unsupported file format: {ext}. "
            f"Supported formats: .cr2, .png, .jpg, .jpeg, .tif, .tiff, .bmp, .raw"
        )


def get_bayer_channels(raw_image: np.ndarray, bayer_pattern: np.ndarray) -> dict:
    """
    Extract individual Bayer color channels from a raw image.
    
    This function assumes an RGGB Bayer pattern layout where:
    - Pattern value 0 = Red
    - Pattern value 1 or 3 = Green
    - Pattern value 2 = Blue
    
    Parameters
    ----------
    raw_image : np.ndarray
        The raw Bayer pattern image (2D array).
    bayer_pattern : np.ndarray
        The Bayer pattern array (typically 2x2) indicating which color is at each position.
        Note: Currently this function assumes RGGB pattern. The parameter is provided
        for future extensibility.
        
    Returns
    -------
    dict
        Dictionary with keys 'R', 'G1', 'G2', 'B' containing the respective channel arrays.
        
    Examples
    --------
    >>> raw_image, metadata = load_raw_image('image.cr2', return_rgb=False)
    >>> channels = get_bayer_channels(raw_image, metadata['raw_pattern'])
    >>> print(channels['R'].shape)
    
    Notes
    -----
    The function currently assumes an RGGB Bayer pattern. For other patterns,
    manual channel extraction may be needed.
    """
    h, w = raw_image.shape
    
    # Extract channels based on RGGB Bayer pattern
    # Pattern layout:
    # [0, 1]    [R, G1]
    # [3, 2] or [G2, B]
    R = raw_image[0:h:2, 0:w:2]
    G1 = raw_image[0:h:2, 1:w:2]
    G2 = raw_image[1:h:2, 0:w:2]
    B = raw_image[1:h:2, 1:w:2]
    
    return {
        'R': R,
        'G1': G1,
        'G2': G2,
        'B': B
    }


if __name__ == "__main__":
    # Example usage and testing
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            print(f"Loading image: {filepath}")
            result = load_raw_image(filepath)
            
            if isinstance(result, tuple):
                image, metadata = result
                print(f"Loaded raw image with shape: {image.shape}")
                print(f"Data type: {image.dtype}")
                print(f"Value range: [{image.min()}, {image.max()}]")
                print(f"Metadata: {metadata}")
            else:
                image = result
                print(f"Loaded image with shape: {image.shape}")
                print(f"Data type: {image.dtype}")
                print(f"Value range: [{image.min()}, {image.max()}]")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("Usage: python raw_loader.py <image_path>")
        print("Example: python raw_loader.py image.cr2")
