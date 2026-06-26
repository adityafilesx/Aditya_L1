export const ANIMATIONS = {
  transitions: {
    default: 'transition-all duration-150 ease-in-out',
    fast: 'transition-all duration-100 ease-in-out',
    slow: 'transition-all duration-300 ease-in-out',
  },
  classes: {
    blink: 'blink',
    liveDot: 'live-dot',
    telemetryBlink: 'telemetry-blink',
    pulse: 'animate-pulse',
    spin: 'animate-spin',
  },
} as const;
