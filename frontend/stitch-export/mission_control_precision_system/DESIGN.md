---
name: Mission Control Precision System
colors:
  surface: '#f7f9fc'
  surface-dim: '#d8dadd'
  surface-bright: '#f7f9fc'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f7'
  surface-container: '#eceef1'
  surface-container-high: '#e6e8eb'
  surface-container-highest: '#e0e3e6'
  on-surface: '#191c1e'
  on-surface-variant: '#464555'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f4'
  outline: '#767586'
  outline-variant: '#c7c4d7'
  surface-tint: '#4949d9'
  primary: '#4140d1'
  on-primary: '#ffffff'
  primary-container: '#5b5ceb'
  on-primary-container: '#f5f2ff'
  inverse-primary: '#c1c1ff'
  secondary: '#ae3104'
  on-secondary: '#ffffff'
  secondary-container: '#fe693c'
  on-secondary-container: '#601600'
  tertiary: '#55575d'
  on-tertiary: '#ffffff'
  tertiary-container: '#6e6f75'
  on-tertiary-container: '#f3f3fa'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e1dfff'
  primary-fixed-dim: '#c1c1ff'
  on-primary-fixed: '#08006c'
  on-primary-fixed-variant: '#2f2bc1'
  secondary-fixed: '#ffdbd1'
  secondary-fixed-dim: '#ffb59f'
  on-secondary-fixed: '#3b0a00'
  on-secondary-fixed-variant: '#862200'
  tertiary-fixed: '#e2e2e9'
  tertiary-fixed-dim: '#c6c6cd'
  on-tertiary-fixed: '#1a1b21'
  on-tertiary-fixed-variant: '#45474c'
  background: '#f7f9fc'
  on-background: '#191c1e'
  surface-variant: '#e0e3e6'
typography:
  display-lg:
    fontFamily: Space Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  data-mono:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  numeric-telemetry:
    fontFamily: Space Grotesk
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 24px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-margin: 32px
  gutter: 24px
  section-gap: 48px
  component-padding-x: 16px
  component-padding-y: 12px
---

## Brand & Style

The design system is engineered for high-stakes aerospace telemetry and mission-critical decision-making. The aesthetic is rooted in **Modern Corporate Minimalism** with a focus on functional density and information clarity, drawing inspiration from high-performance engineering tools.

The visual narrative prioritizes utility over decoration. It employs a rigorous, structured layout that mimics the precision of flight instrumentation. Every element serves a purpose: heavy whitespace is used not just for aesthetics, but to prevent cognitive overload during complex data monitoring. The emotional response is one of reliability, absolute control, and scientific authority.

- **Style:** Minimalist, high-precision enterprise.
- **Visual Tenets:** Sharp edges, subtle depth, high information density, and a restricted decorative palette.
- **Animations:** Strictly functional. Use 150ms linear fades for state transitions only; avoid motion that does not communicate status change.

## Colors

The palette is designed for prolonged visual endurance and immediate error recognition. 

1.  **Surfaces:** The background uses a cool, neutral grey (`#F5F7FA`) to reduce screen glare. Primary workspaces (cards) are pure white for maximum contrast with data. The sidebar is deep charcoal (`#111318`), creating a clear structural anchor for navigation.
2.  **Accents:** Purple (`#5B5CEB`) denotes primary actions and active states. Orange (`#FF6A3D`) is reserved for trajectory data or secondary mission highlights.
3.  **Semantic Status:** Standardized colors for Success, Warning, Critical, and Info must be used consistently across all telemetry charts and status indicators to ensure zero ambiguity during mission anomalies.
4.  **Borders:** Use `#E8ECF2` for all structural divisions. Avoid shadows for separation; rely on these hairlines.

## Typography

This design system utilizes a tri-font strategy to differentiate between UI controls, quantitative data, and technical logs.

-   **UI & Interface (Inter):** Used for all navigational elements, body text, and structural labels. High legibility at small scales is required.
-   **Quantitative Data (Space Grotesk):** Applied to large numeric readouts, coordinates, and countdowns. Must use `tabular-nums` to ensure numbers do not "jump" as values change.
-   **Telemetry & Logs (JetBrains Mono):** Reserved for raw data streams, terminal outputs, and system logs. Monospacing ensures character alignment for quick scanning of vertical data columns.

## Layout & Spacing

The layout is based on a **12-column fluid grid** for the main content area, while the sidebar remains at a fixed width of 260px. 

-   **Outer Margins:** A strict 32px margin surrounds the entire viewport to ensure data is never "crowded" by the physical screen bezel.
-   **Internal Gutters:** 24px spacing between cards or data widgets provides clear visual breathing room.
-   **Density:** For telemetry tables, use a condensed 8px vertical padding to maximize the data-to-pixel ratio.
-   **Breakpoints:** On tablet and mobile, the 12-column grid collapses to 6 and 2 columns respectively. The sidebar transitions to a bottom-docked navigation bar or a hidden drawer on mobile devices.

## Elevation & Depth

Hierarchy is established through **Tonal Layering** and a single, highly refined shadow style.

1.  **The Base:** The neutral background (`#F5F7FA`) acts as the lowest layer.
2.  **The Surface:** All interactive widgets and data containers sit on white surfaces (`#FFFFFF`).
3.  **Shadows:** Use a single, extremely soft shadow for primary cards: `0 10px 30px rgba(15, 23, 42, 0.04)`. This creates a subtle "lift" from the background without feeling heavy or skeuomorphic.
4.  **Interaction:** On hover, do not increase shadow depth. Instead, change the border color from `#E8ECF2` to `#5B5CEB` (Primary Purple) at 1px thickness.

## Shapes

The shape language balances the friendliness of modern SaaS with the structural integrity of industrial tools.

-   **Cards/Containers:** Use an 18px radius to soften large information blocks and distinguish them from the background.
-   **Controls:** Buttons and input fields use an 8px radius. This "sharper" corner communicates precision and fits the technical nature of the mission control interface.
-   **Status Tags:** Use a 4px radius for small status chips to maintain a professional, compact appearance.

## Components

-   **Buttons:** Default state is solid background with white text. Ghost buttons use a 1px border (`#E8ECF2`) and primary text. 8px corner radius.
-   **Cards:** Pure white background, 18px radius, 1px border (`#E8ECF2`), and a soft shadow. Use for telemetry charts and data summaries.
-   **Input Fields:** 8px radius, 1px border. Focus state: border changes to `#5B5CEB` with a 2px outer glow of the same color at 10% opacity.
-   **Data Tables:** Headers in `label-caps` (Inter, uppercase). Rows should have a 1px bottom border. Alternate row striping is prohibited; use hover highlights instead.
-   **Status Badges:** Small, 4px rounded chips. Use semi-transparent versions of semantic colors (e.g., Success background at 10% opacity with solid green text).
-   **Telemetry Strips:** Horizontal components for real-time data using `data-mono` (JetBrains Mono). Include a small "live" indicator (blinking dot) for active streams.