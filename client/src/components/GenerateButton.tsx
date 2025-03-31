import { Button } from "@/components/ui/button"
import { JSX } from "react";

function GenerateButton({ onClick }: { onClick: () => void }): JSX.Element {

    return <div className={"my-6"}>
        <Button variant="outline" onClick={onClick}>Generate Route</Button>
    </div>
}

export default GenerateButton;