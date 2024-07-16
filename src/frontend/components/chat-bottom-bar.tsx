"use client"
import React, { useEffect, useState } from 'react'
import { Button } from './ui/button'
import { ArrowUp, Paperclip } from 'lucide-react'
import TextareaAutosize from 'react-textarea-autosize'
import { useWindowSize } from '@/hooks/useWindowSize'

type Props = {}

const ChatBottomBar = (props: Props) => {
    const [isMounted, setIsMounted] = useState(false);
    const { isMobile } = useWindowSize();

    useEffect(() => {
        setIsMounted(true);
    }, [isMounted]);

    if (!isMounted) {
        return null;
    }

    return (
        <div className="w-full max-w-3xl mx-auto">
            <div className='flex flex-col mx-2'>
                <div className="flex flex-row bg-background p-2 rounded-3xl border items-end gap-2">
                    <Button size='icon' variant='link' className="rounded-full flex-shrink-0">
                        <Paperclip />
                    </Button>
                    <TextareaAutosize
                        autoFocus
                        className='flex-grow resize-none outline-none bg-transparent w-full pb-1'
                        minRows={1}
                        maxRows={isMobile ? 4 : 8}
                        placeholder='Ask AIFAQ'
                    />
                    <Button size='icon' variant='default' className="rounded-full flex-shrink-0">
                        <ArrowUp />
                    </Button>
                </div>
                <div className='flex justify-center text-xxs py-1 text-muted-foreground text-center'>AIFAQ can make mistakes. Check important information.</div>
            </div>
        </div>
    )
}

export default ChatBottomBar