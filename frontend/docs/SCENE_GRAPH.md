# Digital Twin Scene Graph

## Hierarchy Map

```
TwinCanvas (R3F Context)
│
├── AmbientLight (Base lighting)
├── PointLight (Directional intensity)
├── Environment (HDRI lighting for PBR accuracy)
│
├── CameraControls (Drei OrbitControls hooked to Zustand for programmatic focusing)
│
├── SolarSphere (Group)
│   ├── Sphere (Photosphere, radius: 2.00, Material: MeshPhong)
│   ├── Sphere (Corona, radius: 2.08, Material: Additive Blending Basic)
│   └── Sphere (Magnetic Grid, radius: 2.01, Wireframe Basic)
│
└── ActiveRegions3D (Group)
    ├── [AR Loop]
    │   ├── Mesh (Anchor dot, SphereGeometry)
    │   └── Html (Drei UI Overlay projected to 2D)
    │       └── Inspector Tooltip (Probability, Risk, IDs)
```

## Render Optimizations
1. **Instancing**: Active regions use lightweight spheres. Future builds scaling to hundreds of magnetic loop arcs will utilize `InstancedMesh`.
2. **Material Re-use**: Materials inside `SolarSphere` utilize `<animated.material>` from React Spring, avoiding complete reallocation on parameter changes.
