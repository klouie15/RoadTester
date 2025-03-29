import requests


BASE_URL = "http://router.project-osrm.org/"


def generate_route(start_coordinates: list,
                   school_coordinates: list,
                   playground_coordinates: list):
    service = "route"
    version = "v1"
    profile = "driving"

    start_coordinates.reverse()
    start = ",".join([str(c) for c in start_coordinates])

    url = f"{BASE_URL}/{service}/{version}/{profile}/{start};{start}"

    response = requests.get(url)
    print(response.json())

    # TODO: Implement school/playground within a 2km radius
