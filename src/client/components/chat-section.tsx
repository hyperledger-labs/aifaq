"use client";
import { FormEvent, useState, useRef, useEffect } from "react";
import { Message } from "@/lib/types";
import ChatRequest from "./chat-request";
import ChatResponse from "./chat-response";
import ChatInput from "./chat-input";
import { LoaderCircle } from "lucide-react";

export default function ChatSection() {
    const chatContainerRef = useRef<HTMLDivElement | null>(null);
    const [userMessage, setUserMessage] = useState("");
    const [loading, setLoading] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);

    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTo({
                top: chatContainerRef.current.scrollHeight,
                behavior: "smooth",
            });
        }
    }, [messages, loading]);

    const handleSendMessage = async (e: FormEvent) => {
        e.preventDefault();

        if (!userMessage) return;

        const newMessage: Message = { role: "user", content: userMessage };
        setMessages((prevMessages) => [...prevMessages, newMessage]);
        setUserMessage("");
        setLoading(true);

        try {
            const apiUrl = `http://${process.env.NEXT_PUBLIC_API_URL}/query`;
            const response = await fetch(apiUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ text: userMessage }),
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }

            const { msg: assistantResponse } = await response.json();

            setMessages((prevMessages) => [
                ...prevMessages,
                { role: "assistant", content: assistantResponse },
            ]);
        } catch (error) {
            console.error("API Error", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full">
            <div
                ref={chatContainerRef}
                className="flex flex-col flex-1 items-center overflow-y-auto"
            >
                {messages &&
                    messages.map((m, i) => {
                        return m.role === "assistant" ? (
                            <ChatResponse {...m} key={i} />
                        ) : (
                            <ChatRequest {...m} key={i} />
                        );
                    })}

                {loading && (
                    <div className="text-center text-gray-500 mt-2">
                        <LoaderCircle className="animate-spin" />
                    </div>
                )}
            </div>

            <ChatInput
                isDisabled={loading}
                userMessage={userMessage}
                setUserMessage={setUserMessage}
                handleSendMessage={handleSendMessage}
            />
        </div>
    );
}