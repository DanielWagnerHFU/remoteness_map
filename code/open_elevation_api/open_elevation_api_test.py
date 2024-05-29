import requests

def get_elevation(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    response = requests.get(url)
    data = response.json()
    return data["results"][0]["elevation"]

print(get_elevation(48.27364495495722, 8.851803750325754))