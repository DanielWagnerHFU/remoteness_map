import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.ndimage import distance_transform_edt
import cv2
import random

def create_binary_map(polylines, width, height):
    # Create an empty map with zeros
    binary_map = np.zeros((height, width), dtype=np.uint8)

    for line in polylines:
        # Convert the coordinates to integer values
        line = np.round(line).astype(int)

        # Draw polylines on the binary map
        cv2.polylines(binary_map, [line], isClosed=False, color=255, thickness=1)

    return binary_map


def plot_bitmap(bitmap):
    plt.imshow(bitmap, cmap='gray', interpolation='nearest')
    plt.title('Road Network')
    plt.show()

def generate_random_polyline(n):
    n = max(2, n)
    polyline = [(random.randint(0, 2000), random.randint(0, 2000)) for _ in range(n)]
    return polyline

def generate_random_polylines(m):
    polylines = [generate_random_polyline(random.randint(2, random.randint(2, 50))) for _ in range(m)]
    return polylines

def crop_image(image, crop_percent):
    # Check if the crop_percent is within the valid range (0 to 100)
    if crop_percent < 0 or crop_percent >= 50:
        raise ValueError("Invalid crop percentage. It should be in the range [0, 50).")

    # Calculate the number of pixels to crop from each side
    height, width = image.shape
    crop_pixels = int(min(height, width) * crop_percent / 100)

    # Crop the image
    cropped_image = image[crop_pixels:height-crop_pixels, crop_pixels:width-crop_pixels]
    #normalize values
    min_val = np.min(cropped_image)
    max_val = np.max(cropped_image)
    normalized_image = (cropped_image - min_val) / (max_val - min_val)
    return normalized_image

# Example road network
roads = generate_random_polylines(10)
# Set the width and height of the bitmap
width, height = 2000, 2000
road_bitmap = create_binary_map(roads, width, height)
#plot_bitmap(road_bitmap)
# edt with scipy
#edt_result = distance_transform_edt(road_bitmap != 255)

# edt with scipy
road_bitmap = road_bitmap ^ 255 # switch 0 and 255 with xor
edt_result = cv2.distanceTransform(road_bitmap, cv2.DIST_L2, 3)
print(edt_result.dtype)
# plot
edt_result = crop_image(edt_result, 25)
#plot_bitmap(edt_result)
plt.imshow(edt_result, cmap='viridis')
plt.colorbar()  # Add a colorbar to show the mapping of values to colors
plt.title('Cropped and Normalized Image')
plt.show()




