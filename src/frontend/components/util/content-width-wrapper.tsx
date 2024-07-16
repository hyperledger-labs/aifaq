import { cn } from '@/lib/utils'
import React from 'react'

type Props = {
    children: React.ReactNode,
    className?: string
}

const ContentWidthWrapper = ({ children, className }: Props) => {
    return (
        <div
            className={cn(
                'mx-auto w-full max-w-3xl px-4',
                className
            )}>
            {children}
        </div>
    )
}

export default ContentWidthWrapper