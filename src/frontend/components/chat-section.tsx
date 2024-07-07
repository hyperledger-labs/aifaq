import React from 'react'
import ChatRequest from './chat-request'
import ChatResponse from './chat-response'

type Props = {}

const ChatSection = (props: Props) => {
    return (
        <div className='flex flex-col max-w-3xl mx-auto w-full p-4 space-y-4'>
            <ChatRequest text='What are the Hyperledger Fabric WSL2 install instructions?' />
            <ChatResponse text='Both the Fabric documentation and Fabric samples rely heavily on a bash environment. The recommended path is to use WSL2 (Windows Subsystem for Linux version 2) to provide a native Linux environment and then you can follow the Linux prerequisites section (excluding the Linux Docker prerequisite as you already have Docker Desktop) and install them into your WSL2 linux distribution. WSL2 may not be installed by default; you can check and install WSL2 by going into “Programs and Features”, clicking on “Turn Windows features on or off” and ensuring that both “Windows Subsystem For Linux” and “Virtual Machine Platform” are selected. Next you will need to install a Linux distribution such as Ubuntu-20.04 and make sure it’s set to using version 2 of WSL. Refer to Install WSL for more information. Finally, you need to ensure Docker Desktop has integration enabled for your distribution so it can interact with Docker elements, such as a bash command window. To do this, open the Docker Desktop gui and go into settings, select Resources and them WSL Integration and ensure the checkbox for enable integration is checked. You should then see your WSL2 linux distribution listed (if you don’t then it is probably because it is still a WSL1 distribution and needs to be converted to WSL2) and you can then toggle the switch to enable integration for that distro. Refer to Docker Desktop WSL2 backend for more information' />
        </div>
    )
}

export default ChatSection