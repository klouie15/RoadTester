import * as React from "react";
import LocationSelector from "./components/LocationSelector.tsx";
import Map from "./components/Map";
import GenerateButton from "@/components/GenerateButton.tsx";

function App() {
    const [center, setCenter] = React.useState<number[]>([49.2629570706, -123.0292688621]);
    const [isLocationSelected, setIsLocationSelected] = React.useState<boolean>(false);

    return <>
        <h1 className={"text-3xl"}>RoadTester</h1>
        <LocationSelector setCenter={
            (coordinates: number[]): void => {
                setCenter(coordinates);
                setIsLocationSelected(true)
            }
        } />
        <GenerateButton />
        <Map center={center} isLocationSelected={isLocationSelected} />
    </>
}

export default App
