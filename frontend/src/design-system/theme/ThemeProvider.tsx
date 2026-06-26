import React, { createContext, useState, useEffect, useCallback } from 'react';

export type ThemeMode = 'light' | 'dark' | 'high-contrast';

export interface ThemeContextValue {
  theme: ThemeMode;
  setTheme: (mode: ThemeMode) => void;
  toggleTheme: () => void;
}

const STORAGE_KEY = 'aditya-l1-theme';
const THEME_CYCLE: ThemeMode[] = ['light', 'dark', 'high-contrast'];

export const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

function getInitialTheme(): ThemeMode {
  if (typeof window === 'undefined') return 'light';

  // 1. Check localStorage
  const stored = localStorage.getItem(STORAGE_KEY) as ThemeMode | null;
  if (stored && THEME_CYCLE.includes(stored)) return stored;

  // 2. Default to light (matches current production appearance)
  return 'light';
}

function applyTheme(mode: ThemeMode) {
  const root = document.documentElement;
  root.setAttribute('data-theme', mode);

  // Sync localStorage
  try {
    localStorage.setItem(STORAGE_KEY, mode);
  } catch {
    // localStorage might be unavailable in incognito
  }
}

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setThemeState] = useState<ThemeMode>(getInitialTheme);

  // Apply on mount and whenever theme changes
  useEffect(() => {
    applyTheme(theme);
  }, [theme]);

  const setTheme = useCallback((mode: ThemeMode) => {
    setThemeState(mode);
  }, []);

  const toggleTheme = useCallback(() => {
    setThemeState((prev) => {
      const idx = THEME_CYCLE.indexOf(prev);
      return THEME_CYCLE[(idx + 1) % THEME_CYCLE.length];
    });
  }, []);

  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
