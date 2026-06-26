import { TOKENS } from '../tokens';

export type ThemeMode = 'dark' | 'light';

export const theme = {
  tokens: TOKENS,
  isDark: false, // Default is light as per current app style
};

export const getThemeColor = (colorName: keyof typeof TOKENS.colors) => {
  return TOKENS.colors[colorName];
};
