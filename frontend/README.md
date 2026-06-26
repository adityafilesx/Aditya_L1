# Aditya-L1 Mission Control Platform

Production-ready React architecture for the ISRO Aditya-L1 mission control interface, refactored from Google Stitch HTML exports.

## Stack

- **React 19** + **TypeScript**
- **Vite 6** (build tooling)
- **React Router 7** (client routing)
- **Tailwind CSS 3** (design tokens from Mission Control Precision System)
- **Three.js** (Digital Twin solar viewer)

## Quick Start

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # production build → dist/
npm run preview  # preview production build
```

## Architecture

```
src/
├── app/                 # Router, providers, app shell
├── components/
│   ├── common/          # Icon, StatusBadge, KpiCard
│   └── layout/          # Layout, Header, Sidebar, Toolbar, Footer
├── features/            # Domain pages (mission, ai, physics, etc.)
├── hooks/               # useUtcClock, usePressScale
├── contexts/            # Reserved for global React context
├── store/               # Reserved for client state
├── services/            # Reserved for API clients (not wired in FE-1)
├── utils/               # cn(), helpers
├── types/               # Shared TypeScript types
├── constants/           # Navigation, app metadata, routes
├── styles/              # Global CSS + Tailwind layers
└── assets/
    ├── images/          # Consolidated remote image URLs + reference screenshots
    └── fonts/           # Font documentation (loaded via CDN)
```

## Path Aliases

| Alias | Path |
|-------|------|
| `@/*` | `src/*` |
| `@app/*` | `src/app/*` |
| `@components/*` | `src/components/*` |
| `@features/*` | `src/features/*` |
| `@hooks/*` | `src/hooks/*` |
| `@constants/*` | `src/constants/*` |
| `@styles/*` | `src/styles/*` |
| `@assets/*` | `src/assets/*` |
| `@app-types/*` | `src/types/*` |

## Routes

| Path | Page |
|------|------|
| `/` | Mission Control Shell |
| `/overview` | Mission Overview Dashboard |
| `/operations` | Operations Center |
| `/operations/nowcasting` | Integrated Platform |
| `/intelligence` | Space Weather Intelligence |
| `/investigation/ai` | AI Intelligence Workspace |
| `/investigation/physics` | Physics Laboratory |
| `/digital-twin` | Digital Twin Center |
| `/digital-twin/viewer` | Three.js Solar Viewer |
| `/knowledge/graph` | Knowledge Graph |
| `/knowledge/research` | Research Workspace |
| `/reports/collaboration` | Collaboration & Replay |
| `/system/admin` | Platform Administration |
| `/docs/design` | Design System |

## Layout System

All operational pages share the **App Shell** layout:

- **Sidebar** — 260px dark navigation with grouped sections
- **Toolbar** — floating top bar with UTC/MET clocks, live badge, user menu
- **Footer** — bottom status strip with connectivity and station ID
- **Layout** — composes shell chrome; page content renders in the main canvas

Dashboard-variant pages from the Stitch export render their original `<main>` content inside the shared shell canvas to preserve visual fidelity without duplicating navigation chrome.

## Design Tokens

Centralized in `tailwind.config.js` and `src/styles/index.css`, sourced from `stitch-export/mission_control_precision_system/DESIGN.md`:

- MD3 color roles (primary, surface, error, etc.)
- Typography scales (display-lg, label-caps, data-mono)
- Spacing tokens (gutter, container-margin, section-gap)
- Shared component classes (bento-card, glass-card, telemetry-table)

## Legacy Export

Original Stitch HTML files are preserved in `stitch-export/` for reference. Re-convert with:

```bash
npm run convert:pages
```

## Constraints (Phase FE-1)

- No UI redesign — visual output matches Stitch exports
- No backend API integration
- No new features — architecture refactor only

See [REFACTOR_REPORT.md](./REFACTOR_REPORT.md) for the complete change log.
