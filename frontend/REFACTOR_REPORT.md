# Phase FE-1 Refactor Report

**Project:** Aditya-L1 Mission Control Shell  
**Date:** June 25, 2026  
**Scope:** Enterprise frontend architecture refactor (no UI redesign, no API wiring)

---

## Executive Summary

The Google Stitch export (14 standalone HTML files, ~6,700 lines) was transformed into a **React 19 + TypeScript + Vite** single-page application with standardized folder structure, shared layout components, consolidated design tokens, path aliases, barrel exports, and client-side routing.

**Build status:** ✅ `npm run build` passes  
**Visual fidelity:** Preserved — page content converted from original HTML `<main>` sections

---

## 1. Source Analysis

### Original Structure (Removed from Root)

| Folder | Lines | Purpose |
|--------|-------|---------|
| `aditya_l1_mission_control_shell` | 357 | App shell / router host |
| `aditya_l1_integrated_mission_control_platform` | 452 | Platform with search/filters |
| `aditya_l1_mission_overview_dashboard` | 636 | Executive dashboard |
| `aditya_l1_operations_center` | 683 | Real-time telemetry ops |
| `mission_intelligence_space_weather_operations_center` | 508 | Space weather intelligence |
| `ai_intelligence_workspace` | 610 | AI model workspace |
| `aditya_l1_physics_laboratory` | 368 | Physics lab |
| `aditya_l1_digital_twin_center` | 493 | Digital twin viewer |
| `aditya_l1_knowledge_graph_intelligence_center` | 611 | Knowledge graph |
| `aditya_l1_mission_collaboration_replay_reporting_center` | 535 | Collaboration/replay |
| `aditya_l1_research_benchmarking_publication_workspace` | 235 | Research workspace |
| `platform_administration_infrastructure_console` | 370 | Admin console |
| `mission_control_design_system` | 567 | Design system docs |
| `three.js` | 105 | WebGL solar embed |

All moved to **`stitch-export/`** for reference.

### Duplication Identified

| Duplicated Element | Occurrences | Resolution |
|-------------------|-------------|------------|
| Tailwind config block (colors, fonts, spacing) | 14× | Single `tailwind.config.js` |
| Material Symbols font link | 14× (2× per file) | Single link in `index.html` |
| Google Fonts link | 14× | Single link in `index.html` |
| `.material-symbols-outlined` CSS | 14× | `src/styles/index.css` |
| `.bento-card` / `.glass-card` / card shadows | 8× | Unified in `index.css` |
| Dark sidebar navigation | 6× | `Sidebar` component |
| Top nav with UTC/MET clocks | 5× | `Toolbar` component |
| Bottom status footer | 7× | `Footer` component |
| Commander avatar URL | 10× | `@assets/images/commanderAvatar` |
| Inline `style=""` attributes | 40+ | Removed; replaced with CSS classes |
| Duplicate Material Symbols `<link>` | 14× | Deduplicated to 1 |

---

## 2. New Architecture

### Folder Structure Created

```
src/
├── app/                    ✅ AppProviders, AppRouter, routes
├── components/
│   ├── common/             ✅ Icon, StatusBadge, KpiCard
│   ├── layout/             ✅ Layout, Header, Sidebar, Toolbar, Footer
│   ├── cards/              📁 Reserved (KpiCard in common/cards)
│   ├── charts/             📁 Reserved for chart components
│   ├── tables/             📁 Reserved for table components
│   ├── forms/              📁 Reserved for form components
│   ├── navigation/         📁 Reserved
│   └── dialogs/            📁 Reserved
├── features/
│   ├── mission/            ✅ 6 pages
│   ├── ai/                 ✅ AiWorkspacePage
│   ├── physics/            ✅ PhysicsLabPage
│   ├── digital-twin/       ✅ DigitalTwinPage, ThreeJsViewerPage
│   ├── knowledge-graph/    ✅ KnowledgeGraphPage
│   ├── research/           ✅ ResearchPage
│   └── admin/              ✅ AdminPage, DesignSystemPage
├── hooks/                  ✅ useUtcClock, usePressScale
├── contexts/               📁 Stub (future providers)
├── store/                  📁 Stub (future state)
├── services/               📁 Stub (future API)
├── utils/                  ✅ cn()
├── types/                  ✅ Layout, navigation types
├── constants/              ✅ App metadata, navigation, routes
├── styles/                 ✅ Global CSS + Tailwind
└── assets/
    ├── images/             ✅ Consolidated URLs + reference screenshots
    └── fonts/              ✅ Font documentation
```

### Path Aliases Configured

Configured in both `vite.config.ts` and `tsconfig.app.json`:

`@`, `@app`, `@components`, `@features`, `@hooks`, `@contexts`, `@store`, `@services`, `@utils`, `@constants`, `@styles`, `@assets`, `@app-types`

> Note: `@types` alias avoided to prevent conflict with npm `@types/*` packages. Uses `@app-types` instead.

---

## 3. Shared Components Extracted

### Layout (`src/components/layout/`)

| Component | Source | Lines | Description |
|-----------|--------|-------|-------------|
| **Layout** | `mission_control_shell` | ~35 | Composes Sidebar + Toolbar + main canvas + Footer |
| **Sidebar** | `mission_control_shell` | ~75 | 260px dark nav with 6 grouped sections, active route highlighting |
| **Toolbar** | `mission_control_shell` | ~85 | Nav pills, UTC clock (live), MET, Live badge, notifications, user avatar |
| **Footer** | `mission_control_shell` | ~35 | Status, connectivity, station ID, copyright |
| **Header** | `mission_overview_dashboard` | ~55 | Dashboard-variant fixed top bar (reusable) |

### Common (`src/components/common/`)

| Component | Description |
|-----------|-------------|
| **Icon** | Wrapper for Material Symbols Outlined with filled/size variants |
| **StatusBadge** | Severity-colored status chips (success/warning/critical/info) |
| **KpiCard** | Reusable metric card matching bento-card design |

---

## 4. Page Conversions

Each Stitch HTML page → React feature page via `scripts/convert-html-pages.mjs`:

| Feature Page | Route | Layout | Content Lines |
|-------------|-------|--------|---------------|
| `ShellPage` | `/` | Shell | Hand-crafted placeholder |
| `PlatformPage` | `/operations/nowcasting` | Shell | 30 |
| `OverviewPage` | `/overview` | Shell | 424 |
| `OperationsPage` | `/operations` | Shell | 456 |
| `IntelligencePage` | `/intelligence` | Shell | 251 |
| `AiWorkspacePage` | `/investigation/ai` | Shell | 392 |
| `PhysicsLabPage` | `/investigation/physics` | Shell | 191 |
| `DigitalTwinPage` | `/digital-twin` | Shell | 243 |
| `ThreeJsViewerPage` | `/digital-twin/viewer` | Standalone | Hand-crafted React + Three.js |
| `KnowledgeGraphPage` | `/knowledge/graph` | Shell | 365 |
| `CollaborationPage` | `/reports/collaboration` | Shell | 329 |
| `ResearchPage` | `/knowledge/research` | Shell | 41 |
| `AdminPage` | `/system/admin` | Shell | 113 |
| `DesignSystemPage` | `/docs/design` | Shell | 338 |

**Conversion process:**
1. Extract `<main>` content (strip duplicated layout chrome)
2. Remove `<script>`, `<style>`, inline styles, duplicate font links
3. Transform HTML → JSX (`class` → `className`, SVG attrs camelCase)
4. Escape LaTeX/special characters for JSX validity
5. Wrap in scrollable page container

---

## 5. CSS Consolidation

### Removed (from 14 HTML files)

- 14× embedded `<style>` blocks (~800 lines total)
- 14× inline Tailwind CDN config scripts (~1,400 lines)
- 40+ inline `style=""` attributes
- Duplicate `@keyframes` definitions (blinker, pulse, blink)

### Centralized in `src/styles/index.css`

| Class | Purpose |
|-------|---------|
| `.material-symbols-outlined` | Icon font settings |
| `.active-sidebar-item` | Active nav state |
| `.sidebar-item-hover` | Nav hover state |
| `.custom-shadow` / `.shadow-card` | Card elevation |
| `.bento-card` / `.glass-card` / `.glass-panel` / `.lab-card` | Card variants |
| `.telemetry-table` | Data table styling |
| `.data-value` / `.unit-label` | Telemetry typography |
| `.blink` / `.live-dot` / `.blinking-dot` / `.status-dot-pulse` | Status animations |
| `.grid-bg` | Replay workspace grid |
| `.skeleton` | Loading placeholders |
| `.custom-scrollbar` / `.hide-scrollbar` | Scrollbar utilities |

### Tailwind Config

Single `tailwind.config.js` with all MD3 color tokens, typography scales, spacing tokens, and semantic colors (`success`, `warning`, `critical`) from DESIGN.md.

---

## 6. Assets Organization

### Images (`src/assets/images/`)

| Asset | Action |
|-------|--------|
| Commander avatars (10 URLs) | Consolidated into `index.ts` constants |
| Mission patch, solar surface, etc. | Named exports, single source |
| `screen.png` (13 files) | Copied to `assets/images/reference/` for visual regression reference |

### Icons

All icons use **Material Symbols Outlined** via the shared `Icon` component. No scattered SVG files — icons referenced by name string (e.g., `dashboard`, `wb_sunny`).

### Fonts (`src/assets/fonts/`)

Documented in `index.ts`. Loaded once via Google Fonts CDN in `index.html`:
- Inter, Space Grotesk, JetBrains Mono, Material Symbols

### SVG

- `public/favicon.svg` — app favicon (new, minimal)
- Inline SVGs from pages preserved in converted JSX (knowledge graph, charts)

---

## 7. Dead Code & Unused Assets Removed

| Item | Action |
|------|--------|
| Duplicate Material Symbols `<link>` (2nd copy per file) | Removed |
| Inline `<script>` blocks (clocks, micro-interactions) | Replaced with `useUtcClock` hook |
| Tailwind CDN `<script>` tags | Replaced with build-time Tailwind |
| `screen.png` at module roots | Moved to `assets/images/reference/` |
| Empty canvas placeholder HTML | Replaced with `ShellPage` component |

**Not removed:** `stitch-export/` preserved as source-of-truth reference.

---

## 8. Barrel Exports Created

| Path | Exports |
|------|---------|
| `src/app/index.ts` | AppProviders, AppRouter |
| `src/components/index.ts` | layout + common |
| `src/components/layout/index.ts` | Layout, Header, Sidebar, Toolbar, Footer |
| `src/components/common/index.ts` | Icon, StatusBadge, KpiCard |
| `src/features/index.ts` | All feature pages |
| `src/features/{domain}/index.ts` | Domain-specific pages |
| `src/hooks/index.ts` | useUtcClock, usePressScale |
| `src/constants/index.ts` | App + navigation constants |
| `src/types/index.ts` | Shared types |
| `src/utils/index.ts` | cn, stripLayoutChrome |
| `src/assets/index.ts` | Image URLs |

---

## 9. Component Size Analysis

| File | Lines | Status |
|------|-------|--------|
| `OperationsPage.tsx` | 456 | ⚠️ Exceeds 300 — candidate for Phase FE-2 split |
| `OverviewPage.tsx` | 424 | ⚠️ Exceeds 300 — candidate for Phase FE-2 split |
| `AiWorkspacePage.tsx` | 392 | ⚠️ Exceeds 300 — candidate for Phase FE-2 split |
| `KnowledgeGraphPage.tsx` | 365 | ⚠️ Exceeds 300 — candidate for Phase FE-2 split |
| `DesignSystemPage.tsx` | 338 | ⚠️ Exceeds 300 — acceptable (reference docs) |
| `CollaborationPage.tsx` | 329 | ⚠️ Exceeds 300 — candidate for Phase FE-2 split |
| `IntelligencePage.tsx` | 251 | ✅ Under 300 |
| `DigitalTwinPage.tsx` | 243 | ✅ Under 300 |
| `PhysicsLabPage.tsx` | 191 | ✅ Under 300 |
| All layout components | < 90 | ✅ Under 300 |

> Large pages retain original Stitch markup density. Further splitting into domain sub-components (e.g., `ExecutiveKpiGrid`, `TelemetryCharts`) is recommended in Phase FE-2.

---

## 10. Routing

React Router 7 with lazy-loaded feature pages:

- Shell routes wrap content in shared `Layout`
- Standalone route for Three.js viewer (no shell chrome)
- Catch-all redirects to `/`
- Sidebar uses `NavLink` with active state matching

---

## 11. What Was NOT Changed

- ❌ No visual redesign
- ❌ No backend API connections
- ❌ No new UI features
- ❌ No changes to color values, typography, or spacing
- ❌ No changes to page content/layout within the main canvas

---

## 12. Files Added

| Category | Count |
|----------|-------|
| Config (package.json, vite, tsconfig, tailwind, postcss) | 7 |
| App shell (main, routes, providers) | 3 |
| Layout components | 5 |
| Common components | 3 |
| Feature pages | 14 |
| Hooks | 1 |
| Constants/types/utils | 6 |
| Styles | 1 |
| Assets | 2 |
| Scripts | 1 |
| Documentation | 2 |
| **Total new source files** | **~45** |

---

## 13. Recommended Next Steps (Phase FE-2)

1. Split large feature pages into domain sub-components under `features/{domain}/components/`
2. Extract repeated patterns (TelemetryTable, TerminalLog, PlaybackScrubber) into `components/`
3. Wire `@services/` with API clients when backend is ready
4. Add `@store/` (Zustand) for shared telemetry state
5. Replace remote Google CDN image URLs with local assets
6. Add visual regression tests against `assets/images/reference/` screenshots
7. Code-split Three.js into async chunk (currently 510 kB)

---

## 14. Verification

```bash
npm install     # ✅ 251 packages
npm run build   # ✅ TypeScript + Vite build passes
npm run dev     # ✅ Dev server starts on :5173
```

All 14 routes accessible via sidebar navigation. UTC clock updates live via `useUtcClock` hook.
