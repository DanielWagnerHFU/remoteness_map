import pyproj
import multiprocessing
import json

def project_geometry(geometry_chunk, transformer):
    # Project each point in the geometry chunk
    projected_geometry_chunk = []
    for element in geometry_chunk:
        projected_geometry = []
        geometry = element['geometry']
        for point in geometry:
            lon, lat = point['lon'], point['lat']
            projected_lon, projected_lat = transformer.transform(lon, lat)
            projected_geometry.append({'lon': projected_lon, 'lat': projected_lat})
        projected_geometry_chunk.append(projected_geometry)
    return projected_geometry_chunk

def project_json_parallel(json_data):
    # Define transformer from EPSG:4326 to EPSG:3857
    transformer = pyproj.Transformer.from_crs("epsg:4326", "epsg:3857")

    # Split the list of geometries into smaller chunks
    num_processes = multiprocessing.cpu_count()
    chunk_size = len(json_data['elements']) // num_processes
    geometry_chunks = [json_data['elements'][i:i+chunk_size] for i in range(0, len(json_data['elements']), chunk_size)]

    # Create a multiprocessing pool
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Map the project_geometry function to each geometry chunk
        projected_geometries_chunks = pool.starmap(project_geometry, [(chunk, transformer) for chunk in geometry_chunks])

    # Flatten the list of projected geometries chunks
    projected_geometries = [geometry for chunk in projected_geometries_chunks for geometry in chunk]
    return projected_geometries

if __name__ == '__main__':
    # Read input JSON data from file
    input_file = "input_data.json"
    with open(input_file, "r") as f:
        input_json = json.load(f)
        projected_geometries = project_json_parallel(input_json)
        print("Projected Geometries:", projected_geometries)


