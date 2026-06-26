/**
 * Font families are loaded via Google Fonts in index.html:
 * - Inter (UI / body)
 * - Space Grotesk (telemetry / display)
 * - JetBrains Mono (logs / data)
 * - Material Symbols Outlined (icons)
 *
 * Tailwind font tokens: font-body-sm, font-display-lg, font-data-mono, etc.
 */
export const FONT_FAMILIES = {
  inter: 'Inter, sans-serif',
  spaceGrotesk: 'Space Grotesk, sans-serif',
  jetbrainsMono: 'JetBrains Mono, monospace',
} as const;
