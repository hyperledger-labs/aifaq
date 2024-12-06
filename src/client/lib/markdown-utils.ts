// lib/markdown-utils.ts
export const processInlineMarkdown = (text: string): string => {
    // Bold
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Italic
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    // Inline Code
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    // Links
    text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
    // Strikethrough
    text = text.replace(/~~(.*?)~~/g, '<del>$1</del>');
    // Highlight
    text = text.replace(/==(.*?)==/g, '<mark>$1</mark>');
    // Subscript
    text = text.replace(/~(.*?)~/g, '<sub>$1</sub>');
    // Superscript
    text = text.replace(/\^(.*?)\^/g, '<sup>$1</sup>');
    // Keyboard
    text = text.replace(/<kbd>(.*?)<\/kbd>/g, '<kbd>$1</kbd>');
  
    return text;
  };
  
  export const parseTableRow = (row: string): string[] => {
    return row
      .split('|')
      .filter(cell => cell.trim() !== '')
      .map(cell => cell.trim());
  };
  
  export const isTableDelimiterRow = (row: string): boolean => {
    return row.includes('|') && row.replace(/[\s-:|]/g, '').length === 0;
  };