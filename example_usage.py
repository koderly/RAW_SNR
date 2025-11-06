"""
Example script showing how to use raw_loader with existing RAW_SNR workflows.

This demonstrates integration of the raw_loader module with the existing
SNR calculation and ROI analysis code.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from raw_loader import load_raw_image, get_bayer_channels


def calculate_roi_snr(raw_image, bayer_pattern, roi):
    """
    Calculate SNR for each Bayer channel in a selected ROI.
    
    Parameters
    ----------
    raw_image : np.ndarray
        The raw Bayer pattern image
    bayer_pattern : np.ndarray
        The Bayer pattern array
    roi : tuple
        ROI coordinates (x1, y1, x2, y2)
        
    Returns
    -------
    dict
        SNR values for each channel
    """
    x1, y1, x2, y2 = roi
    selected_region = raw_image[y1:y2, x1:x2]
    
    # Extract channels from the selected region
    red_values = []
    green1_values = []
    green2_values = []
    blue_values = []
    
    # Traverse through the selected region and categorize pixel values
    for i in range(selected_region.shape[0]):
        for j in range(selected_region.shape[1]):
            pattern_position = bayer_pattern[i % 2, j % 2]
            if pattern_position == 0:  # Red
                red_values.append(selected_region[i, j])
            elif pattern_position == 1:  # Green (G1 or G2)
                if i % 2 == 0:
                    green1_values.append(selected_region[i, j])
                else:
                    green2_values.append(selected_region[i, j])
            elif pattern_position == 2 or pattern_position == 3:  # Blue
                blue_values.append(selected_region[i, j])
    
    # Calculate statistics
    results = {}
    
    if red_values:
        avg_red = np.mean(red_values)
        std_red = np.std(red_values)
        results['R'] = {
            'mean': avg_red,
            'std': std_red,
            'snr': avg_red / std_red if std_red > 0 else 0
        }
    
    if green1_values:
        avg_green1 = np.mean(green1_values)
        std_green1 = np.std(green1_values)
        results['G1'] = {
            'mean': avg_green1,
            'std': std_green1,
            'snr': avg_green1 / std_green1 if std_green1 > 0 else 0
        }
    
    if green2_values:
        avg_green2 = np.mean(green2_values)
        std_green2 = np.std(green2_values)
        results['G2'] = {
            'mean': avg_green2,
            'std': std_green2,
            'snr': avg_green2 / std_green2 if std_green2 > 0 else 0
        }
    
    if blue_values:
        avg_blue = np.mean(blue_values)
        std_blue = np.std(blue_values)
        results['B'] = {
            'mean': avg_blue,
            'std': std_blue,
            'snr': avg_blue / std_blue if std_blue > 0 else 0
        }
    
    return results


def example_roi_analysis(image_path):
    """
    Example showing ROI-based SNR analysis using the new raw_loader.
    
    This replaces the scattered loading code in roi.py with the centralized
    load_raw_image function.
    """
    print(f"Loading image: {image_path}")
    
    # Load the image using the new raw_loader
    result = load_raw_image(image_path)
    
    # Handle different return types
    if isinstance(result, tuple):
        # CR2 file - we have raw image and metadata
        raw_image, metadata = result
        bayer_pattern = metadata['raw_pattern']
        print(f"Loaded CR2 file: {raw_image.shape}, pattern: {bayer_pattern}")
    else:
        # Standard image file
        raw_image = result
        # Assume RGGB pattern for demonstration
        bayer_pattern = np.array([[0, 1], [1, 2]])
        print(f"Loaded image: {raw_image.shape}")
    
    # Display the image
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(raw_image, cmap='gray')
    ax.set_title(f'Raw Image: {image_path}')
    
    # Store ROI
    roi_data = {'roi': None}
    
    def onselect(eclick, erelease):
        x1, y1 = int(eclick.xdata), int(eclick.ydata)
        x2, y2 = int(erelease.xdata), int(erelease.ydata)
        roi_data['roi'] = (x1, y1, x2, y2)
        
        print(f"\nROI selected: ({x1}, {y1}) to ({x2}, {y2})")
        print(f"ROI size: {x2-x1} x {y2-y1} pixels")
        
        # Calculate SNR
        results = calculate_roi_snr(raw_image, bayer_pattern, roi_data['roi'])
        
        print("\n" + "="*50)
        print("SNR Analysis Results:")
        print("="*50)
        for channel, stats in results.items():
            print(f"\n{channel} Channel:")
            print(f"  Mean:  {stats['mean']:.2f}")
            print(f"  Std:   {stats['std']:.2f}")
            print(f"  SNR:   {stats['snr']:.2f} ({20*np.log10(stats['snr']):.2f} dB)")
    
    # Create ROI selector
    toggle_selector = RectangleSelector(
        ax, onselect, useblit=True,
        button=[1], minspanx=5, minspany=5,
        spancoords='pixels', interactive=True
    )
    
    plt.show()


def example_full_image_statistics(image_path):
    """
    Calculate statistics for the entire image using raw_loader.
    """
    print(f"\nCalculating statistics for: {image_path}")
    
    # Load the image
    result = load_raw_image(image_path)
    
    if isinstance(result, tuple):
        raw_image, metadata = result
        bayer_pattern = metadata['raw_pattern']
        
        # Extract channels
        channels = get_bayer_channels(raw_image, bayer_pattern)
        
        print("\nFull Image Statistics:")
        print("="*50)
        for channel_name, channel_data in channels.items():
            mean_val = channel_data.mean()
            std_val = channel_data.std()
            snr = mean_val / std_val if std_val > 0 else 0
            
            print(f"\n{channel_name} Channel:")
            print(f"  Shape: {channel_data.shape}")
            print(f"  Mean:  {mean_val:.2f}")
            print(f"  Std:   {std_val:.2f}")
            print(f"  Min:   {channel_data.min()}")
            print(f"  Max:   {channel_data.max()}")
            print(f"  SNR:   {snr:.2f} ({20*np.log10(snr):.2f} dB)")
    else:
        # Standard image
        print(f"\nImage shape: {result.shape}")
        print(f"Data type: {result.dtype}")
        print(f"Value range: [{result.min()}, {result.max()}]")
        print(f"Mean: {result.mean():.2f}")
        print(f"Std: {result.std():.2f}")


if __name__ == "__main__":
    import sys
    
    # Example 1: Full image statistics
    print("="*60)
    print("Example 1: Full Image Statistics")
    print("="*60)
    
    # Check which image files are available
    import os
    
    cr2_files = [f for f in os.listdir('.') if f.endswith('.cr2')]
    png_files = [f for f in os.listdir('.') if f.endswith('.png')]
    
    if cr2_files:
        example_full_image_statistics(cr2_files[0])
    elif png_files:
        example_full_image_statistics(png_files[0])
    else:
        print("No suitable image files found in current directory")
    
    # Example 2: Interactive ROI analysis
    if len(sys.argv) > 1:
        print("\n" + "="*60)
        print("Example 2: Interactive ROI Analysis")
        print("="*60)
        print("Select an ROI by clicking and dragging on the image")
        example_roi_analysis(sys.argv[1])
    else:
        print("\nTo run interactive ROI analysis:")
        print("  python example_usage.py <image_path>")
        print("  Example: python example_usage.py template1.png")
