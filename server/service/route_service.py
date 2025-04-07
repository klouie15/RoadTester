import requests
import overpy
import random
from typing import TypedDict, List, Dict, Any
import polyline


HTTP_STATUS_OK = 200

KM_TO_DEGREES_CONVERSION = 111
M_TO_KM_CONVERSION = 1000

NUMBER_OF_WAYS = 3
RADIUS_M = 1750

OSRM_BASE_URL = "http://router.project-osrm.org/route/v1/driving"
OSRM_NEAREST_URL = "http://router.project-osrm.org/nearest/v1/driving"

class DirectionStep(TypedDict):
    instruction: str
    distance: str
    type: str

def format_distance(meters: float) -> str:
    if meters < 1000:
        return f"{int(meters)} meters"
    else:
        return f"{meters/1000:.1f} km"

def get_direction_type(maneuver: Dict[str, Any]) -> str:
    maneuver_type = maneuver.get("type", "")
    modifier = maneuver.get("modifier", "")
    
    if maneuver_type == "turn":
        if modifier in ["left", "right"]:
            return modifier
    elif maneuver_type == "continue":
        return "straight"
    elif maneuver_type == "depart":
        return "straight"
    elif maneuver_type == "arrive":
        return "straight"
    return "straight"


def generate_route(start_coordinates: tuple[float, float]) -> Dict[str, Any] | None:
    start = str(start_coordinates[1]) + "," + str(start_coordinates[0])

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
    url = f"{OSRM_BASE_URL}/{coordinate_str}?overview=full&continue_straight=true&steps=true"
    print(f"Request URL: {url}")

    try:
        response = requests.get(url)
        print(f"Response status: {response.status_code}")
        
        if response.status_code != HTTP_STATUS_OK:
            print(f"Error response: {response.text}")
            return None
            
        data = response.json()
        
        if not data or "routes" not in data or not data["routes"]:
            print("No routes found in response")
            return None
            
        route_data = data["routes"][0]
        if "geometry" not in route_data:
            print("Invalid route geometry data")
            return None

        decoded_coordinates = polyline.decode(route_data["geometry"])
        route_coordinates = [[lat, lon] for lat, lon in decoded_coordinates]
        steps = process_steps(route_data)

        return {
            "route": route_coordinates,
            "steps": steps
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing response: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def process_steps(route_data):
    steps: List[DirectionStep] = []
    if "legs" in route_data and route_data["legs"]:
        for leg in route_data["legs"]:
            if "steps" in leg:
                for step in leg["steps"]:
                    if step["maneuver"]["type"] == "arrive":
                        continue

                    instruction = step["name"]
                    distance = format_distance(step["distance"])
                    direction_type = get_direction_type(step["maneuver"])

                    steps.append({
                        "instruction": instruction,
                        "distance": distance,
                        "type": direction_type
                    })
    return steps


def generate_random_waypoints(
    start_coordinates: tuple[float, float],
    radius_m: int
) -> list[tuple[float, float]]:

    overpass = overpy.Overpass()
    lat, lon = start_coordinates

    query = f"""
    [out:json];
    (
      way(around:{radius_m},{lat},{lon})
        ["highway"~"residential|unclassified|tertiary|secondary|primary"]
        ["service"!~"parking_aisle|driveway|parking"]
        ["access"!~"private|no"];
     way(around:{radius_m},{lat},{lon})
        ["highway"~"residential|unclassified|tertiary|secondary|primary"]
        ["service"!~"parking_aisle|driveway|parking"]
        ["access"!~"private|no"];
    );
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
