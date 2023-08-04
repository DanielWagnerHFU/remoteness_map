import requests
import json

def get_elevation_for_locations(locations):
    base_url = "https://api.open-elevation.com/api/v1/lookup"
    coordinates = "|".join([f"{lat},{lon}" for lat, lon in locations])
    url = f"{base_url}?locations={coordinates}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Save the response data to a JSON file
        with open("elevation_data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        print("Elevation data saved to 'elevation_data.json'")
    else:
        print("Error:", response.status_code)

if __name__ == "__main__":
    locations = [
        (41.161758, -8.583933),
        (40.712776, -74.005974),
        (34.052235, -118.243683)
    ]

    get_elevation_for_locations(locations)
