# GitHub Copilot Instructions for RAW_SNR

## Project Overview

RAW_SNR is a Python-based repository for analyzing Signal-to-Noise Ratio (SNR) in RAW image data, particularly from Bayer pattern sensors. The project includes tools for:

- RAW image processing and analysis
- Bayer pattern color channel extraction
- SNR calculation for different color channels
- Region of Interest (ROI) selection and analysis
- Color chart grid detection and analysis
- Photon shot noise visualization

## Technology Stack

### Primary Languages & Tools
- **Python**: Primary language for image processing scripts
- **Jupyter Notebooks**: Used for interactive analysis and visualization
- **JavaScript/React**: Used in some visualization components (e.g., photon_shot_noise.py)

### Key Dependencies
- `rawpy`: RAW image file reading
- `numpy`: Numerical computations
- `matplotlib`: Plotting and visualization
- `opencv-python` (cv2): Image processing and GUI components
- `scipy`: Statistical analysis (potential dependency)

## Repository Structure

```
.
├── photon_shot_noise.py       # Poisson distribution visualization (React component)
├── roi.py                      # ROI selection tool for Bayer pattern analysis
├── color_chart_grid_gui.py    # Interactive color chart grid analyzer
├── color_chart_grid_gui2.py   # Alternative grid analyzer implementation
├── *.ipynb                     # Jupyter notebooks for analysis
├── *.cr2, *.png, *.raw        # Sample image files for testing
├── HoloSeg/                    # Subdirectory (currently empty)
└── yolov5/                     # Subdirectory (currently empty)
```

## Development Guidelines

### Code Style
- Follow PEP 8 style guidelines for Python code
- Use descriptive variable names (e.g., `avg_red`, `std_green1`)
- Include docstrings for functions, especially those with complex logic
- Maintain consistent indentation (4 spaces)

### Working with Images
- RAW images use Bayer pattern format with the pattern: `[[0, 1], [1, 2]]` where:
  - 0 = Red
  - 1 = Green (G1 or G2 depending on position)
  - 2 = Blue
- Image coordinates follow standard convention: (x, y) with origin at top-left
- When calculating statistics, separate each Bayer color channel

### Mathematical Conventions
- SNR is calculated as: `mean / standard_deviation` (linear scale)
- Use numpy for statistical calculations: `np.mean()`, `np.std()`
- Handle edge cases where standard deviation might be zero

### Interactive Tools
- GUI tools use matplotlib widgets or OpenCV (`cv2`) for interaction
- ROI selection uses `RectangleSelector` from matplotlib
- Grid-based tools use mouse callbacks for corner dragging

### Jupyter Notebooks
- Notebooks are used for exploratory analysis
- Keep cell outputs for reference unless they contain large binary data
- Use markdown cells to document analysis steps

## Common Tasks

### Adding New Image Processing Functions
1. Follow the pattern in `roi.py` for Bayer pattern analysis
2. Separate concerns: image loading, processing, and visualization
3. Handle both RAW and processed image formats
4. Include error handling for invalid image paths or formats

### Creating Interactive Tools
1. Base interactive tools on the patterns in `color_chart_grid_gui.py`
2. Provide visual feedback (e.g., colored overlays, text labels)
3. Include keyboard shortcuts for common actions (e.g., 'q' to quit)
4. Print results to console for record-keeping

### Statistical Analysis
1. Calculate statistics per color channel for Bayer pattern images
2. Report both mean and standard deviation
3. Include SNR calculations when appropriate
4. Handle cases with zero or near-zero denominators

## Testing

- No formal test framework is currently in place
- Test new features manually with the sample images in the repository
- Verify output values against expected ranges for image data (e.g., 0-255 or 0-1.0)
- Use the provided sample files (.cr2, .png, .raw) for testing

## Dependencies Installation

To set up the development environment:

```bash
pip install rawpy numpy matplotlib opencv-python jupyter
```

For React components (if needed):
```bash
npm install react recharts
```

## Important Notes

- **File Paths**: Some scripts contain hardcoded absolute paths (e.g., `/path/to/user/directory/...` or `~/...`). Use relative paths or make paths configurable when modifying these files.
- **Large Files**: The repository contains large RAW image files (.cr2, .raw). Be mindful of repository size when adding new sample images.
- **Notebooks**: Jupyter notebook files (.ipynb) are version controlled. Clear outputs before committing if they're large.

## Best Practices for Copilot

- When modifying image processing code, preserve the Bayer pattern logic
- Maintain backward compatibility with existing scripts
- Add comments for complex mathematical operations or image processing steps
- Test with multiple sample images to ensure robustness
- Keep dependencies minimal and well-documented
