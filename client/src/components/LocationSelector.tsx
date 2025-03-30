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

function LocationSelector(): JSX.Element {
    return <div className={"my-6"}>
        <Select>
            <SelectTrigger className="w-[200px]">
                <SelectValue placeholder="Select Testing Location" />
            </SelectTrigger>
            <SelectContent>
                {locations.map((location: Location) => (
                    <SelectItem value={location.location}>{location.location}</SelectItem>
                ))}
            </SelectContent>
        </Select>
    </div>
}

export default LocationSelector;