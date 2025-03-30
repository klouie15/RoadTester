import { MapContainer, TileLayer } from "react-leaflet";
import 'leaflet/dist/leaflet.css';

function Map({ center }: { center: number[] }) {
    return <div className={"relative z-0"}>
        <MapContainer center={center} zoom={12}>
            <TileLayer
                attribution={'&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'}
                url={'https://tile.openstreetmap.org/{z}/{x}/{y}.png'}
            />
        </MapContainer>
    </div>
}

export default Map;