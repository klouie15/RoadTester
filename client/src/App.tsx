import LocationSelector from "./components/LocationSelector.tsx";
import Map from "./components/Map";
import GenerateButton from "@/components/GenerateButton.tsx";
import Location from "@/models/Location.tsx";
import { JSX, useState } from "react";
import {LatLngExpression} from "leaflet";
import RouteRequest from "@/models/RouteRequest.tsx";
import axios from "axios";

function App(): JSX.Element {
    const [center, setCenter] = useState<number[]>([49.2629570706, -123.0292688621]);
    const [isLocationSelected, setIsLocationSelected] = useState<boolean>(false);
    const [location, setLocation] = useState<Location | null>(null);
    const [route, setRoute] = useState<LatLngExpression[]>([]);

    const generateRoute: () => Promise<void> =
        async (): Promise<void> => {

        if (!location) {
            return;
        }

        try {
            const request: RouteRequest = {
                start_latitude: location.coordinates[0],
                start_longitude: location.coordinates[1],
            }
            const response = await axios.post("http://127.0.0.1:8000/generate-route", request);

            console.log(response);
            setRoute(response.data.route)
        } catch (error) {
            console.error(error);
        }
    };

    return <>
        <h1 className={"text-3xl"}>RoadTester</h1>
        <LocationSelector setCenter={
            (coordinates: number[]): void => {
                setCenter(coordinates);
                setIsLocationSelected(true)
            }
        } setLocation={setLocation}
        />
        <GenerateButton onClick={(): Promise<void> => generateRoute()} />
        <Map
            center={center}
            isLocationSelected={isLocationSelected}
            location={location}
            route={route}
        />
    </>
}

export default App
