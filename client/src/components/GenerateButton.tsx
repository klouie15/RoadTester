import { Button } from "@/components/ui/button"

function onClick() {
    // TODO: Call generate route API
}

function GenerateButton() {
    return <div className={"my-6"}>
        <Button variant="outline" onClick={onClick}>Generate Route</Button>
    </div>
}

export default GenerateButton;