import { JSX } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight, ArrowLeft, ArrowUp, ArrowDown } from "lucide-react";

interface DirectionStep {
    instruction: string;
    distance: string;
    type: "left" | "right" | "straight" | "uturn";
}

function Directions({ steps }: { steps: DirectionStep[] }): JSX.Element {
    const getDirectionIcon = (type: DirectionStep["type"]) => {
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

    return (
        <Card className="w-full max-w-md h-[500px] flex flex-col">
            <CardHeader>
                <CardTitle>Directions</CardTitle>
            </CardHeader>
            <CardContent className="flex-1 overflow-y-auto">
                <div className="space-y-4">
                    {steps.map((step, index) => (
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
            </CardContent>
        </Card>
    );
}

export default Directions;