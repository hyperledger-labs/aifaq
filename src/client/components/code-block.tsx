import { useState } from 'react';
import { Copy, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { CodeBlockTheme } from '@/lib/types';

interface CodeBlockProps {
  language: string;
  code: string;
  theme?: CodeBlockTheme;
}

export function CodeBlock({ language, code, theme = 'dark' }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  const themeClasses = {
    dark: "bg-gray-950 text-gray-50",
    light: "bg-gray-100 text-gray-900",
    dracula: "bg-[#282a36] text-[#f8f8f2]",
    github: "bg-white text-gray-800 dark:bg-gray-800 dark:text-gray-100",
    monokai: "bg-[#272822] text-[#f8f8f2]",
    nord: "bg-[#2e3440] text-[#d8dee9]"
  };

  return (
    <div className={cn(
      "relative my-4 rounded-lg overflow-hidden group",
      themeClasses[theme]
    )}>
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-700/50">
        <div className="flex items-center gap-2">
          <span className="text-xs opacity-70">{language}</span>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleCopy}
          className={cn(
            "h-8 px-3 flex items-center gap-1.5 text-xs font-medium transition-colors",
            "text-gray-400 hover:text-gray-100 hover:bg-gray-800",
            copied && "text-green-400"
          )}
        >
          {copied ? (
            <>
              <Check className="h-3.5 w-3.5" />
              <span>Copied!</span>
            </>
          ) : (
            <>
              <Copy className="h-3.5 w-3.5" />
              <span>Copy code</span>
            </>
          )}
        </Button>
      </div>
      <div className="relative">
        <pre className="p-4 overflow-x-auto">
          <code className="text-sm font-mono">{code}</code>
        </pre>
        {/* Floating copy button */}
        <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleCopy}
            className={cn(
              "h-8 w-8 p-0 bg-gray-800/50 hover:bg-gray-800",
              copied && "text-green-400"
            )}
          >
            {copied ? (
              <Check className="h-4 w-4" />
            ) : (
              <Copy className="h-4 w-4" />
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}