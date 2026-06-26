export function cn(...inputs: Array<string | false | null | undefined>): string {
  return inputs.filter(Boolean).join(' ');
}

export function stripLayoutChrome(html: string): string {
  return html
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/\sstyle="[^"]*"/gi, '')
    .trim();
}
