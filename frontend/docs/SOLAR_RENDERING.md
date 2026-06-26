# Solar Rendering Strategies

## Layering System
The Solar Twin is rendered using multiple concentric spheres to represent distinct atmospheric structures. Since WebGL depth sorting is complex for nested transparent objects, we use specific material attributes:

### 1. Photosphere (Base)
- **Radius**: `2.00`
- **Material**: `MeshPhongMaterial` (lit by scene lights)
- **Opacity Strategy**: The base layer typically remains at `1.0` unless operators want to see through to internal physics layers.

### 2. Chromosphere / Corona
- **Radius**: `2.08`
- **Material**: `MeshBasicMaterial` (unlit, purely emissive)
- **Opacity Strategy**: Uses `AdditiveBlending` with `side: THREE.BackSide`. This creates a soft halo/glow effect without harsh geometry intersections when active region meshes penetrate the surface.

### 3. Magnetic / Physics Layers
- **Radius**: `2.01`
- **Material**: Wireframe or texture-mapped projections.
- **Opacity Strategy**: Animated smoothly via `React Spring` when triggered by Leva UI controls.

## Performance Profiling (60FPS)
- Uses `<PerformanceMonitor>` from Drei. If the framerate drops below 55 FPS, it triggers a warning. A future implementation could dynamically reduce `dpr` or texture resolution.
- The `useFrame` loop handles continuous rotation independently of React state, ensuring silky smooth planetary revolution.
