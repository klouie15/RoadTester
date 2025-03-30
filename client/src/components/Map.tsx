import { JSX, useEffect } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import 'leaflet/dist/leaflet.css';

const defaultZoom = 11;
const locationSelectedZoom = 14;

function Map({ center, isLocationSelected }: { center: number[], isLocationSelected: boolean }): JSX.Element {
    return <div className={"relative z-0"}>
        <MapContainer center={center} zoom={isLocationSelected ? locationSelectedZoom : defaultZoom}>
            <TileLayer
                attribution={'&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'}
                url={'https://tile.openstreetmap.org/{z}/{x}/{y}.png'}
            />
            <ChangeView center={center} zoom={isLocationSelected ? locationSelectedZoom : defaultZoom} />
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