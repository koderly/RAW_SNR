import cv2
import numpy as np

# Load the image
image_path = "image.png"  # Replace with your image path
image = cv2.imread(image_path)

# Get image dimensions
rows, cols, _ = image.shape

# Define grid dimensions
grid_width = cols // 2
grid_height = rows // 2
grid_top_left = (cols // 4, rows // 4)  # Top-left corner to center the grid
buffer_pixels = 30 # pixels to put the smaller recrangle inside the outter

# Define the initial grid points (centered, scaled)
grid_corners = np.array([
    [grid_top_left[0], grid_top_left[1]],                          # Top-left
    [grid_top_left[0] + grid_width, grid_top_left[1]],             # Top-right
    [grid_top_left[0] + grid_width, grid_top_left[1] + grid_height],  # Bottom-right
    [grid_top_left[0], grid_top_left[1] + grid_height]             # Bottom-left
], dtype=np.int32)

# State variables for dragging
selected_corner = -1
dragging = False

# Button position (at the bottom of the image)
button_rect = [20, rows - 100, 400, rows - 20]  # (x1, y1, x2, y2)

def draw_grid_with_inner_rectangles(img, corners, averages=None, buffer):
    """Draw the grid, button, and optionally inner rectangles with average text overlay."""
    grid_img = img.copy()
    
    # Create intermediate points for a 1-row, 6-column grid
    top = np.linspace(corners[0], corners[1], 7, dtype=np.int32)
    bottom = np.linspace(corners[3], corners[2], 7, dtype=np.int32)
    
    # Draw vertical grid lines
    for i in range(7):
        cv2.line(grid_img, tuple(top[i]), tuple(bottom[i]), (0, 255, 0), 2)
    
    # Draw top and bottom horizontal lines
    cv2.line(grid_img, tuple(corners[0]), tuple(corners[1]), (0, 255, 0), 2)
    cv2.line(grid_img, tuple(corners[3]), tuple(corners[2]), (0, 255, 0), 2)
    
    # Draw the corners as draggable points
    for corner in corners:
        cv2.circle(grid_img, tuple(corner), 10, (0, 0, 255), -1)
    
    # Draw the button
    cv2.rectangle(grid_img, (button_rect[0], button_rect[1]), (button_rect[2], button_rect[3]), (255, 0, 0), -1)
    cv2.putText(grid_img, "Calc Avg", (button_rect[0] + 20, button_rect[1] + 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    
    # Draw inner rectangles (buffered) and overlay averages
    if averages is not None:
        for i, avg in enumerate(averages):
            # Calculate buffered rectangle corners
            rect_top_left = top[i]
            rect_bottom_right = bottom[i + 1]
            rect_bottom_left = bottom[i]
            rect_top_right = top[i + 1]
            
            rect_top_left = (rect_top_left[0] + buffer, rect_top_left[1] + buffer)
            rect_bottom_right = (rect_bottom_right[0] - buffer, rect_bottom_right[1] - buffer)
            rect_bottom_left = (rect_bottom_left[0] + buffer, rect_bottom_left[1] - buffer)
            rect_top_right = (rect_top_right[0] - buffer, rect_top_right[1] + buffer)
            
            # Draw the inner rectangle
            pts = np.array([rect_top_left, rect_top_right, rect_bottom_right, rect_bottom_left], np.int32)
            cv2.polylines(grid_img, [pts], isClosed=True, color=(255, 0, 0), thickness=2)
            
            # Calculate center of the inner rectangle for text
            center = ((rect_top_left[0] + rect_bottom_right[0]) // 2, 
                      (rect_top_left[1] + rect_bottom_right[1]) // 2)
            
            # Display the RGB values
            r_text = f"R: {avg[2]:.2f}"  # BGR format
            g_text = f"G: {avg[1]:.2f}"
            b_text = f"B: {avg[0]:.2f}"
            
            cv2.putText(grid_img, r_text, (center[0] - 50, center[1] - 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
            cv2.putText(grid_img, g_text, (center[0] - 50, center[1]), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
            cv2.putText(grid_img, b_text, (center[0] - 50, center[1] + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
    
    return grid_img
def calculate_averages_with_buffer(corners, buffer):
    """Calculate average pixel value for each rectangle in the grid, considering an inner rectangle with a buffer."""
    averages = []
    top = np.linspace(corners[0], corners[1], 7, dtype=np.int32)
    bottom = np.linspace(corners[3], corners[2], 7, dtype=np.int32)
    
    for i in range(6):
        # Rectangle corners
        rect_top_left = top[i]
        rect_bottom_right = bottom[i + 1]
        rect_bottom_left = bottom[i]
        rect_top_right = top[i + 1]
        
        # Shrink rectangle inward by buffer pixels
        rect_top_left = [rect_top_left[0] + buffer, rect_top_left[1] + buffer]
        rect_bottom_right = [rect_bottom_right[0] - buffer, rect_bottom_right[1] - buffer]
        rect_bottom_left = [rect_bottom_left[0] + buffer, rect_bottom_left[1] - buffer]
        rect_top_right = [rect_top_right[0] - buffer, rect_top_right[1] + buffer]
        
        # Create a mask for the smaller inner rectangle
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        pts = np.array([rect_top_left, rect_top_right, rect_bottom_right, rect_bottom_left], np.int32)
        cv2.fillPoly(mask, [pts], 255)
        
        # Calculate mean pixel value for the inner rectangle
        mean_val = cv2.mean(image, mask=mask)[:3]  # Only consider BGR values
        averages.append(mean_val)
    
    return averages
def mouse_callback(event, x, y, flags, param):
    """Mouse callback function to drag corners or handle button clicks."""
    global selected_corner, dragging

    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if clicking near any corner
        for i, corner in enumerate(grid_corners):
            if np.linalg.norm(np.array([x, y]) - corner) < 10:
                selected_corner = i
                dragging = True
                break

        # Check if the button is clicked
        if button_rect[0] <= x <= button_rect[2] and button_rect[1] <= y <= button_rect[3]:
            averages = calculate_averages_with_buffer(grid_corners)
            print("Average pixel values of each rectangle:")
            for i, avg in enumerate(averages):
                print(f"Rectangle {i + 1}: {avg}")
    
    elif event == cv2.EVENT_MOUSEMOVE and dragging:
        # Update the position of the selected corner
        if selected_corner != -1:
            grid_corners[selected_corner] = [x, y]
    
    elif event == cv2.EVENT_LBUTTONUP:
        # Release the drag
        dragging = False
        selected_corner = -1

# Set up the window and callback
cv2.namedWindow("Interactive Grid")
cv2.setMouseCallback("Interactive Grid", mouse_callback)

while True:
    # Calculate averages (update this for live display)
    averages = calculate_averages_with_buffer(grid_corners)
    
    # Draw the grid and button on the image, and overlay average values
    grid_img = draw_grid_with_inner_rectangles(image, grid_corners, averages, buffer_pixels)
    
    # Display the image
    cv2.imshow("Interactive Grid", grid_img)
    
    # Break on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()