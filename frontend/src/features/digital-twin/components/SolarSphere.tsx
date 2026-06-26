import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere } from '@react-three/drei';
import * as THREE from 'three';
import { useWorkspaceStore } from '../../../realtime/workspaceStore';
import { useSpring, animated } from '@react-spring/three';

export const SolarSphere: React.FC = () => {
  const sunRef = useRef<THREE.Mesh>(null);
  const coronaRef = useRef<THREE.Mesh>(null);
  const gridRef = useRef<THREE.Mesh>(null);
  
  const digitalTwin = useWorkspaceStore(state => state.digitalTwin);
  const isPlaying = useWorkspaceStore(state => state.isPlaying);
  const replaySpeed = useWorkspaceStore(state => state.replaySpeed);

  // Animated springs for smooth opacity transitions via Leva UI
  const { photosphereOp, coronaOp, magneticOp } = useSpring({
    photosphereOp: digitalTwin.photosphereOpacity / 100,
    coronaOp: digitalTwin.coronaOpacity / 100,
    magneticOp: digitalTwin.magneticOpacity / 100,
    config: { tension: 120, friction: 14 }
  });

  useFrame((_state, delta) => {
    if (isPlaying && sunRef.current && gridRef.current && coronaRef.current) {
      const rotationSpeed = 0.05 * replaySpeed * delta;
      sunRef.current.rotation.y += rotationSpeed;
      gridRef.current.rotation.y += rotationSpeed;
      coronaRef.current.rotation.y += rotationSpeed * 1.2;
    }
  });

  return (
    <group>
      {/* Photosphere / Base Layer */}
      <Sphere ref={sunRef} args={[2, 64, 64]}>
        <animated.meshPhongMaterial 
          color="#ffcc33" 
          emissive="#ff6600"
          emissiveIntensity={0.8}
          shininess={10}
          transparent
          opacity={photosphereOp}
        />
      </Sphere>

      {/* Corona Layer */}
      <Sphere ref={coronaRef} args={[2.08, 64, 64]}>
        <animated.meshBasicMaterial 
          color="#ffaa00"
          transparent
          opacity={coronaOp.to(o => o * 0.3)} // Max opacity is lower for corona
          side={THREE.BackSide}
          blending={THREE.AdditiveBlending}
        />
      </Sphere>

      {/* Magnetic / Grid Layer */}
      <Sphere ref={gridRef} args={[2.01, 32, 32]}>
        <animated.meshBasicMaterial 
          color="#ffffff"
          wireframe
          transparent
          opacity={magneticOp.to(o => o * 0.15)}
          blending={THREE.AdditiveBlending}
        />
      </Sphere>
    </group>
  );
};
