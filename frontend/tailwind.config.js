/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: ['selector', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        surface: 'rgb(var(--color-surface) / <alpha-value>)',
        'surface-dim': 'rgb(var(--color-surface-dim) / <alpha-value>)',
        'surface-bright': 'rgb(var(--color-surface-bright) / <alpha-value>)',
        'surface-container-lowest': 'rgb(var(--color-surface-container-lowest) / <alpha-value>)',
        'surface-container-low': 'rgb(var(--color-surface-container-low) / <alpha-value>)',
        'surface-container': 'rgb(var(--color-surface-container) / <alpha-value>)',
        'surface-container-high': 'rgb(var(--color-surface-container-high) / <alpha-value>)',
        'surface-container-highest': 'rgb(var(--color-surface-container-highest) / <alpha-value>)',
        'surface-variant': 'rgb(var(--color-surface-variant) / <alpha-value>)',
        'on-surface': 'rgb(var(--color-on-surface) / <alpha-value>)',
        'on-surface-variant': 'rgb(var(--color-on-surface-variant) / <alpha-value>)',
        outline: 'rgb(var(--color-outline) / <alpha-value>)',
        'outline-variant': 'rgb(var(--color-outline-variant) / <alpha-value>)',
        primary: 'rgb(var(--color-primary) / <alpha-value>)',
        'on-primary': 'rgb(var(--color-on-primary) / <alpha-value>)',
        success: 'rgb(var(--color-success) / <alpha-value>)',
        warning: 'rgb(var(--color-warning) / <alpha-value>)',
        critical: 'rgb(var(--color-critical) / <alpha-value>)',
        error: 'rgb(var(--color-error) / <alpha-value>)',
        'card-border': 'rgb(var(--color-card-border) / <alpha-value>)',
      },
      borderRadius: {
        card: 'var(--radius-card)',
        control: 'var(--radius-control)',
      },
      spacing: {
        'component-padding-y': 'var(--space-component-padding-y)',
        'container-margin': 'var(--space-container-margin)',
        'section-gap': 'var(--space-section-gap)',
        gutter: 'var(--space-gutter)',
        'component-padding-x': 'var(--space-component-padding-x)',
      },
      fontFamily: {
        'body': ['var(--font-body)', 'sans-serif'],
        'display': ['var(--font-display)', 'sans-serif'],
        'mono': ['var(--font-mono)', 'monospace'],
        // Legacy
        'body-sm': ['var(--font-body)', 'sans-serif'],
        'display-lg': ['var(--font-display)', 'sans-serif'],
        'headline-md': ['var(--font-body)', 'sans-serif'],
        'label-caps': ['var(--font-body)', 'sans-serif'],
        'numeric-telemetry': ['var(--font-display)', 'sans-serif'],
        'body-lg': ['var(--font-body)', 'sans-serif'],
        'data-mono': ['var(--font-mono)', 'monospace'],
      },
      fontSize: {
        // Phase 2 Typography Tiers
        'hero': ['var(--text-hero-size)', { lineHeight: 'var(--text-hero-leading)', fontWeight: 'var(--text-hero-weight)', letterSpacing: 'var(--text-hero-tracking)' }],
        'heading': ['var(--text-heading-size)', { lineHeight: 'var(--text-heading-leading)', fontWeight: 'var(--text-heading-weight)', letterSpacing: 'var(--text-heading-tracking)' }],
        'primary-metric': ['var(--text-primary-size)', { lineHeight: 'var(--text-primary-leading)', fontWeight: 'var(--text-primary-weight)', letterSpacing: 'var(--text-primary-tracking)' }],
        'label': ['var(--text-label-size)', { lineHeight: 'var(--text-label-leading)', fontWeight: 'var(--text-label-weight)', letterSpacing: 'var(--text-label-tracking)' }],
        
        // Legacy
        'body-sm': ['var(--text-body-sm-size)', { lineHeight: 'var(--text-body-sm-leading)', fontWeight: 'var(--text-body-sm-weight)' }],
        'display-lg': ['var(--text-display-lg-size)', { lineHeight: 'var(--text-display-lg-leading)', letterSpacing: 'var(--text-display-lg-tracking)', fontWeight: 'var(--text-display-lg-weight)' }],
        'headline-md': ['var(--text-headline-md-size)', { lineHeight: 'var(--text-headline-md-leading)', fontWeight: 'var(--text-headline-md-weight)' }],
        'label-caps': ['var(--text-label-caps-size)', { lineHeight: 'var(--text-label-caps-leading)', letterSpacing: 'var(--text-label-caps-tracking)', fontWeight: 'var(--text-label-caps-weight)' }],
        'numeric-telemetry': ['var(--text-numeric-size)', { lineHeight: 'var(--text-numeric-leading)', fontWeight: 'var(--text-numeric-weight)' }],
        'body-lg': ['var(--text-body-lg-size)', { lineHeight: 'var(--text-body-lg-leading)', fontWeight: 'var(--text-body-lg-weight)' }],
        'data-mono': ['var(--text-data-mono-size)', { lineHeight: 'var(--text-data-mono-leading)', fontWeight: 'var(--text-data-mono-weight)' }],
      },
      boxShadow: {
        card: 'var(--shadow-card)',
        overlay: 'var(--shadow-overlay)',
        focus: 'var(--shadow-focus)',
      },
    },
  },
  plugins: [],
};
