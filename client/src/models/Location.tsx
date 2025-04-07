import { LatLngExpression } from "leaflet";

export default interface Location {
    location: string;
    address: string;
    coordinates: number[];
}

export function toLatLngExpression(location: Location): LatLngExpression {
    return [location.coordinates[0], location.coordinates[1]] as LatLngExpression;
}