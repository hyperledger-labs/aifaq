import React from 'react'
import UserDropdown from './user-dropdown'

type Props = {}

const ChatHeader = (props: Props) => {
    return (
        <div className="flex flex-row h-12 flex-shrink-0 px-2 py-1 items-center justify-between">
            <span className='text-2xl font-bold font-primary select-none'>AIFAQ</span>
            <UserDropdown />
        </div>
    )
}

export default ChatHeader