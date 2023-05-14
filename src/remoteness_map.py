from shapely.geometry import Point
from shapely.ops import nearest_points
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, LineString
from scipy.spatial import cKDTree
from skimage import draw

class RemotenessMap:
    def __init__(self, gdf, width = 200):
        self.gdf = gdf
        self.width = width
    
    def generate_distance_plot(self, resolution=0.001):
        bounds = self.gdf.total_bounds
        minx, miny, maxx, maxy = bounds
        x = np.arange(minx, maxx, resolution)
        y = np.arange(miny, maxy, resolution)
        xx, yy = np.meshgrid(x, y)

        distances = np.zeros_like(xx)
        iterations = xx.shape[0] * xx.shape[1]
        for i in range(xx.shape[0]):
            for j in range(xx.shape[1]):
                print(iterations, i*xx.shape[1] + j)
                point = Point(xx[i, j], yy[i, j])
                nearest_line = nearest_points(point, self.gdf.unary_union)[1]
                distances[i, j] = point.distance(nearest_line)

        plt.imshow(distances, cmap='ocean_r', extent=[minx, maxx, miny, maxy], origin='lower')
        plt.colorbar(label='Distance (meters)')
        self.gdf.plot(ax=plt.gca(), color='black', linewidth=1)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Distance from Roads')
        plt.show()
    
    def generate_distance_matrix(self):
        bounds = self.gdf.total_bounds
        minx, miny, maxx, maxy = bounds
        aspect_ratio = (maxy - miny) / (maxx - minx)
        height = int(self.width * aspect_ratio)
        x = np.linspace(minx, maxx, self.width)
        y = np.linspace(miny, maxy, height)
        xx, yy = np.meshgrid(x, y)
        distances = np.zeros((height, self.width), dtype=np.float32)
        for i in range(height):
            for j in range(self.width):
                point = Point(xx[i, j], yy[i, j])
                min_distance = float('inf')
                for geometry in self.gdf.geometry:
                    distance = point.distance(geometry)
                    if distance < min_distance:
                        min_distance = distance
                distances[i, j] = min_distance
        return distances
    
    def generate_distance_matrix_efficient(self):
        bounds = self.gdf.total_bounds
        minx, miny, maxx, maxy = bounds
        aspect_ratio = (maxy - miny) / (maxx - minx)
        height = int(self.width * aspect_ratio)
        x = np.linspace(minx, maxx, self.width)
        y = np.linspace(miny, maxy, height)
        xx, yy = np.meshgrid(x, y)
        distances = np.zeros((height, self.width), dtype=np.float32)
        vertices = []
        line_indices = []
        for i, geom in enumerate(self.gdf.geometry):
            vertices.extend(np.array(geom.xy).T.tolist())
            line_indices.extend([i] * len(geom.coords))
        vertices = np.array(vertices)
        line_indices = np.array(line_indices)
        kdtree = cKDTree(vertices)
        for i in range(height):
            for j in range(self.width):
                point = Point(xx[i, j], yy[i, j])
                _, idx = kdtree.query(np.array(point.coords)[0])
                nearest_line_index = line_indices[idx]
                nearest_line = self.gdf.geometry.iloc[nearest_line_index]
                min_distance = point.distance(nearest_line)
                distances[i, j] = min_distance
        return distances
    
    def generate_road_matrix(self):
        bounds = self.gdf.total_bounds
        minx, miny, maxx, maxy = bounds
        aspect_ratio = (maxy - miny) / (maxx - minx)
        height = int(self.width * aspect_ratio)
        pixel_width = (maxx - minx) / self.width
        pixel_height = (maxy - miny) / height
        road_matrix = np.zeros((height, self.width), dtype=np.uint8)
        for geometry in self.gdf.geometry:
            pixels = []
            for x, y in geometry.coords:
                pixel_x = int((x - minx) / pixel_width)
                pixel_y = int((y - miny) / pixel_height)
                pixels.append((pixel_x, pixel_y))
            for i in range(len(pixels) - 1):
                x0, y0 = pixels[i]
                x1, y1 = pixels[i + 1]
                if 0 <= x0 < self.width and 0 <= y0 < height and 0 <= x1 < self.width and 0 <= y1 < height:
                    rr, cc = draw.line(y0, x0, y1, x1)
                    road_matrix[rr, cc] = 1
        return road_matrix
    

