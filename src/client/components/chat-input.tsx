import { FormEvent } from "react";
import { Button } from "./ui/button";
import { Send } from "lucide-react";

type ChatProps = {
    isDisabled: boolean;
    userMessage: string;
    setUserMessage: (value: string) => void;
    handleSendMessage: (e: FormEvent) => void;
};

export default function ChatInput({
    isDisabled,
    userMessage,
    setUserMessage,
    handleSendMessage,
}: ChatProps) {
    return <div className="flex items-center mt-auto">
        <form
            onSubmit={handleSendMessage}
            className="flex items-center justify-center w-full"
        >
            <input
                type="text"
                value={userMessage}
                disabled={isDisabled}
                onChange={(e) => setUserMessage(e.target.value)}
                placeholder="Type your message here"
                className="flex h-10 w-full rounded-md px-3 text-sm text-foreground outline-none"
            />
            <Button size="icon" className="flex items-center justify-center aspect-square rounded-full" disabled={isDisabled}>
                <Send />
            </Button>
        </form>
    </div>
}