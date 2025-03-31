from fastapi import FastAPI
from service import route_service, decode_polyline_service
from request import RouteRequest

RADIUS_M = 2000

app = FastAPI()


@app.post("/generate-route")
async def generate_route(request: RouteRequest):
    location_coordinates = [request["start_latitude"], request["start_longitude"]]

    route = route_service.compile_route(location_coordinates, RADIUS_M)

    if not route:
        return

    route_coordinates = decode_polyline_service.decode_polyline(route)
    return {"route": route_coordinates}
