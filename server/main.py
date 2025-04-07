from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from service import route_service


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
    start_coordinates: tuple[float, float]


@app.post("/generate-route")
async def generate_route(request: RouteRequest):
    location_coordinates = (request.start_coordinates[0], request.start_coordinates[1])

    response = route_service.generate_route(location_coordinates)

    if not response:
        return

    return response
