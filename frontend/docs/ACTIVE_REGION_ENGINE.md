# Active Region Engine

## Spherical to Cartesian Conversion
Active regions (AR) provided by the backend use Heliographic latitude and longitude. To render these dynamically over a sphere in WebGL, we map them using spherical coordinates:

```javascript
const phi = (90 - region.lat) * (Math.PI / 180);
const theta = (region.lon + 90) * (Math.PI / 180);

const x = radius * Math.sin(phi) * Math.cos(theta);
const y = radius * Math.cos(phi);
const z = radius * Math.sin(phi) * Math.sin(theta);
```

## Interactivity and Zustand Integration
- **Pointer Events**: Meshes attached to `ActiveRegions3D` intercept `onClick`, `onPointerOver`, and `onPointerOut` directly.
- **State Selection**: Clicking an AR fires `setActiveRegion` on the `workspaceStore`.
- **UI Projections**: Using Drei's `<Html>` wrapper, standard React DOM components (like the Inspector Tooltips) are projected onto the WebGL canvas, anchored strictly to the `x, y, z` coordinates of the mesh.
- **Camera Auto-Focus**: When `workspaceStore.activeRegion` changes, `CameraControls.tsx` automatically computes the Cartesian coordinates of that region and interpolates the `OrbitControls` camera position to lock onto it.
