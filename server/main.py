from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from service import route_service, decode_polyline_service

RADIUS_M = 2000

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RouteRequest(BaseModel):
    start_latitude: float
    start_longitude: float


@app.post("/generate-route")
async def generate_route(request: RouteRequest):
    location_coordinates = [request.start_latitude, request.start_longitude]

    route = route_service.compile_route(location_coordinates, RADIUS_M)

    if not route:
        return

    route_coordinates = decode_polyline_service.decode_polyline(route)
    return {"route": route_coordinates}
