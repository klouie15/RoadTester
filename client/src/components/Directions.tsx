import { JSX } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight, ArrowLeft, ArrowUp, ArrowDown } from "lucide-react";

type DirectionStepType = "left" | "right" | "straight" | "uturn";

interface DirectionStep {
    instruction: string;
    distance: string;
    type: DirectionStepType;
}

function Directions({ steps }: { steps: DirectionStep[] }): JSX.Element {
    const getDirectionIcon: (type: DirectionStepType) => JSX.Element =
        (type: DirectionStepType): JSX.Element => {

            switch (type) {
                case "left":
                    return <ArrowLeft className="size-4" />;
                case "right":
                    return <ArrowRight className="size-4" />;
                case "straight":
                    return <ArrowUp className="size-4" />;
                case "uturn":
                    return <ArrowDown className="size-4" />;
            }
        };

    const totalDistance: number = steps.reduce((total: number, step: DirectionStep): number => {
        const distance: number = parseFloat(step.distance.split(' ')[0]);
        return total + (step.distance.includes('km') ? distance : distance / 1000);
    }, 0);

    const estimatedTime: number = Math.round(totalDistance * 2);

    return (
        <Card className="w-full max-w-lg h-[80vh] flex flex-col">
            <CardHeader>
                <CardTitle>Directions</CardTitle>
            </CardHeader>
            <CardContent className="flex-1 overflow-y-auto">
                {steps.length === 0 ? (
                    <div className="flex items-center justify-center h-full text-muted-foreground">
                        <p className="text-center">Select a location and generate a route to see directions</p>
                    </div>
                ) : (
                    <>
                        <div className="mb-4 p-3 bg-muted/30 rounded-lg">
                            <p className="text-sm font-medium">Total Distance: {totalDistance.toFixed(1)} km</p>
                            <p className="text-sm font-medium">Estimated Time: {estimatedTime} minutes</p>
                        </div>
                        <div className="space-y-4">
                            {steps.map((step: DirectionStep, index: number): JSX.Element => (
                                <div
                                    key={index}
                                    className="flex items-start gap-3 p-3 rounded-lg bg-muted/50"
                                >
                                    <div className="flex items-center justify-center size-8 rounded-full bg-primary/10 text-primary">
                                        {getDirectionIcon(step.type)}
                                    </div>
                                    <div className="flex-1">
                                        <p className="text-sm font-medium">{step.instruction}</p>
                                        <p className="text-xs text-muted-foreground">{step.distance}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </>
                )}
            </CardContent>
        </Card>
    );
}

export default Directions;