"use client";

import { FormEvent, useState, useRef, useEffect } from "react";
import { Message } from "@/lib/types";
import ChatInput from "./chat-input";
import { MessageContent as ImportedMessageContent } from "./message-content";
import { cn } from "@/lib/utils";

function TypewriterText({ content, onComplete }: { content: string; onComplete?: () => void }) {
  const [displayedContent, setDisplayedContent] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (currentIndex < content.length) {
      const timer = setTimeout(() => {
        setDisplayedContent(prev => prev + content[currentIndex]);
        setCurrentIndex(prev => prev + 1);
      }, 1);

      return () => clearTimeout(timer);
    } else if (onComplete) {
      onComplete();
    }
  }, [content, currentIndex, onComplete]);

  return <LocalMessageContent content={displayedContent} />;
}

function LocalMessageContent({ content }: { content: string }) {
  const renderContent = () => {
    const parts = content.split(/(```[\s\S]*?```)/);
    
    return parts.map((part, index) => {
      // Handle code blocks
      if (part.startsWith('```')) {
        const match = part.match(/```(\w+)?\n([\s\S]*?)```/);
        if (match) {
          const [, language, code] = match;
          return (
            <div key={index} className="relative my-4 rounded-lg bg-zinc-950 text-zinc-50 overflow-x-auto">
              <div className="flex items-center justify-between px-4 py-2 border-b border-zinc-800">
                <span className="text-xs text-zinc-400">{language || 'text'}</span>
              </div>
              <pre className="p-4">
                <code className="text-sm font-mono">{code.trim()}</code>
              </pre>
            </div>
          );
        }
      }

      // Handle regular text
      const lines = part.split('\n');
      return (
        <div key={index} className="break-words">
          {lines.map((line, lineIndex) => {
            // Headers
            if (line.startsWith('### ')) {
              return (
                <h3 key={lineIndex} className="text-lg font-semibold mt-4 mb-2">
                  {line.slice(4)}
                </h3>
              );
            }

            // Regular text with formatting
            const formattedLine = line
              .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
              .replace(/\*(.*?)\*/g, '<em>$1</em>')
              .replace(/`([^`]+)`/g, '<code class="px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 font-mono text-sm">$1</code>');

            return formattedLine ? (
              <div
                key={lineIndex}
                className="mb-2 last:mb-0"
                dangerouslySetInnerHTML={{ __html: formattedLine }}
              />
            ) : (
              <div key={lineIndex} className="h-4" /> // Spacing for empty lines
            );
          })}
        </div>
      );
    });
  };

  return (
    <div className="space-y-1 leading-normal">
      {renderContent()}
    </div>
  );
}

export default function ChatSection() {
  const chatContainerRef = useRef<HTMLDivElement | null>(null);
  const [userMessage, setUserMessage] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTo({
        top: chatContainerRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages]);

  const handleSendMessage = async (e: FormEvent) => {
    e.preventDefault();

    if (!userMessage.trim() || isGenerating) return;

    const newMessage: Message = { role: "user", content: userMessage };
    setMessages(prev => [...prev, newMessage]);
    setUserMessage("");
    setIsGenerating(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL 
        ? `http://${process.env.NEXT_PUBLIC_API_URL}/query`
        : '/api/query';
        
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: userMessage }),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
      }

      const data = await response.json();
      const assistantResponse = data.msg?.answer || data.msg;

      if (assistantResponse) {
        setMessages(prev => [...prev, { role: "assistant", content: assistantResponse }]);
      }
    } catch (error) {
      console.error("API Error:", error);
      setMessages(prev => [
        ...prev,
        { 
          role: "assistant", 
          content: "I apologize, but I encountered an error processing your request. Please try again."
        },
      ]);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-950">
      <div ref={chatContainerRef} className="flex-1 overflow-y-auto scroll-smooth">
        <div className="max-w-2xl mx-auto px-4 py-6 space-y-6">
          {messages.map((message, index) => (
            <div
              key={index}
              className={cn("flex", message.role === "user" ? "justify-end" : "justify-start")}
            >
              <div
                className={cn(
                  "max-w-[85%] rounded-lg px-4 py-2 break-words",
                  message.role === "user" 
                    ? "bg-blue-100 text-white dark:bg-blue-500" 
                    : "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100"
                )}
              >
                <div className="prose prose-sm dark:prose-invert max-w-none">
                  {message.role === "assistant" && index === messages.length - 1 ? (
                    <TypewriterText 
                      content={message.content} 
                      onComplete={() => chatContainerRef.current?.scrollTo({
                        top: chatContainerRef.current.scrollHeight,
                        behavior: "smooth",
                      })}
                    />
                  ) : (
                    <ImportedMessageContent content={message.content} />
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="border-t dark:border-gray-800 bg-gradient-to-b from-transparent to-white dark:to-gray-950 pt-2">
        <div className="max-w-2xl mx-auto px-4">
          <ChatInput
            isDisabled={isGenerating}
            userMessage={userMessage}
            setUserMessage={setUserMessage}
            handleSendMessage={handleSendMessage}
          />
        </div>
      </div>
    </div>
  );
}