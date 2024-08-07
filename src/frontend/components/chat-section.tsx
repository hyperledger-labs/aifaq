import React, { useRef, useEffect } from 'react';
import { Message } from '@/lib/types';
import ChatRequest from './chat-request';
import ChatResponse from './chat-response';

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
        <div className='relative flex flex-col items-center py-2'>
            <div className='flex flex-col max-w-3xl w-full flex-grow space-y-2' ref={chatContainerRef}>
                {messages.map((message, index) => (
                    <div key={message.id}>
                        {
                            message.type === 0 ? <ChatRequest request={message.content} /> : <ChatResponse response={message.content} />
                        }
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ChatSection;