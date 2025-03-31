import Location from "../models/Location.tsx"
import { JSX, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { useMap } from "react-leaflet";
import 'leaflet/dist/leaflet.css';

const defaultZoom = 11;
const locationSelectedZoom = 14;

function Map({ center, isLocationSelected, location }: {
    center: number[], isLocationSelected: boolean, location: Location | null;
}): JSX.Element {

    return <div className={"relative z-0"}>
        <MapContainer center={center} zoom={isLocationSelected ? locationSelectedZoom : defaultZoom}>
            <TileLayer
                attribution={'&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'}
                url={'https://tile.openstreetmap.org/{z}/{x}/{y}.png'}
            />
            <ChangeView center={center} zoom={isLocationSelected ? locationSelectedZoom : defaultZoom} />

            {isLocationSelected && (
                <Marker position={center}>
                    {location && (
                        <Popup>{location.location} <br/> {location.address}</Popup>
                    )}
                </Marker>
                )
            }
        </MapContainer>
    </div>
}

function ChangeView({ center, zoom }: { center: number[], zoom: number }): null {
    const map = useMap();

    useEffect((): void => {
        map.setView(center, zoom);
    }, [center, map, zoom]);

    return null;
}

export default Map;