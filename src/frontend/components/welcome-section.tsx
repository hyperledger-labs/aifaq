import React from 'react'
import { IconHyperledger } from './icons/IconHyperledger'

type Props = {}

const WelcomeSection = (props: Props) => {
    return (
        <div className="flex h-full flex-col items-center justify-center text-primary space-y-2">
            <IconHyperledger className="w-16 h-16 fill-primary shrink-0" />
        </div>
    )
}

export default WelcomeSection