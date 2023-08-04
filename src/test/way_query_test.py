import requests
import json

def overpass_query_to_json(query):
    overpass_url = "https://overpass-api.de/api/interpreter"
    response = requests.get(overpass_url, params={"data": query})
    if response.status_code == 200:
        try:
            data = response.json()
            with open("overpass_data.json", "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            print("Data saved to 'overpass_data.json'")
        except json.JSONDecodeError as e:
            print("Failed to parse JSON data:", e)
    else:
        print("Error:", response.status_code)

if __name__ == "__main__":
    query = "[out:json];way(around:100, 48.27859652235137, 8.848723012168243);out geom;"
    overpass_query_to_json(query)
