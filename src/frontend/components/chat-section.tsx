"use client";

import React, {useRef, useEffect } from 'react';
import ChatResponse from './chat-response';
import ChatRequest from './chat-request';

interface Message {
    request: string;
    response: string;
}

interface ChatSectionProps {
    messages: Message[];
}

const ChatSection: React.FC<ChatSectionProps> = ({ messages }) => {
    const chatContainerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className='relative flex flex-col items-center h-screen overflow-hidden'>
            <div className='flex flex-col max-w-3xl w-full p-4 space-y-4 flex-grow overflow-y-auto' ref={chatContainerRef} style={{ paddingBottom: '5rem' }}>
                {messages.map((msg, index) => (
                    <div key={index}>
                        <ChatRequest request={msg.request} /> 
                        <ChatResponse response={msg.response} /> 
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ChatSection;
