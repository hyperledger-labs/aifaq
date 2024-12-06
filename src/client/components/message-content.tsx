"use client";

import { useState } from "react";
import { Copy, Check } from "lucide-react";
import { Button } from "@/components/ui/button";

function CodeBlock({ language, code }: { language: string; code: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative my-4 rounded-lg bg-gray-950 text-gray-50">
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-800">
        <span className="text-xs text-gray-400">{language}</span>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleCopy}
          className="h-8 w-8 p-0 hover:bg-gray-800"
        >
          {copied ? (
            <Check className="h-4 w-4" />
          ) : (
            <Copy className="h-4 w-4" />
          )}
        </Button>
      </div>
      <pre className="p-4 overflow-x-auto">
        <code className="text-sm font-mono">{code}</code>
      </pre>
    </div>
  );
}

function MessageContent({ content }: { content: string }) {
  const renderContent = () => {
    const parts = content.split(/(```[\s\S]*?```)/);
    
    return parts.map((part, index) => {
      // Handle code blocks
      if (part.startsWith('```')) {
        const match = part.match(/```(\w+)?\n([\s\S]*?)```/);
        if (match) {
          const [, language, code] = match;
          return (
            <CodeBlock
              key={index}
              language={language || 'text'}
              code={code.trim()}
            />
          );
        }
      }

      // Handle regular text
      const lines = part.split('\n');
      return (
        <div key={index} className="break-words">
          {lines.map((line, lineIndex) => {
            // Handle Headings
            if (line.startsWith('## ')) {
              return (
                <h2 key={lineIndex} className="text-xl font-semibold mt-4 mb-2">
                  {line.slice(3)}
                </h2>
              );
            }
            if (line.startsWith('### ')) {
              return (
                <h3 key={lineIndex} className="text-lg font-semibold mt-3 mb-2">
                  {line.slice(4)}
                </h3>
              );
            }

            // Handle regular text with bold elements only
            let formattedText = line;
            // Only handle bold formatting with **
            formattedText = formattedText.replace(
              /\*\*(.*?)\*\*/g,
              '<strong>$1</strong>'
            );
            
            return formattedText ? (
              <div
                key={lineIndex}
                className="mb-2 last:mb-0"
                dangerouslySetInnerHTML={{ __html: formattedText }}
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

export { MessageContent };