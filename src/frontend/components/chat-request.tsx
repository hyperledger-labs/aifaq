"use client";

import React, { useState } from 'react';

interface ChatRequestProps {
    onSend: (message: string) => void;
}

const ChatRequest = ({ onSend }: ChatRequestProps) => {
    const [message, setMessage] = useState('');

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setMessage(e.target.value);
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (message.trim()) {
            onSend(message);
            setMessage('');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input 
                type="text" 
                value={message} 
                onChange={handleChange} 
            />
            <button type="submit">Send</button>
        </form>
    );
};

export default ChatRequest;