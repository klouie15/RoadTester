import * as React from "react";
import LocationSelector from "./components/LocationSelector.tsx";
import Map from "./components/Map";

function App() {
    const [center, setCenter] = React.useState<number[]>([49.2629570706, -123.0292688621]);

    return <>
        <h1 className={"text-3xl"}>RoadTester</h1>
        <LocationSelector/>
        <Map center={center}/>
    </>
}

export default App
