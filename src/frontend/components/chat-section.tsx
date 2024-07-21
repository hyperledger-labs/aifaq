"use client";

import React, { useState } from 'react';
import ChatBottomBar from './chat-bottom-bar';
import ChatResponse from './chat-response';

interface Message {
    request: string;
    response: string;
}

const ChatSection = () => {
    const [messages, setMessages] = useState<Message[]>([]);

    const sendMessage = async (message: string) => {
        // const response = await fetch('http://localhost:8080/chat', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({ message }),
        // });
        // const data = await response.json();
        // setMessages([...messages, { request: message, response: data.response }]);

        setMessages([...messages, { request: "message sent successfully", response: "the original message is " + message }]);
    };

    return (
        <div className="flex flex-col h-full">
            <div className="flex-1 overflow-y-auto">
                {messages.map((msg, index) => (
                    <ChatResponse key={index} request={msg.request} response={msg.response} />
                ))}
            </div>
            <ChatBottomBar onSend={sendMessage} />
        </div>
    );
};

export default ChatSection;