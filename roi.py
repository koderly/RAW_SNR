import rawpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector

import matplotlib.image as mpimg

bayer_pattern = np.array([[0, 1], [1, 2]])

im_filename = 'template1.png'# the actual RAW bayer image
#im_filename = '00137_11_06400_0.005_Outdoor.cr2'
#im_filename = '00137_11_12800_0.5_Outdoor.cr2'
#im_filename = '/Users/danijelmaricic/Downloads/Resolution_captures_AR0231_Imatest_2020-09/5lux/cap0041.png'
#im_filename = '/Users/danijelmaricic/Downloads/Resolution_captures_AR0231_Imatest_2020-09/100lux/cap0020.png'
#im_filename = '/Users/danijelmaricic/Downloads/Resolution_captures_AR0231_Imatest_2020-09/1000lux/cap0031.png'

img=mpimg.imread(im_filename)
print(im_filename)


# Load the raw image
# raw = rawpy.imread('/Users/danijelmaricic/my_jupyter_project/template1.png')
# bayer_pattern = raw.raw_pattern
# raw_image = raw.raw_image_visible
raw_image = img

# Display the raw image (as a grayscale image for simplicity)
fig, ax = plt.subplots()
ax.imshow(raw_image, cmap='gray')

# Global variables to store the selected ROI
roi = None

# Define the ROI selection callback functions
def onselect(eclick, erelease):
    global roi
    x1, y1 = int(eclick.xdata), int(eclick.ydata)
    x2, y2 = int(erelease.xdata), int(erelease.ydata)
    roi = (x1, y1, x2, y2)
    print(f"ROI selected: ({x1}, {y1}) to ({x2}, {y2})")

def calculate_average_bayer(roi, raw_image, bayer_pattern):
    x1, y1, x2, y2 = roi
    selected_region = raw_image[y1:y2, x1:x2]

    # Initialize arrays to store pixel values for each Bayer pattern color
    red_values = []
    green1_values = []
    green2_values = []
    blue_values = []

    # Traverse through the selected region and categorize the pixel values based on the Bayer pattern
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
            elif pattern_position == 2:  # Blue
                blue_values.append(selected_region[i, j])

    # Calculate the average values for each color
    avg_red = np.mean(red_values) if red_values else 0
    avg_green1 = np.mean(green1_values) if green1_values else 0
    avg_green2 = np.mean(green2_values) if green2_values else 0
    avg_blue = np.mean(blue_values) if blue_values else 0

    std_red = np.std(red_values) if red_values else 0
    std_green1 = np.std(green1_values) if green1_values else 0
    std_green2 = np.std(green2_values) if green2_values else 0
    std_blue = np.std(blue_values) if blue_values else 0
    return avg_red, avg_green1, avg_green2, avg_blue, std_red, std_green1, std_green2, std_blue

# Create the ROI selector
toggle_selector = RectangleSelector(ax, onselect, useblit=True,
                                    button=[1], minspanx=5, minspany=5,
                                    spancoords='pixels', interactive=True)

plt.show()

# Calculate and print the average Bayer pattern values if an ROI was selected
if roi:
    avg_red, avg_green1, avg_green2, avg_blue, std_red, std_green1, std_green2, std_blue = calculate_average_bayer(roi, raw_image, bayer_pattern)
    print(f"Average Red value in selected ROI: {avg_red}")
    print(f"Average Red value in selected ROI: {avg_red}")
    print(f"Average Green1 value in selected ROI: {avg_green1}")
    print(f"Average Green2 value in selected ROI: {avg_green2}")
    print(f"Average Blue value in selected ROI: {avg_blue}")
    print(f"Std dev Red value in selected ROI: {std_red}")
    print(f"Std dev Green1 value in selected ROI: {std_green1}")
    print(f"Std dev Green2 value in selected ROI: {std_green2}")
    print(f"Std dev Blue value in selected ROI: {std_blue}")
    print('------------------ SNR Lin ----------------------')
    print(f"SNR Red value in selected ROI: {avg_red/std_red}")
    print(f"SNR Green1 value in selected ROI: {avg_green1/std_green1}")
    print(f"SNR Green2 value in selected ROI: {avg_green2/std_green2}")
    print(f"SNR Blue value in selected ROI: {avg_blue/std_blue}")

