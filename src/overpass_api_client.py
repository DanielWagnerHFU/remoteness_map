import requests
from requests import Response

class OverpassAPIClient:
    def __init__(self, endpoint: str ="http://overpass-api.de/api/interpreter"):
        self.endpoint: str = endpoint

    def execute_query(self, overpass_query: str) -> str:
        payload: dict[str, str] = {"data": overpass_query}
        headers: dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"}
        response: Response = requests.post(self.endpoint, data=payload, headers=headers)
        response.raise_for_status()
        return response.text

if __name__ == "__main__":
    overpass_client = OverpassAPIClient()
    overpass_query = """
        [out:json];
        ( way(51.477,-0.001,51.478,0.001)[name="Blackheath Avenue"];
        node(w);
        relation(51.477,-0.001,51.478,0.001); );
        convert item ::=::,::geom=geom(),_osm_type=type();
        out geom;
        """
    result = overpass_client.execute_query(overpass_query)
    print(result)