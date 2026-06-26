# Aditya-L1 Mission Control — Design System

## Overview

The Aditya-L1 Mission Control frontend architecture implements a comprehensive design system optimized for scientific operations and mission-critical telemetry monitoring. It draws inspiration from NASA Mission Control, ESA Operations, Palantir Gotham, and Bloomberg Terminals.

The primary directive is **Situational Awareness**: an operator should understand mission status within 5 seconds.

## Architecture

The frontend is built on Streamlit but strictly abstracts away default Streamlit behaviors to create a consistent, customized, and responsive interface.

### Theming System (`ui/theme.py`)

A centralized theming engine manages colors across the application, bypassing Streamlit's default theme engine to ensure that standard components and custom HTML/CSS components always match.

- **Theme Engine**: `get_theme()` resolves the active theme.
- **Palette Modules**: `ui/colors.py` defines semantic color mappings (e.g., `background`, `card`, `primary`, `danger`, `telemetry`, `physics`).

### Spacing and Radius (`ui/spacing.py`)

Hardcoded pixel values are prohibited. The design system uses predefined spacing variables to ensure visual consistency:

- `SPACING`: Scale from `xxs` (4px) to `xxxl` (48px).
- `RADIUS`: Scale from `none` (0px) to `pill` (9999px).
- `SHADOWS`: Consistent elevation settings (`card`, `floating`, `dropdown`).

## Component Library

### Layout & Structural Components

- `page_config`: Global initialization (must be called first).
- `mission_layout`: Context manager defining the central layout width and containment.
- `render_header`: Standardized page headers with badges.
- `section_header`: Used to divide content logically with an icon and description.
- `spacer`: Replaces empty `st.write("")` for vertical margins.
- `divider`: Replaces `st.markdown("---")` with a custom-styled border line.

### Cards

The primary unit of data display is the Card. The library provides several variants in `ui/components/cards/`:

- **Metric Card**: For primary KPIs (e.g., SoLEXS Flux, Flare Probability). Supports sparklines and delta indicators.
- **Mission Card**: High-level mission status, payload health, and orbital data.
- **Risk Card**: Dedicated visual styling for space weather alerts (e.g., HF Blackout risks).
- **Telemetry Card**: Fast-updating sensor data readouts.
- **Sensor/Health Cards**: Sub-system diagnostics.
- **Base Card**: A highly configurable container for custom content, supporting `accent_border` and loading states.

### Status Indicators

Found in `ui/components/indicators/`:

- **Badges**: Small pill-shaped tags (e.g., `LIVE`, `WARNING`, `OFFLINE`). Colors map automatically to the semantic state.
- **Status Dots**: Blinking or static indicator lights next to component labels.
- **Status Bars**: Horizontal progress indicators for confidence scores or data quality.

### Alerts (`ui/components/alerts/`)

Mission-grade alert banners capable of rendering different severity levels, used to notify operators of imminent flares or system anomalies.

### Charts (`ui/components/charts/`)

All visualizations are rendered using Plotly with centralized templating:

- `register_templates()`: Registers the "mission_dark" template with Plotly.
- `render_chart_card()`: Wraps a Plotly figure in a standard mission card layout, complete with headers and contextual badges.
- Do NOT use `st.line_chart` or `st.bar_chart`.

### Timeline & Gauges

- **Timeline**: A vertical event sequence to map flare progression or operational schedules (`ui/components/timeline/`).
- **Gauges**: Plotly angular gauges and CSS-based mini gauges for quick threshold monitoring (`ui/components/gauges/`).

## Dynamic Routing (`ui/app.py`)

The application avoids standard Streamlit multi-page routing in favor of a dynamic Single Page Application (SPA) architecture.

- The `app.py` script acts as the entry point.
- It instantiates the sidebar (`ui/components/navigation/sidebar.py`).
- Based on the selected active page stored in `st.session_state`, it dynamically invokes the corresponding render function (e.g., `render_mission_overview()` or `render_showcase()`).

This prevents full page reloads, keeps state intact, and allows smooth transitions between domains.
