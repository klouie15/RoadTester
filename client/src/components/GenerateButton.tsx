import { Button } from "@/components/ui/button"
import { JSX, useState } from "react";
import { LatLngExpression } from "leaflet";

function onClick() {
    // TODO: Call generate route API

}

function GenerateButton(): JSX.Element {
    const [route, setRoute] = useState<LatLngExpression[]>([]);

    return <div className={"my-6"}>
        <Button variant="outline" onClick={onClick}>Generate Route</Button>
    </div>
}

export default GenerateButton;