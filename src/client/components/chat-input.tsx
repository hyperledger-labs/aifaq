"use client"

import { FormEvent, ChangeEvent, KeyboardEvent } from "react";
import { Button } from "@/components/ui/button";
import { Send } from "lucide-react";

type ChatInputProps = {
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
}: ChatInputProps) {
    const handleInput = (e: ChangeEvent<HTMLTextAreaElement>) => {
        const textarea = e.target;
        setUserMessage(textarea.value);
        
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (userMessage.trim()) {
                handleSendMessage(e as unknown as FormEvent);
                (e.target as HTMLTextAreaElement).style.height = 'auto';
            }
        }
    };

    return (
        <div className="px-4 pb-4">
            <div className="relative flex items-center max-w-2xl mx-auto">
                <form onSubmit={handleSendMessage} className="relative flex w-full items-end">
                    <div className="relative flex-1 overflow-hidden rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 shadow-sm">
                        <textarea
                            rows={1}
                            value={userMessage}
                            onChange={handleInput}
                            onKeyDown={handleKeyDown}
                            placeholder="Ask anything..."
                            disabled={isDisabled}
                            className="w-full resize-none bg-transparent px-4 py-3 pr-12 text-sm focus:outline-none disabled:opacity-50 dark:text-white chat-textarea"
                        />
                        <div className="absolute right-2 bottom-2">
                            <Button 
                                type="submit" 
                                size="icon"
                                variant="ghost"
                                disabled={isDisabled || !userMessage.trim()}
                                className="h-8 w-8 hover:bg-gray-100 dark:hover:bg-gray-800"
                            >
                                <Send className="h-4 w-4" />
                                <span className="sr-only">Send message</span>
                            </Button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
}