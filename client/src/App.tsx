import LocationSelector from "./components/LocationSelector.tsx";
import Map from "./components/Map";
import GenerateButton from "@/components/GenerateButton.tsx";
import Location from "@/models/Location.tsx";
import { JSX, useEffect, useState } from "react";
import { LatLngExpression } from "leaflet";
import RouteRequest from "@/models/RouteRequest.tsx";
import axios from "axios";
import Directions from "./components/Directions.tsx";

interface DirectionStep {
    instruction: string;
    distance: string;
    type: "left" | "right" | "straight" | "uturn";
}

interface RouteResponse {
    route: LatLngExpression[];
    steps: DirectionStep[];
}

function App(): JSX.Element {
    const [center, setCenter] = useState<LatLngExpression>([49.2629570706, -123.0292688621]);
    const [isLocationSelected, setIsLocationSelected] = useState<boolean>(false);
    const [location, setLocation] = useState<Location | null>(null);
    const [route, setRoute] = useState<LatLngExpression[]>([]);
    const [steps, setSteps] = useState<DirectionStep[]>([]);

    useEffect((): void => {
        setRoute([]);
        setSteps([]);
    }, [center]);

    const generateRoute: () => Promise<void> =
        async (): Promise<void> => {
            if (!location) {
                return;
            }

            try {
                const request: RouteRequest = {
                    start_coordinates: location.coordinates
                }
                const response = await axios.post<RouteResponse>("http://127.0.0.1:8000/generate-route", request);
                setRoute(response.data.route);
                setSteps(response.data.steps);
            } catch (error) {
                console.error(error);
            }
        };

    return <>
        <h1 className={"text-3xl font-semibold"}>RoadTester</h1>
        <LocationSelector setCenter={
            (coordinates: LatLngExpression): void => {
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

        {steps.length > 0 && (
            <div className={"my-6 flex justify-center"}>
                <Directions steps={steps} />
            </div>
        )}
    </>
}

export default App
