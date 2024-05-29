import requests

url = "https://api.open-elevation.com/api/v1/lookup"
payload = {
    "locations": [
        {"latitude": 48.278816171713515, "longitude": 8.851363719986814},
        {"latitude": 48.05241190997449, "longitude": 8.205293403711481}
    ]
}
response = requests.post(url, json=payload)
if response.status_code == 200:
    elevation_data = response.json()
    print("Elevation data:", elevation_data)
else:
    print("Error:", response.status_code)