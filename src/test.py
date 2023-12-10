import cv2
import numpy as np

# Create a 10x10 binary image with one pixel set to foreground
binary_image = np.zeros((11, 11), dtype=np.uint8)
binary_image[0, 5] = 255  # Setting a single pixel to foreground
binary_image[10, 5] = 255 
# Apply distance transform
binary_image = binary_image ^ 255
dist_transform = cv2.distanceTransform(binary_image, cv2.DIST_L2, 0)

# Print the distance transform image
print("Distance Transform:\n", dist_transform)