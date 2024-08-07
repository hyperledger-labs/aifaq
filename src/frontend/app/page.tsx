"use client";

import React, { useState } from 'react';
import Sidebar from "@/components/sidebar";
import ChatHeader from "@/components/chat-header";
import WelcomeSection from "@/components/welcome-section";
import ChatSection from "@/components/chat-section";
import ChatBottomBar from '@/components/chat-bottom-bar';

interface Message {
    request: string;
    response: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const chatSelected = false;

  const handleSend = (request: string) => {
    const response = 'Both the Fabric documentation and Fabric samples rely heavily on a bash environment. The recommended path is to use WSL2 (Windows Subsystem for Linux version 2) to provide a native Linux environment and then you can follow the Linux prerequisites section (excluding the Linux Docker prerequisite as you already have Docker Desktop) and install them into your WSL2 linux distribution. WSL2 may not be installed by default; you can check and install WSL2 by going into “Programs and Features”, clicking on “Turn Windows features on or off” and ensuring that both “Windows Subsystem For Linux” and “Virtual Machine Platform” are selected. Next you will need to install a Linux distribution such as Ubuntu-20.04 and make sure it’s set to using version 2 of WSL. Refer to Install WSL for more information. Finally, you need to ensure Docker Desktop has integration enabled for your distribution so it can interact with Docker elements, such as a bash command window. To do this, open the Docker Desktop gui and go into settings, select Resources and them WSL Integration and ensure the checkbox for enable integration is checked. You should then see your WSL2 linux distribution listed (if you don’t then it is probably because it is still a WSL1 distribution and needs to be converted to WSL2) and you can then toggle the switch to enable integration for that distro. Refer to Docker Desktop WSL2 backend for more information';
        // To-do: Error Handling
        // const response = await fetch('http://localhost:8080/chat', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({ message }),
        // });
        // const data = await response.json();
        // setMessages([...messages, { request: message, response: data.response }]);
        
    const newMessage = { request, response };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
  };

  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex flex-col flex-1">
        <ChatHeader />
        <div className="flex-1 overflow-y-auto bg-background">
          {chatSelected ? <WelcomeSection /> : <ChatSection messages={messages} />}
        </div>
        <div className='relative bottom-1 w-full flex justify-center'>
          <div className='max-w-3xl w-full p-4'>
            <ChatBottomBar onSend={handleSend} />
          </div>
        </div>
      </main>
    </div>
  );
}
