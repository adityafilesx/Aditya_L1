# 11. Frontend Component Guide

This document lists the core reusable UI components, their props, dependencies, and expected rendering behavior.

---

## 🎴 Common Cards & Controls

### 1. `KpiCard`
*   **Location**: `src/components/common/cards/KpiCard/KpiCard.tsx`
*   **Props**:
    ```typescript
    interface KpiCardProps {
      title: string;
      value: string | number;
      subtitle?: string;
      icon?: string;
      trend?: 'up' | 'down' | 'neutral';
      status?: 'success' | 'warning' | 'danger' | 'info';
      loading?: boolean;
    }
    ```
*   **Usage**: Displays single high-level values like current solar flux or active region count with status-colored glows.

---

## 📈 Charts & Spectrums

### 2. `PlotlyContainer`
*   **Location**: `src/design-system/components/charts/PlotlyContainer.tsx`
*   **Props**:
    ```typescript
    interface PlotlyContainerProps {
      data: Plotly.Data[];
      layout: Partial<Plotly.Layout>;
      config?: Partial<Plotly.Config>;
      className?: string;
    }
    ```
*   **Usage**: Renders responsive Plotly line and density charts. Wraps raw Plotly dependencies to manage window resize triggers and avoid redraw leaks.

---

## ⏱️ Mission Timelines & Scrubber

### 3. `MissionTimeline`
*   **Location**: `src/design-system/components/MissionTimeline.tsx`
*   **Props**:
    ```typescript
    interface MissionTimelineProps {
      className?: string;
    }
    ```
*   **Behavior**: Reads coordinates from the historical database and maps them as clickable dots on a temporal timeline. Clicking a dot initiates the Replay Engine, loading that historical period into `useStreamStore`.

---

## 🌞 3D twin canvas

### 4. `SolarSphere`
*   **Location**: `src/features/digital-twin/components/SolarSphere.tsx`
*   **Props**:
    ```typescript
    interface SolarSphereProps {
      activeLayer: 'photosphere' | 'magnetogram' | 'corona';
    }
    ```
*   **Usage**: Employs standard Three.js materials to map textures onto a sphere representing the Sun. Includes rotation matrices simulating the 27-day solar synodic rotation period.

---

## 🕸️ React Flow networks

### 5. `KnowledgeGraphWorkspace`
*   **Location**: `src/features/knowledge-graph/components/KnowledgeGraphWorkspace.tsx`
*   **Usage**: Uses `@xyflow/react` (React Flow) to display nodes representing flares, active regions, and spacecraft payloads. Implements customized node components that show active statuses or link structures.
*   **Dependencies**: `@xyflow/react`, `d3-force` (for automatic layouting).
