import geopandas as gpd
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import numpy as np

class RemotenessMap:
    def __init__(self, lat, long, radius, data):
        self.lat = lat
        self.long = long
        self.radius = radius
        self.gdf = self.generate_geodataframe(data)

    def generate_geodataframe(self, data):
        features = []
        for element in data["elements"]:
            if element["type"] == "way" and "geometry" in element:
                coords = [(point["lon"], point["lat"]) for point in element["geometry"]]
                line = LineString(coords)
                feature = {
                    "geometry": line,
                    "properties": element["tags"]
                }
                features.append(feature)
        gdf = gpd.GeoDataFrame.from_features(features)

    def calculate_minimum_distance_to_road(self,point):
        query_point = Point(point[1], point[0])
        distances = self.gdf.geometry.apply(lambda line: geodesic(query_point.coords[0], line.centroid.coords[0]).meters)
        min_distance = distances.min()
        return min_distance
    
    def generate_distance_plot(gdf, resolution=0.001):
        bounds = gdf.total_bounds
        minx, miny, maxx, maxy = bounds
        x = np.arange(minx, maxx, resolution)
        y = np.arange(miny, maxy, resolution)
        xx, yy = np.meshgrid(x, y)

        distances = np.zeros_like(xx)
        for i in range(xx.shape[0]):
            for j in range(xx.shape[1]):
                query_point = Point(xx[i, j], yy[i, j])
                nearest_line = nearest_points(query_point, gdf.unary_union)[1]
                distances[i, j] = query_point.distance(nearest_line)

        plt.imshow(distances, cmap='ocean_r', extent=[minx, maxx, miny, maxy], origin='lower')
        plt.colorbar(label='Distance (meters)')
        gdf.plot(ax=plt.gca(), color='black', linewidth=1)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Distance from Roads')
        plt.show()

def test_remoteness_map():
    pass

if __name__ == '__main__':
    test_remoteness_map()
    #pass