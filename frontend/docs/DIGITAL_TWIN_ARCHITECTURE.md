# Digital Twin Architecture

## Overview
The Digital Twin subsystem acts as the interactive 3D visual hub for the Aditya-L1 Mission Control. Instead of relying on static plots or isolated web components, it uses WebGL via **React Three Fiber (R3F)** to render a multi-layered solar environment. It is fully synchronized with the mission state, including telemetry streams, X-Ray tracking, and AI predictions.

## Tech Stack
- **React Three Fiber (R3F)**: React wrapper over Three.js for declarative 3D.
- **Drei**: Core R3F helpers for environment, camera controls, HTML overlays, and performance.
- **Leva**: Lightweight GUI panel for operator overrides (e.g. layer opacities).
- **React Spring**: Used for smooth interpolation of opacity layers.
- **Zustand**: Provides the `workspaceStore` to ensure synchronized scrubbing with Plotly.

## State Strategy
The `TwinCanvas` is directly mounted within the `DigitalTwinPage` React tree, allowing it to hook into `useWorkspaceStore`.
- The Timeline component globally sets `globalCursorTime`.
- The `<SolarSphere>` component respects playback speeds through `useFrame()`.
- R3F `Html` overlays provide pixel-perfect HTML UI annotations projected into the 3D scene (Active Regions).

## Rendering Pipeline
1. `TwinCanvas` sets up lights, the `Environment` (image-based lighting), and `CameraControls` (`OrbitControls`).
2. `SolarSphere` draws concentric `Sphere` geometries utilizing additive blending to mimic the Photosphere, Corona, and Magnetic layers.
3. `ActiveRegions3D` converts Lat/Lon metadata into 3D Cartesian coordinates (`x, y, z`), rendering interactive anchor meshes that operators can click to Auto-Focus.
