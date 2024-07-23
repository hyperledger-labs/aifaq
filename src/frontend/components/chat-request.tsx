"use client";

import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { UserRound } from 'lucide-react'

interface Props {
    request: string;
}

const ChatRequest = ({ request }: Props) => {
    return (
        <div className='flex justify-end p-2 mr-5'>
            <div className='flex flex-col items-end mr-2'>
                <div className='bg-muted w-fit px-4 py-2 rounded-xl text-left'>
                    <p> {request} </p>
                </div>
            </div>
            <div className='h-10 w-10 rounded-full border flex justify-center items-center p-2 shrink-0'>
                <Avatar className=''>
                    <AvatarImage src="" />
                    <AvatarFallback>
                        <UserRound />
                    </AvatarFallback>
                </Avatar>
            </div>
        </div>
    );
};

export default ChatRequest;