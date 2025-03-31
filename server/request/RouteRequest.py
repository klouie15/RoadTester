from pydantic import BaseModel

class RouteRequest(BaseModel):
    start_latitude: float
    start_longitude: float