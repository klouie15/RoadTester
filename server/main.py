from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from service import route_service, decode_polyline_service


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
    location_coordinates = (request.start_latitude, request.start_longitude)

    route = route_service.generate_route(location_coordinates)

    if not route:
        return

    route_coordinates = decode_polyline_service.decode_polyline(route["routes"][0]["geometry"])
    return {"route": route_coordinates}
