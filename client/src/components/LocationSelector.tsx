import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import Location, { toLatLngExpression } from "../models/Location.tsx"
import locations from "../../../data/locations.json";
import { JSX } from "react";
import { LatLngExpression } from "leaflet";

function LocationSelector({ setCenter, setLocation }: {
    setCenter: (coordinates: LatLngExpression) => void,
    setLocation: (location: Location) => void
}): JSX.Element {

    function handleSelectChange(locationName: string): void {
        const selectedLocation = locations.find(
            (location) => location.location === locationName
        );

        if (selectedLocation) {
            setCenter(toLatLngExpression(selectedLocation))
            setLocation(selectedLocation)
        }
    }

    return <div className={"my-6"}>
        <Select onValueChange={handleSelectChange}>
            <SelectTrigger className="w-[200px]">
                <SelectValue placeholder="Select Testing Location" />
            </SelectTrigger>
            <SelectContent>
                {locations.map((location) => (
                    <SelectItem key={location.address} value={location.location}>{location.location}</SelectItem>
                ))}
            </SelectContent>
        </Select>
    </div>
}

export default LocationSelector;