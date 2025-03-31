import * as React from "react";
import LocationSelector from "./components/LocationSelector.tsx";
import Map from "./components/Map";
import GenerateButton from "@/components/GenerateButton.tsx";
import Location from "@/models/Location.tsx";
import { JSX } from "react";

function App(): JSX.Element {
    const [center, setCenter] = React.useState<number[]>([49.2629570706, -123.0292688621]);
    const [isLocationSelected, setIsLocationSelected] = React.useState<boolean>(false);
    const [location, setLocation] = React.useState<Location | null>(null);

    return <>
        <h1 className={"text-3xl"}>RoadTester</h1>
        <LocationSelector setCenter={
            (coordinates: number[]): void => {
                setCenter(coordinates);
                setIsLocationSelected(true)
            }
        } setLocation={setLocation}
        />
        <GenerateButton />
        <Map center={center} isLocationSelected={isLocationSelected} location={location} />
    </>
}

export default App
