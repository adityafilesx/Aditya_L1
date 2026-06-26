import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { Environment, Preload, PerformanceMonitor } from '@react-three/drei';
import { SolarSphere } from './SolarSphere';
import { CameraControls } from './CameraControls';
import { ActiveRegions3D } from './ActiveRegions3D';

export const TwinCanvas: React.FC = () => {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 45 }}
      gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
      dpr={[1, 2]} // Support high-DPI displays but cap at 2x for performance
    >
      <PerformanceMonitor onDecline={(fps) => console.warn('FPS Drop: ' + fps)}>
        <ambientLight intensity={1.5} />
        <pointLight position={[10, 10, 10]} intensity={2.5} />
        
        <Suspense fallback={null}>
          <SolarSphere />
          <ActiveRegions3D />
          <Environment preset="night" />
          <Preload all />
        </Suspense>

        <CameraControls />
      </PerformanceMonitor>
    </Canvas>
  );
};
