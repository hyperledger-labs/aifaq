export interface Message {
    role: "user" | "assistant";
    content: string;
  }
  
  export type CodeBlockTheme = 'dark' | 'light' | 'dracula' | 'github' | 'monokai' | 'nord';