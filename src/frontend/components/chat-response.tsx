import React from 'react';
import { IconHyperledger } from './icons/IconHyperledger';
import ChatResponseOptions from './chat-response-options';

interface Props {
    response: string;
}

const ChatResponse = ({ response }: Props) => (
    <div className='flex flex-row space-x-4 p-4'>
        <div className='h-10 w-10 rounded-full border shrink-0 p-2 bg-background'>
            <IconHyperledger />
        </div>

        <div className='flex flex-col'>
            <div className='w-fit p-2'>
                <p> {response} </p>
            </div>
            <div className='mt-4'>
                <ChatResponseOptions text={response} />
            </div>
        </div>
    </div>
);

export default ChatResponse;