import LocationSelector from "./components/LocationSelector.tsx";
import Map from "./components/Map";
import GenerateButton from "@/components/GenerateButton.tsx";
import Location from "@/models/Location.tsx";
import { JSX, useState } from "react";
import {LatLngExpression} from "leaflet";

function App(): JSX.Element {
    const [center, setCenter] = useState<number[]>([49.2629570706, -123.0292688621]);
    const [isLocationSelected, setIsLocationSelected] = useState<boolean>(false);
    const [location, setLocation] = useState<Location | null>(null);

    return <>
        <h1 className={"text-3xl"}>RoadTester</h1>
        <LocationSelector setCenter={
            (coordinates: number[]): void => {
                setCenter(coordinates);
                setIsLocationSelected(true)
            }
        } setLocation={setLocation}
        />
        <GenerateButton/>
        <Map
            center={center}
            isLocationSelected={isLocationSelected}
            location={location}
            route={route}
        />
    </>
}

export default App
