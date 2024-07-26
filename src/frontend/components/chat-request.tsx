import React from 'react';

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
        </div>
    );
};

export default ChatRequest;