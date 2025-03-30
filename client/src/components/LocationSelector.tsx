import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import Location from "../models/Location.tsx"
import locations from "../../../data/locations.json";
import { JSX } from "react";

function LocationSelector({ setCenter }: {
    setCenter: (coordinates: number[]) => void
}): JSX.Element {

    function handleSelectChange(locationName: string): void {

        const selectedLocation: Location | undefined = locations.find(
            (location: Location): boolean => location.location === locationName
        );

        if (selectedLocation) {
            setCenter(selectedLocation.coordinates)
        }
    }

    return <div className={"my-6"}>
        <Select onValueChange={handleSelectChange}>
            <SelectTrigger className="w-[200px]">
                <SelectValue placeholder="Select Testing Location" />
            </SelectTrigger>
            <SelectContent>
                {locations.map((location: Location) => (
                    <SelectItem key={location.address} value={location.location}>{location.location}</SelectItem>
                ))}
            </SelectContent>
        </Select>
    </div>
}

export default LocationSelector;