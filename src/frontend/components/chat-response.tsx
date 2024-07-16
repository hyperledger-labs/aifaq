import React from 'react'
import { IconHyperledger } from './icons/IconHyperledger'
import ChatResponseOptions from './chat-response-options'

type Props = {
    text: string
}

const ChatResponse = ({ text }: Props) => {
    return (
        <div className='flex flex-row'>
            <div className='h-10 w-10 rounded-full border shrink-0 p-2'>
                <IconHyperledger />
            </div>
            <div className='flex flex-col'>
                <div className='w-fit p-2'>
                    {text}
                </div>
                <ChatResponseOptions text={text} />
            </div>
        </div>
    )
}

export default ChatResponse