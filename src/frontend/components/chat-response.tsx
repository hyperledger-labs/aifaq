import React from 'react'
import { IconHyperledger } from './icons/IconHyperledger'

type Props = {
    text: string
}

const ChatResponse = ({ text }: Props) => {
    return (
        <div className='flex flex-row'>
            <div className='h-10 w-10 rounded-full border aspect-square p-2'>
                <IconHyperledger />
            </div>
            <div className='w-fit p-2'>
                {text}
            </div>
        </div>
    )
}

export default ChatResponse