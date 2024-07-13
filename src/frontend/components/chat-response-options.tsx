"use client"
import React from 'react'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from './ui/dropdown-menu'
import { ThumbsUp, ThumbsDown, Share2, EllipsisVertical, Copy, Flag } from 'lucide-react'
import { Button } from './ui/button'
import { ResponsiveDialog } from './responsive-dialog'

type Props = {
    text: string
}

const ChatResponseOptions = ({ text }: Props) => {
    return (
        <div className='flex flex-row space-x-1'>
            <Button variant='highlight' size='icon' className='h-6 w-6'>
                <ThumbsUp />
            </Button>
            <Button variant='highlight' size='icon' className='h-6 w-6'>
                <ThumbsDown />
            </Button>
            <ResponsiveDialog
                description={"Share this chat."}
                title={"Share"}
                trigger={<Button variant='highlight' size='icon' className='h-6 w-6'><Share2 /></Button>}
            >
                <div>Share this post</div>
            </ResponsiveDialog>
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button variant='highlight' size='icon' className='h-6 w-6'>
                        <EllipsisVertical />
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent side='top'>
                    <DropdownMenuItem className='flex flex-row items-center gap-2' onSelect={() => navigator.clipboard.writeText(text)}>
                        <Copy className='h-4 w-4' />
                        <span>Copy</span>
                    </DropdownMenuItem>
                    <DropdownMenuItem className='flex flex-row items-center gap-2'>
                        <Flag className='h-4 w-4' />
                        <span>Report</span>
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
        </div>
    )
}

export default ChatResponseOptions