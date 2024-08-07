"use client";

import React, { useEffect, useState } from 'react';
import { Button } from './ui/button';
import { ArrowUp, Paperclip } from 'lucide-react';
import TextareaAutosize from 'react-textarea-autosize';
import { useWindowSize } from '@/hooks/useWindowSize';
import { Message } from '@/lib/types';
import { v4 as uuidv4 } from 'uuid';
import { handleSend } from '@/lib/apis/fetcher';

interface Props {
    onSend: (newMessage: Message) => void
}

const ChatBottomBar = ({ onSend }: Props) => {
    const [isMounted, setIsMounted] = useState(false);
    const [message, setMessage] = useState<Message>({
        content: '',
        type: 0,
        id: "-1"
    });
    const { isMobile } = useWindowSize();

    useEffect(() => {
        setIsMounted(true);
    }, [isMounted]);

    if (!isMounted) {
        return null;
    }

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setMessage({
            ...message,
            content: e.target.value
        });
    };

    const handleSubmit = (e?: React.FormEvent | React.KeyboardEvent) => {
        if (e) {
            e.preventDefault();
            if ('key' in e && e.key !== 'Enter') {
                return;
            }
        }

        if (message.content.trim()) {
            const updatedMessage = {
                ...message,
                id: uuidv4(),
            };

            handleSend(updatedMessage).then((value) => {
                if (value !== undefined) {
                    onSend(updatedMessage)
                    onSend(value.message)
                }
            }).catch().finally(() => setMessage({
                ...message,
                content: '',
            }))
        }
    };

    return (
        <div className='w-full px-4 max-w-3xl mx-auto'>
            <form className="flex flex-row p-2 rounded-3xl border items-end gap-2" onSubmit={handleSubmit}>
                <Button size='icon' variant='link' className="rounded-full flex-shrink-0">
                    <Paperclip />
                </Button>
                <TextareaAutosize
                    autoFocus
                    className='flex-grow resize-none outline-none bg-transparent w-full pb-1'
                    minRows={1}
                    maxRows={isMobile ? 4 : 8}
                    placeholder='Ask AIFAQ'
                    value={message.content}
                    onChange={handleChange}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            handleSubmit(e);
                        }
                    }}
                />
                <Button
                    size='icon'
                    variant='default'
                    className="rounded-full flex-shrink-0"
                    type="button"
                    onClick={handleSubmit}
                >
                    <ArrowUp />
                </Button>
            </form>
            <div className='flex justify-center text-xxs py-1 text-muted-foreground text-center'>AIFAQ can make mistakes. Check important information.</div>
        </div>
    );
};

export default ChatBottomBar;