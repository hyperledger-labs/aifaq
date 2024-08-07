import React from 'react';

interface Props {
    request: string;
}

const ChatRequest = ({ request }: Props) => {
    return (
        <div className='flex justify-end'>
            <div className='flex flex-col items-end mr-1'>
                <div className='bg-muted w-fit px-4 py-2 rounded-xl text-left'>
                    <p> {request} </p>
                </div>
            </div>
        </div>
    );
};

export default ChatRequest;