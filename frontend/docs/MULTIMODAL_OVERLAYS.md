# Multi-Modal Overlay Strategy

The Digital Twin is designed to merge distinct sensory inputs from the Aditya-L1 observatory and ground stations into a single spatial view.

## Core Modalities

1. **SoLEXS / HEL1OS (X-Ray Flux)**: Represented via dynamic heatmap textures projected onto the inner Photosphere layer or localized to specific AR anchors in the Scene Graph.
2. **SUIT (UV/EUV)**: Can be integrated as the diffuse texture map on the Chromosphere sphere.
3. **SWIS (Solar Wind)**: Rendered as vector fields or particle systems extending beyond the Corona radius.

## Overlay Implementation
Multi-modal inputs are typically provided as UV-mapped `.png` sequences or API telemetry vectors.
- **Textures**: `useLoader(TextureLoader, url)` is used inside R3F components to fetch spatial images.
- **Data Layers**: Layer states (e.g., `showPredictionLayer`, `magneticOpacity`) in `workspaceStore.ts` dictate which `<Sphere>` components are currently rendering in the GPU pipeline.

By combining layers using `AdditiveBlending`, multiple overlapping emission spectra can be viewed concurrently without Z-fighting or occlusion artifacts.
