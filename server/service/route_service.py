import requests
import overpy
import random
import math


MIN_DURATION = 10
MAX_DURATION = 15

HTTP_STATUS_OK = 200

KM_TO_DEGREES_CONVERSION = 111
M_TO_KM_CONVERSION = 1000
SEC_TO_MIN_CONVERSION = 60

NUMBER_OF_WAYPOINTS = 5
RADIUS_M = 1500

OSRM_BASE_URL = "http://router.project-osrm.org/route/v1/driving"
OSRM_NEAREST_URL = "http://router.project-osrm.org/nearest/v1/driving"


def generate_route(start_coordinates: tuple[float, float]) -> str | None:
    start = str(start_coordinates[1]) + "," + str(start_coordinates[0])

    while True:
        slow_zones = retrieve_slow_zones(start_coordinates, RADIUS_M)

        slow_zone_coordinates = list(random.choice(slow_zones))
        if not slow_zone_coordinates:
            print("Nearby school/playground zone not found.")
            return None

        slow_zone_coordinates.reverse()
        slow_zone = ",".join([str(c) for c in slow_zone_coordinates])

        waypoint_coordinates = generate_random_waypoints(start_coordinates, RADIUS_M)
        waypoints = ";".join(f"{lon},{lat}" for lat, lon in waypoint_coordinates)

        coordinate_str = f"{start};{slow_zone};{waypoints};{start}"
        url = f"{OSRM_BASE_URL}/{coordinate_str}?overview=full&continue_straight=true"
        print(url)

        response = requests.get(url)
        if response.status_code != HTTP_STATUS_OK:
            print(response.json())
            continue

        route_data = response.json()
        if is_valid_route(route_data):
            return route_data


def generate_random_waypoints(
        start_coordinates: tuple[float, float],
        radius_m: int
) -> list[tuple[float, float]]:

    waypoints = []
    radius_km = radius_m / M_TO_KM_CONVERSION

    latitude = start_coordinates[0]
    longitude = start_coordinates[1]

    for i in range(NUMBER_OF_WAYPOINTS):
        latitude_offset = random.uniform(-radius_km / KM_TO_DEGREES_CONVERSION, radius_km / KM_TO_DEGREES_CONVERSION)
        longitude_offset = random.uniform(
            -radius_km / (KM_TO_DEGREES_CONVERSION * abs(math.cos(math.radians(latitude)))),
            radius_km / (KM_TO_DEGREES_CONVERSION * abs(math.cos(math.radians(latitude))))
        )

        random_latitude = latitude + latitude_offset
        random_longitude = longitude + longitude_offset

        snapped_point = snap_to_road((random_latitude, random_longitude))
        if snapped_point:
            waypoints.append(snapped_point)
            break

    return waypoints


def snap_to_road(coordinates: tuple[float, float]):
    url = f"{OSRM_NEAREST_URL}/{coordinates[1]},{coordinates[0]}"
    response = requests.get(url)

    if response.status_code == HTTP_STATUS_OK:
        data = response.json()

        if "waypoints" in data and len(data["waypoints"]) > 0:
            snapped = data["waypoints"][0]["location"]
            return snapped[1], snapped[0]

    return None


def is_valid_route(route_data):
    duration_minutes = route_data["routes"][0]["duration"] / SEC_TO_MIN_CONVERSION
    return MIN_DURATION <= duration_minutes <= MAX_DURATION


def retrieve_slow_zones(
        location_coordinates: tuple[float, float],
        radius_m: int
) -> list[tuple[float, float]]:

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
