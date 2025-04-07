import { LatLngExpression } from "leaflet";

interface Location {
    location: string;
    address: string;
    coordinates: LatLngExpression;
}

export default Location;