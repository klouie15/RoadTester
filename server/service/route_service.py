import requests
import overpy
import random


HTTP_STATUS_OK = 200

KM_TO_DEGREES_CONVERSION = 111
M_TO_KM_CONVERSION = 1000

NUMBER_OF_WAYS = 3
RADIUS_M = 1750

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

        return response.json()


def generate_random_waypoints(
    start_coordinates: tuple[float, float],
    radius_m: int
) -> list[tuple[float, float]]:

    overpass = overpy.Overpass()
    lat, lon = start_coordinates

    query = f"""
    [out:json];
    way(around:{radius_m},{lat},{lon})
      ["highway"~"residential|unclassified|tertiary|secondary|primary"]
      ["service"!~"parking_aisle|driveway|parking"];
    out center {NUMBER_OF_WAYS * 2};
    """

    try:
        result = overpass.query(query)
    except overpy.exception.OverpassTooManyRequests:
        print("Overpass API rate limit hit.")
        return []

    all_waypoints = [
        (way.center_lat, way.center_lon)
        for way in result.ways
        if hasattr(way, "center_lat") and hasattr(way, "center_lon")
    ]

    if not all_waypoints:
        print("No suitable roads found.")
        return []

    random.shuffle(all_waypoints)
    selected = all_waypoints[:NUMBER_OF_WAYS]
    return snap_to_road(selected)


def snap_to_road(coordinates: list[tuple[float, float]]):
    snapped = []
    for coord in coordinates:
        url = f"{OSRM_NEAREST_URL}/{coord[1]},{coord[0]}"
        try:
            response = requests.get(url)
            if response.status_code != HTTP_STATUS_OK:
                return None

            data = response.json()
            if "waypoints" in data and len(data["waypoints"]) > 0:
                loc = data["waypoints"][0]["location"]
                snapped.append((loc[1], loc[0]))

        except requests.exceptions.RequestException as e:
            print(f"Snap failed: {e}")
    return snapped


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
