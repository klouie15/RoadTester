import requests
import overpy
import random


BASE_URL = "http://router.project-osrm.org/"


def generate_route(start_coordinates: list,
                   slow_zone_coordinates: list):
    service = "route"
    version = "v1"
    profile = "driving"

    start_coordinates.reverse()
    start = ",".join([str(c) for c in start_coordinates])

    slow_zone_coordinates.reverse()
    slow_zone = ",".join([str(c) for c in slow_zone_coordinates])

    url = f"{BASE_URL}/{service}/{version}/{profile}/{start};{slow_zone};{start}"
    print(url)

    response = requests.get(url)
    print(response.json())


def retrieve_slow_zones(location_coordinates: list, radius_m: int) -> list:
    overpass = overpy.Overpass()

    query = f"""
    [out:json];
    (
      node["amenity"="school"](around:{radius_m},{location_coordinates[0]}, {location_coordinates[1]});
      way["amenity"="school"](around:{radius_m}, {location_coordinates[0]}, {location_coordinates[1]});
      node["leisure"="playground"](around:{radius_m}, {location_coordinates[0]}, {location_coordinates[1]});
      way["leisure"="playground"](around:{radius_m}, {location_coordinates[0]}, {location_coordinates[1]});
    );
    out center;
    """

    result = overpass.query(query)
    slow_zones = [(node.lat, node.lon) for node in result.nodes]

    return slow_zones


def compile_route(location_coordinates: list, radius_m: int) -> None:
    slow_zones = retrieve_slow_zones(location_coordinates, radius_m)

    slow_zone_coordinates = list(random.choice(slow_zones))
    if not slow_zone_coordinates:
        print("Nearby school/playground zone not found.")

    generate_route(location_coordinates, slow_zone_coordinates)


compile_route([49.2498109, -123.1675322], 2000)