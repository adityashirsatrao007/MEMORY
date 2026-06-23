# 15 — Premium 3D Web Design & SaaS Template Architecture

Engineering guidelines for developing, optimizing, and deploying high-performance 3D scrollytelling pages and premium commercial SaaS templates.

---

## Core 3D Architecture Patterns

### 1. Unified Scroll-Inertial Smoothing (Lenis + GSAP)
All scrollytelling timelines must bind Lenis scroll updates directly to GSAP's ticker:
- **BOILERPLATE**:
  ```javascript
  const lenis = new Lenis({
    smoothWheel: true,
    wheelMultiplier: 1.0,
    touchMultiplier: 1.8,
  });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);
  ```

### 2. Vertex Displacement Shaders (Digital Terrains)
To build glowing digital landscapes that wave and distort based on scroll, displace Plane vertices in the animation loop:
- **FORMULA**:
  ```javascript
  const wave = Math.sin(x * 0.6 + time) * Math.cos(y * 0.6 + time) * (minHeight + scrollRatio * maxHeight);
  geometry.attributes.position.setZ(i, wave);
  ```

### 3. Connection Mesh Segmenting (Laser Linkages)
For networks of floating nodes, render dynamic linkages by checking distance thresholds in the loop:
- **DRAW RANGE**: Use a single `THREE.LineSegments` object and dynamically calculate connection pairs in the loop. Call `connectionLines.geometry.setDrawRange(0, lineCount)` to prune draw calls.

---

## Performance Guardrails

1. **Draw Call Consolidation**: Always prefer `THREE.InstancedMesh` over hundreds of standalone mesh instances.
2. **Resource Garbage Collection**: Explicitly call `.dispose()` on geometries, materials, and textures when the canvas component unmounts to prevent GPU memory leaks.
3. **Low-Poly Decimation**: Export 3D assets from Blender with decimation modifiers, target Draco compression, and limit textures to power-of-two resolutions (max 1024x1024).
