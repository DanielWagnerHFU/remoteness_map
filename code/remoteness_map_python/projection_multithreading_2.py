import requests
import multiprocessing
import cv2
import numpy as np
from pyproj import Transformer
import time

def main():
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    time.sleep(10)
    test_01(transformer, pool)
    test_01(transformer, pool)
    test_01(transformer, pool)
    test_02(transformer, pool)

def test_01(transformer, pool):
    lat_min, long_min = 48.195651758475506, 8.7195352489608
    lat_max, long_max = 48.33115535177915, 8.983512222877913
    x_min, y_min = transformer.transform(long_min, lat_min)
    x_max, y_max = transformer.transform(long_max, lat_max)
    map_width = 1500
    scale_factor = map_width / (x_max- x_min)
    map_height = scale_factor * (y_max - y_min)
    geo_json = get_geojson(lat_min, long_min, lat_max, long_max)
    polylines = generate_projeted_geometry(geo_json, x_min, y_max, scale_factor, transformer, pool)
    map_matrix = generate_image_from_geometry(map_width, map_height, polylines)
    cv2.imshow('Map', map_matrix)
    cv2.waitKey(2)
    cv2.destroyAllWindows()

def test_02(transformer, pool):
    lat_min, long_min = 48.65559785066402, 8.923875599125946
    lat_max, long_max = 48.969628788293114, 9.5281326879464
    x_min, y_min = transformer.transform(long_min, lat_min)
    x_max, y_max = transformer.transform(long_max, lat_max)
    map_width = 1500
    scale_factor = map_width / (x_max- x_min)
    map_height = scale_factor * (y_max - y_min)
    geo_json = get_geojson(lat_min, long_min, lat_max, long_max)
    polylines = generate_projeted_geometry(geo_json, x_min, y_max, scale_factor, transformer, pool)
    map_matrix = generate_image_from_geometry(map_width, map_height, polylines)
    cv2.imshow('Map', map_matrix)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def generate_image_from_geometry(width, height, polylines):
    map_matrix = np.zeros((int(height), int(width)), dtype=np.uint8)
    for polyline in polylines:
        cv2.polylines(map_matrix, [np.array(polyline)], isClosed=False, color=(255), thickness=1)
    return map_matrix

def generate_projeted_geometry(geo_json, x_min, y_max, scale_factor, transformer, pool):
    st = time.time()
    chunk_size = len(geo_json['elements']) // pool._processes
    element_chunks = [geo_json['elements'][i:i+chunk_size] for i in range(0, len(geo_json['elements']), chunk_size)]
    polylines_chunks = pool.starmap(project_elements, [(element_chunk, x_min, y_max, scale_factor, transformer) for element_chunk in element_chunks])
    polylines =  [polyline for polyline_chunk in polylines_chunks for polyline in polyline_chunk]
    t = time.time()- st
    print(f"Elapsed time: {t:.6f} seconds")
    return polylines

def project_elements(element_chunk, x_min, y_max, scale_factor, transformer):
    polylines = []
    for element in element_chunk:
        polyline = []
        geometry = element['geometry']
        for point in geometry:
            x, y = transformer.transform(point['lon'], point['lat'])
            x_ , y_ = x - x_min, y_max - y
            x__, y__ = scale_factor * x_, scale_factor * y_
            polyline.append((int(x__), int(y__)))
        polylines.append(polyline)
    return polylines

def get_geojson(lat_min, long_min, lat_max, long_max):
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = """
    [out:json];
    way({},{},{},{})[highway];
    out geom;
    """
    formatted_query = query.format(lat_min, long_min, lat_max, long_max)
    response = requests.get(overpass_url, params={'data': formatted_query})
    return response.json()

if __name__ == '__main__':
    main()
