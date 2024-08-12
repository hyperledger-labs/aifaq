"use client";

import React, { useEffect, useState } from 'react';
import { Button } from './ui/button';
import { ArrowUp, Paperclip } from 'lucide-react';
import TextareaAutosize from 'react-textarea-autosize';
import { useWindowSize } from '@/hooks/useWindowSize';

interface Props {
    onSend: (message: string) => void;
}

const ChatBottomBar = ({ onSend }: Props) => {
    const [isMounted, setIsMounted] = useState(false);
    const [message, setMessage] = useState('');
    const { isMobile } = useWindowSize();

    useEffect(() => {
        console.log('ChatBottomBar onSend:', onSend);
        setIsMounted(true);
    }, [isMounted]);

    if (!isMounted) {
        return null;
    }

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setMessage(e.target.value);
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (message.trim()) {
            onSend(message);
            setMessage('');
        }
    };

    const handleSendButtonClick = () => {
        if (message.trim()) {
            onSend(message);
            setMessage('');
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e as unknown as React.FormEvent);
        }
    };

    return (
        <div className="w-full max-w-3xl mx-auto">
            <div className='flex flex-col mx-2'>
                <form className="flex flex-row bg-background p-2 rounded-3xl border items-end gap-2" onSubmit={handleSubmit}>
                    <Button size='icon' variant='link' className="rounded-full flex-shrink-0">
                        <Paperclip />
                    </Button>
                    <TextareaAutosize
                        autoFocus
                        className='flex-grow resize-none outline-none bg-transparent w-full pb-1'
                        minRows={1}
                        maxRows={isMobile ? 4 : 8}
                        placeholder='Ask AIFAQ'
                        value={message}
                        onChange={handleChange}
                        onKeyDown={handleKeyDown}
                    />
                    <Button
                        size='icon'
                        variant='default'
                        className={`rounded-full flex-shrink-0 transition-opacity duration-200 ${
                            message.trim() ? 'opacity-100' : 'opacity-50'
                        }`}
                        type="button"
                        onClick={handleSendButtonClick}
                        disabled={!message.trim()}
                    >
                        <ArrowUp />
                    </Button>
                </form>
                <div className='flex justify-center text-xxs py-1 text-muted-foreground text-center'>AIFAQ can make mistakes. Check important information.</div>
            </div>
        </div>
    );
};

export default ChatBottomBar;
