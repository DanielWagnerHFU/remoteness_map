import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points
    on the Earth's surface given their latitudes and longitudes.
    """
    R = 6371.0  # Earth radius in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c
    return distance

def generate_grid_points(center_lat, center_lon, grid_size_km, num_points):
    """
    Generate a grid of points around a given center point on Earth.
    """
    points = []
    for x in range(-num_points//2, num_points//2 + 1):
        for y in range(-num_points//2, num_points//2 + 1):
            lat = center_lat + (y * grid_size_km) / 111.0
            lon = center_lon + (x * grid_size_km) / (111.0 * math.cos(math.radians(center_lat)))
            points.append((lat, lon))
    return points

if __name__ == "__main__":
    center_lat = 40.7128  # Latitude of the center point (New York City)
    center_lon = -74.0060  # Longitude of the center point (New York City)
    grid_size_km = 10  # Grid spacing in kilometers
    num_points = 5  # Number of points in each dimension of the grid

    grid_points = generate_grid_points(center_lat, center_lon, grid_size_km, num_points)

    # Extract latitudes and longitudes from the grid_points list
    latitudes = [point[0] for point in grid_points]
    longitudes = [point[1] for point in grid_points]

    # Plot the grid points as a scatter plot
    plt.scatter(longitudes, latitudes, marker='o', color='red')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Grid Points')
    plt.grid(True)
    plt.show()