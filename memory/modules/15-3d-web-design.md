# 3D Web Design Patterns

## React Three Fiber (R3F) Setup
```bash
npm install three @react-three/fiber @react-three/drei
```

### Basic Scene
```jsx
import { Canvas } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera } from '@react-three/drei'

function Scene() {
  return (
    <Canvas>
      <PerspectiveCamera makeDefault position={[0, 2, 5]} />
      <OrbitControls />
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} />
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="#6366f1" />
      </mesh>
    </Canvas>
  )
}
```

## Model Loading
```jsx
import { useGLTF } from '@react-three/drei'

function Model({ url }) {
  const { scene } = useGLTF(url)
  return <primitive object={scene} />
}

// Preload for performance
useGLTF.preload('/models/scene.glb')
```

## Draco Compression
```bash
npm install gltf-pipeline
# Compress models
gltf-pipeline -i input.glb -o output.glb --draco.compressionLevel 7
```

## Texture Optimization
```jsx
import { useTexture } from '@react-three/drei'

function TexturedPlane() {
  const [map, normalMap] = useTexture(['./diffuse.jpg', './normal.jpg'])
  return (
    <mesh>
      <planeGeometry args={[4, 4]} />
      <meshStandardMaterial map={map} normalMap={normalMap} />
    </mesh>
  )
}
```

### Rules
- Use `Suspense` wrapper for async loads
- Set `dpr={[1, 2]}` for mobile optimization
- Use `useMemo` for geometry/materials
- Dispose unused resources: `geometry.dispose()`
- Prefer GLB over GLTF (single file)
- Max texture size: 2048x2048 for mobile, 4096 for desktop

## GSAP + Three.js Integration
```jsx
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

// Scroll-driven camera animation
gsap.to(camera.position, {
  scrollTrigger: { trigger: '#section2', start: 'top center' },
  z: 2, y: 1, duration: 1
})
```

## Performance Budget
| Metric | Target |
|--------|--------|
| Initial load | < 3MB |
| FPS (mobile) | > 30 |
| FPS (desktop) | > 60 |
| Draw calls | < 50 |
| Triangles | < 100K |
