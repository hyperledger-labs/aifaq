"use client";

import React from 'react';
import { IconHyperledger } from './icons/IconHyperledger';
import ChatResponseOptions from './chat-response-options';

interface Props {
    request: string;
    response: string;
}

const ChatResponse = ({ request, response }: Props) => (
    <div className='flex flex-row space-x-4 p-4'>
        <div className='h-10 w-10 rounded-full border shrink-0 p-2'>
            <IconHyperledger />
        </div>

        <div className='flex flex-col space-y-4'>
            <div className='w-fit p-2 bg-gray-100 rounded-md'>
                <p className='mb-2'><strong>You:</strong> {request}</p>
                <p><strong>ChatBot:</strong> {response}</p>
            </div>
            <div className='mt-4'>
                <ChatResponseOptions text={response} />
            </div>
        </div>
    </div>
);

export default ChatResponse;