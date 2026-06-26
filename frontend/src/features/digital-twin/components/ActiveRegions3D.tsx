import React, { useMemo } from 'react';
import * as THREE from 'three';
import { Html } from '@react-three/drei';
import { useWorkspaceStore } from '../../../realtime/workspaceStore';

// Mock active regions for now
const REGIONS = [
  { id: 'AR13872', lat: 15, lon: -25, risk: 'high', flareProb: 85 },
  { id: 'AR13873', lat: -10, lon: 45, risk: 'mod', flareProb: 42 },
  { id: 'AR13874', lat: 22, lon: 10, risk: 'low', flareProb: 5 },
];

export const ActiveRegions3D: React.FC = () => {
  const focusedRegion = useWorkspaceStore(state => state.activeRegion);
  const setActiveRegion = useWorkspaceStore(state => state.setActiveRegion);

  const regionMeshes = useMemo(() => {
    return REGIONS.map((region) => {
      const phi = (90 - region.lat) * (Math.PI / 180);
      const theta = (region.lon + 90) * (Math.PI / 180);
      
      const r = 2.05; // slightly above photosphere
      const x = r * Math.sin(phi) * Math.cos(theta);
      const y = r * Math.cos(phi);
      const z = r * Math.sin(phi) * Math.sin(theta);
      
      return { ...region, position: new THREE.Vector3(x, y, z) };
    });
  }, []);

  return (
    <group>
      {regionMeshes.map((region) => {
        const isSelected = focusedRegion?.id === region.id;
        const color = region.risk === 'high' ? '#ff3b30' : region.risk === 'mod' ? '#ff9500' : '#34c759';

        return (
          <group key={region.id} position={region.position}>
            {/* 3D Marker */}
            <mesh 
              onClick={(e) => {
                e.stopPropagation();
                setActiveRegion({ id: region.id, lat: region.lat, lon: region.lon });
              }}
              onPointerOver={() => document.body.style.cursor = 'pointer'}
              onPointerOut={() => document.body.style.cursor = 'auto'}
            >
              <sphereGeometry args={[isSelected ? 0.08 : 0.05, 16, 16]} />
              <meshBasicMaterial color={color} transparent opacity={0.8} />
            </mesh>

            {/* HTML Overlay Annotation */}
            {isSelected && (
              <Html distanceFactor={10} zIndexRange={[100, 0]} className="pointer-events-none">
                <div className="bg-surface-container-highest/90 backdrop-blur-md p-3 rounded-lg border border-outline-variant shadow-lg flex flex-col gap-1 w-48 -translate-x-1/2 -translate-y-[120%]">
                  <div className="flex justify-between items-center border-b border-outline-variant pb-1">
                    <span className="font-numeric-telemetry text-primary font-bold text-[14px]">{region.id}</span>
                    <span className="text-[10px] font-bold uppercase" style={{ color }}>{region.risk}</span>
                  </div>
                  <div className="flex justify-between mt-1 text-[11px] font-body-sm">
                    <span className="text-on-surface-variant">Flare Prob:</span>
                    <span className="font-data-mono font-bold text-on-surface">{region.flareProb}%</span>
                  </div>
                </div>
              </Html>
            )}
          </group>
        );
      })}
    </group>
  );
};
