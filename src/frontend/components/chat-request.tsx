import React from 'react'

type Props = {
    text: string
}

const ChatRequest = ({ text }: Props) => {
    return (
        <div className='flex justify-end'>
            <div className='bg-muted w-fit px-4 py-2 rounded-xl max-w-[70%]'>
                {text}
            </div>
        </div>
    )
}

export default ChatRequest