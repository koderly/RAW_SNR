import cv2
import numpy as np
import matplotlib.pyplot as plt

def identify_gray_squares_with_inner_region(image_path, buffer=5):
    # Load the raw Bayer image
    raw_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if raw_image is None:
        print("Error: Image not found or invalid format.")
        return

    # Get image dimensions
    h, w = raw_image.shape

    # Extract Bayer channels
    R = raw_image[0:h:2, 0:w:2]
    G1 = raw_image[0:h:2, 1:w:2]
    G2 = raw_image[1:h:2, 0:w:2]
    B = raw_image[1:h:2, 1:w:2]

    # Approximate luminance for gray detection using Bayer pattern
    luminance = (R.astype(float) + G1.astype(float) + G2.astype(float) + B.astype(float)) / 4

    # Normalize luminance for gray square detection
    luminance = cv2.normalize(luminance, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Threshold to find gray squares
    _, binary = cv2.threshold(luminance, 60, 255, cv2.THRESH_BINARY_INV)

    # Find contours to identify square-like shapes
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    highlighted_image = cv2.cvtColor(raw_image, cv2.COLOR_BAYER_RG2RGB)

    gray_square_averages = []
    for contour in contours:
        # Approximate shape
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the contour is a square
        if len(approx) == 4 and cv2.isContourConvex(approx):
            x, y, w, h = cv2.boundingRect(approx)

            # Define inner rectangle with buffer
            x_inner = x + buffer
            y_inner = y + buffer
            w_inner = w - 2 * buffer
            h_inner = h - 2 * buffer

            if w_inner > 0 and h_inner > 0:
                # Extract inner square region
                region_R = R[y_inner // 2:(y_inner + h_inner) // 2, x_inner // 2:(x_inner + w_inner) // 2]
                region_G1 = G1[y_inner // 2:(y_inner + h_inner) // 2, x_inner // 2:(x_inner + w_inner) // 2]
                region_G2 = G2[y_inner // 2:(y_inner + h_inner) // 2, x_inner // 2:(x_inner + w_inner) // 2]
                region_B = B[y_inner // 2:(y_inner + h_inner) // 2, x_inner // 2:(x_inner + w_inner) // 2]

                # Compute average signal for each channel
                avg_R = np.mean(region_R)
                avg_G1 = np.mean(region_G1)
                avg_G2 = np.mean(region_G2)
                avg_B = np.mean(region_B)

                gray_square_averages.append(((x_inner, y_inner, w_inner, h_inner), (avg_R, avg_G1, avg_G2, avg_B)))

                # Highlight outer square in green
                cv2.rectangle(highlighted_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Highlight inner square in blue
                cv2.rectangle(highlighted_image, (x_inner, y_inner), (x_inner + w_inner, y_inner + h_inner), (255, 0, 0), 2)

    # Display highlighted image
    plt.figure(figsize=(10, 10))
    plt.title("Highlighted Gray Squares with Inner Rectangles")
    plt.imshow(cv2.cvtColor(highlighted_image, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()

    # Print and return averages
    for idx, ((x_inner, y_inner, w_inner, h_inner), (avg_R, avg_G1, avg_G2, avg_B)) in enumerate(gray_square_averages):
        print(f"Square {idx + 1}:")
        print(f"  Inner Rectangle -> x: {x_inner}, y: {y_inner}, w: {w_inner}, h: {h_inner}")
        print(f"  Averages -> R: {avg_R:.2f}, G1: {avg_G1:.2f}, G2: {avg_G2:.2f}, B: {avg_B:.2f}\n")

    return gray_square_averages

# Provide the path to the raw Bayer image
image_path = "image.png"
buffer = 5  # Default buffer size in pixels
gray_squares = identify_gray_squares_with_inner_region(image_path, buffer)