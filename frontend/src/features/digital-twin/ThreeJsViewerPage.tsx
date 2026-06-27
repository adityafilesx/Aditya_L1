import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { WebGLErrorBoundary } from '@design-system/components/error-boundaries';

function DigitalTwinCanvas() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let scene: THREE.Scene | null = null;
    let camera: THREE.PerspectiveCamera | null = null;
    let renderer: THREE.WebGLRenderer | null = null;
    let sun: THREE.Mesh | null = null;
    let grid: THREE.Mesh | null = null;
    let corona: THREE.Mesh | null = null;
    let frameId = 0;

    const init = () => {
      const width = container.clientWidth || window.innerWidth;
      const height = container.clientHeight || window.innerHeight;

      scene = new THREE.Scene();
      camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
      camera.position.z = 5;

      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
      renderer.setSize(width, height);
      renderer.setPixelRatio(window.devicePixelRatio);
      container.appendChild(renderer.domElement);

      const geometry = new THREE.SphereGeometry(2, 64, 64);
      const material = new THREE.MeshPhongMaterial({
        color: 0xffcc33,
        emissive: 0xff6600,
        emissiveIntensity: 0.8,
        shininess: 10,
      });
      sun = new THREE.Mesh(geometry, material);
      scene.add(sun);

      const coronaGeo = new THREE.SphereGeometry(2.1, 64, 64);
      const coronaMat = new THREE.MeshBasicMaterial({
        color: 0xffaa00,
        transparent: true,
        opacity: 0.15,
        side: THREE.BackSide,
      });
      corona = new THREE.Mesh(coronaGeo, coronaMat);
      scene.add(corona);

      const gridGeometry = new THREE.SphereGeometry(2.01, 32, 32);
      const gridMaterial = new THREE.MeshBasicMaterial({
        color: 0xffffff,
        wireframe: true,
        transparent: true,
        opacity: 0.1,
      });
      grid = new THREE.Mesh(gridGeometry, gridMaterial);
      scene.add(grid);

      scene.add(new THREE.AmbientLight(0x404040, 2));
      const pointLight = new THREE.PointLight(0xffffff, 1, 100);
      pointLight.position.set(10, 10, 10);
      scene.add(pointLight);

      const animate = () => {
        frameId = requestAnimationFrame(animate);
        if (sun && grid) {
          sun.rotation.y += 0.001;
          grid.rotation.y += 0.001;
        }
        if (renderer && scene && camera) {
          renderer.render(scene, camera);
        }
      };
      animate();

      const onResize = () => {
        if (!container || !camera || !renderer) return;
        const w = container.clientWidth || window.innerWidth;
        const h = container.clientHeight || window.innerHeight;
        renderer.setSize(w, h);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
      };
      window.addEventListener('resize', onResize);

      return () => {
        window.removeEventListener('resize', onResize);
      };
    };

    let cleanupResize: (() => void) | undefined;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !renderer) {
          cleanupResize = init();
        } else if (!entries[0].isIntersecting && renderer) {
          // Pause animation when out of view
          cancelAnimationFrame(frameId);
        } else if (entries[0].isIntersecting && renderer) {
          // Resume animation
          const animate = () => {
            frameId = requestAnimationFrame(animate);
            if (sun && grid) {
              sun.rotation.y += 0.001;
              grid.rotation.y += 0.001;
            }
            if (renderer && scene && camera) {
              renderer.render(scene, camera);
            }
          };
          animate();
        }
      },
      { threshold: 0.1 }
    );

    observer.observe(container);

    return () => {
      observer.disconnect();
      cancelAnimationFrame(frameId);
      if (cleanupResize) cleanupResize();

      if (renderer) {
        container.removeChild(renderer.domElement);
        renderer.dispose();
      }
      
      // Deep dispose to free GPU memory
      scene?.traverse((object) => {
        if (object instanceof THREE.Mesh) {
          object.geometry.dispose();
          if (object.material instanceof Array) {
            object.material.forEach((m) => m.dispose());
          } else {
            object.material.dispose();
          }
        }
      });
    };
  }, []);

  return <div ref={containerRef} className="w-full h-full" />;
}

export function ThreeJsViewerPage() {
  return (
    <div className="fixed inset-0 w-full h-full bg-black">
      <WebGLErrorBoundary>
        <DigitalTwinCanvas />
      </WebGLErrorBoundary>
    </div>
  );
}
