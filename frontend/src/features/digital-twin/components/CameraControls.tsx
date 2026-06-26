import React, { useRef, useEffect } from 'react';
import { OrbitControls } from '@react-three/drei';
import { useThree } from '@react-three/fiber';
import { useWorkspaceStore } from '../../../realtime/workspaceStore';

export const CameraControls: React.FC = () => {
  const controlsRef = useRef<any>(null);
  const { camera } = useThree();
  const focusedRegion = useWorkspaceStore(state => state.activeRegion);

  useEffect(() => {
    if (focusedRegion && controlsRef.current) {
      // Basic spherical to cartesian conversion for the active region
      const phi = (90 - focusedRegion.lat) * (Math.PI / 180);
      const theta = (focusedRegion.lon + 90) * (Math.PI / 180);
      
      const r = 3; // distance
      const x = r * Math.sin(phi) * Math.cos(theta);
      const y = r * Math.cos(phi);
      const z = r * Math.sin(phi) * Math.sin(theta);
      
      // Auto focus camera
      camera.position.set(x, y, z);
      camera.lookAt(0, 0, 0);
      controlsRef.current.update();
    }
  }, [focusedRegion, camera]);

  return (
    <OrbitControls
      ref={controlsRef}
      enablePan={true}
      enableZoom={true}
      minDistance={2.1}
      maxDistance={10}
      enableDamping
      dampingFactor={0.05}
    />
  );
};
