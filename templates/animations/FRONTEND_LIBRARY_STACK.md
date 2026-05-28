# Ultimate Frontend Library Stack — Premium Website Development

> Combined reference: Three.js, React Three Fiber, Lenis, Motion.dev, ReactBits, Scrolling Patterns
> Last updated: 2026-05-28

---

## LIBRARY ECOSYSTEM MAP

```
┌─────────────────────────────────────────────────────┐
│                   PREMIUM WEBSITE                     │
├─────────────┬──────────────┬──────────────┬──────────┤
│   3D LAYER  │ SCROLL LAYER │ ANIMATION    │ UI       │
│             │              │ LAYER        │ LAYER    │
├─────────────┼──────────────┼──────────────┼──────────┤
│ Three.js    │ Lenis        │ Motion.dev   │ ReactBits│
│ R3F         │ GSAP Scroll  │ Framer Motion│ Radix UI │
│ Drei        │ Locomotive   │ React Spring │ Tailwind │
│ Postprocess │ ScrollMagic  │ CSS Anim     │ shadcn   │
└─────────────┴──────────────┴──────────────┴──────────┘
```

---

## 1. THREE.JS + REACT THREE FIBER (3D Layer)

### Installation
```bash
bun add three @types/three @react-three/fiber @react-three/drei
```

### What Each Package Does
| Package | Stars | Purpose |
|---------|-------|---------|
| `three` | 113k | Core 3D engine — WebGL/WebGPU renderer, scene, camera, mesh, materials |
| `@react-three/fiber` | 30.9k | React renderer for Three.js — declarative JSX 3D scenes |
| `@react-three/drei` | — | Useful helpers — Environment, Float, Text3D, useGLTF, etc. |
| `@react-three/postprocessing` | — | Post-processing effects — Bloom, DOF, Vignette |

### Basic 3D Scene (React)
```tsx
"use client"
import { Canvas } from "@react-three/fiber"
import { Float, Environment, ContactShadows } from "@react-three/drei"

export function Hero3D() {
  return (
    <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
      <ambientLight intensity={0.5} />
      <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
      <Float speed={2} rotationIntensity={0.5}>
        <mesh>
          <torusGeometry args={[1, 0.4, 16, 100]} />
          <meshStandardMaterial color="#0050FF" metalness={0.9} roughness={0.1} />
        </mesh>
      </Float>
      <ContactShadows position={[0, -1.5, 0]} opacity={0.4} blur={2.5} />
      <Environment preset="city" />
    </Canvas>
  )
}
```

### Scroll-Linked 3D (Product Showcase)
```tsx
"use client"
import { useRef } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { useScroll, useTransform } from "motion/react"
import * as THREE from "three"

function RotatingProduct() {
  const meshRef = useRef<THREE.Mesh>(null)
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = state.clock.getElapsedTime() * 0.3
    }
  })
  return (
    <mesh ref={meshRef}>
      <torusKnotGeometry args={[1, 0.3, 128, 32]} />
      <meshStandardMaterial color="#00D6FF" wireframe />
    </mesh>
  )
}

export function Scroll3D() {
  const containerRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({ target: containerRef, offset: ["start end", "end start"] })

  return (
    <div ref={containerRef} className="h-[200vh]">
      <div className="sticky top-0 h-screen">
        <Canvas camera={{ position: [0, 0, 5] }}>
          <ambientLight intensity={0.5} />
          <RotatingProduct />
        </Canvas>
      </div>
    </div>
  )
}
```

### Ecosystem Packages
| Package | Purpose |
|---------|---------|
| `@react-three/drei` | Helpers (Environment, Float, Text3D, useGLTF, OrbitControls) |
| `@react-three/postprocessing` | Bloom, DOF, Vignette, ChromaticAberration |
| `@react-three/rapier` | 3D physics engine |
| `@react-three/xr` | VR/AR support |
| `@react-three/flex` | Flexbox for 3D layouts |
| `leva` | GUI controls for debugging |
| `maath` | Math helpers for 3D |
| `zustand` | State management for R3F scenes |

---

## 2. LENIS (Smooth Scroll Layer)

### Installation
```bash
bun add lenis
```

### Setup (React)
```tsx
"use client"
import { useEffect } from "react"
import Lenis from "lenis"
import "lenis/dist/lenis.css"

export function SmoothScroll({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const lenis = new Lenis({
      autoRaf: true,
      lerp: 0.1,
      duration: 1.2,
      smoothWheel: true,
    })

    return () => lenis.destroy()
  }, [])

  return <>{children}</>
}
```

### With GSAP ScrollTrigger
```tsx
import Lenis from "lenis"
import { gsap } from "gsap"
import { ScrollTrigger } from "gsap/ScrollTrigger"

const lenis = new Lenis()
lenis.on("scroll", ScrollTrigger.update)
gsap.ticker.add((time) => lenis.raf(time * 1000))
gsap.ticker.lagSmoothing(0)
```

### Key Settings
| Setting | Default | Purpose |
|---------|---------|---------|
| `lerp` | 0.1 | Linear interpolation (lower = smoother) |
| `duration` | 1.2 | Scroll animation duration in seconds |
| `smoothWheel` | true | Smooth mouse wheel scrolling |
| `autoRaf` | false | Auto requestAnimationFrame loop |
| `infinite` | false | Enable infinite scrolling |
| `anchors` | false | Enable anchor link scrolling |
| `gestureOrientation` | vertical | Vertical, horizontal, or both |

---

## 3. MOTION.DEV (Animation Layer)

### Installation
```bash
bun add motion
```

### Core APIs
```tsx
import { motion, AnimatePresence, useScroll, useTransform, stagger } from "motion/react"
```

### Key Patterns (see MOTION_DEV_LIBRARY.md for full reference)
| Pattern | Use Case |
|---------|----------|
| `motion.div` + `animate` | Basic element animation |
| `whileHover` / `whileTap` | Gesture-based interactions |
| `whileInView` | Scroll-triggered reveals |
| `useScroll` + `useTransform` | Scroll-linked effects |
| `AnimatePresence` | Mount/unmount animations |
| `variants` + `stagger` | Coordinated list animations |
| `layout` | Layout morphing animations |
| `spring` transitions | Physics-based natural motion |

---

## 4. REACTBITS (UI Component Layer)

### Installation
```bash
npx shadcn@latest add @react-bits/BlurText-TS-TW
npx shadcn@latest add @react-bits/TiltCard-TS-TW
npx shadcn@latest add @react-bits/Marquee-TS-TW
npx shadcn@latest add @react-bits/Spotlight-TS-TW
```

### Categories (see REACT_BITS_LIBRARY.md for full reference)
| Category | Components |
|----------|-----------|
| Text Animations | BlurText, SplitText, DecryptText, ShuffleText, GradientText, Typewriter |
| Backgrounds | GradientBg, ParticleField, WavesBg, NoiseBg, AuroraBg, Globe |
| UI Components | TiltCard, Magnet, Spotlight, HoverBorder, AnimatedCard, ScrollReveal |
| Utilities | AnimatedGroup, FadeIn, ScaleIn, SlideIn, Marquee |

---

## 5. GSAP (Animation Powerhouse — Alternative to Motion)

### Installation
```bash
bun add gsap
```

### When to Use GSAP Over Motion
| Scenario | Use GSAP | Use Motion |
|----------|----------|-----------|
| Complex timeline sequences | ✅ | ❌ |
| Scroll-triggered pinning | ✅ | ✅ |
| React declarative animations | ❌ | ✅ |
| SVG morphing/path animation | ✅ | ✅ |
| Physics-based spring | ❌ | ✅ |
| Three.js integration | ✅ | ❌ |
| Learning curve | Steeper | Easier |

---

## SCROLLING PATTERNS — DECISION GUIDE

> Source: Clay Global, UXPin (2026)

### The 4 Patterns
| Pattern | What | Best For |
|---------|------|----------|
| **Long Scroll** | All content on one page | Storytelling, landing pages, mobile |
| **Fixed Scroll** | Sticky headers/sidebars | Docs, e-commerce, dashboards |
| **Infinite Scroll** | Auto-loads at bottom | Social feeds, galleries |
| **Parallax** | Layers move at different speeds | Brand stories, portfolios |

### Long Scroll Best Practices (Clay Global 2026)
1. **Chunk content visually** — distinct sections with headings, background changes
2. **Front-load value** — most important content + CTA above the fold
3. **Provide orientation** — sticky nav, progress indicators, back-to-top
4. **Lazy load images** — Intersection Observer for off-screen content
5. **Break text blocks** — short paragraphs, images, videos between sections
6. **Clear CTAs throughout** — guide users on what to do next
7. **Mobile-first** — buttons/links big enough to tap, text readable
8. **Optimize speed** — compress files, limit plugins, use modern formats
9. **Monitor with Hotjar** — heatmaps show where users scroll/lose interest
10. **Respect `prefers-reduced-motion`** — always provide fallback

### Anti-Patterns (Never Do This)
- ❌ Infinite scroll + parallax on same page (conflict)
- ❌ Auto-loading without "Load More" fallback
- ❌ Fixed elements that obscure content on mobile
- ❌ Heavy parallax on content-heavy pages (kills readability)
- ❌ No loading indicators during content loads
- ❌ Forgetting footer links are unreachable with infinite scroll

---

## THE ULTIMATE STACK (Recommended for Premium Sites)

```bash
# Core
bun add next@latest react@19 react-dom@19

# 3D
bun add three @types/three @react-three/fiber @react-three/drei

# Scroll
bun add lenis gsap

# Animation
bun add motion

# UI Components
npx shadcn@latest init
npx shadcn@latest add @react-bits/BlurText-TS-TW
npx shadcn@latest add @react-bits/TiltCard-TS-TW
npx shadcn@latest add @react-bits/Marquee-TS-TW

# Styling
bun add tailwindcss @tailwindcss/vite

# State (for complex 3D scenes)
bun add zustand
```

### Package Sizes (bundle impact)
| Package | Size | Critical? |
|---------|------|-----------|
| `three` | ~150KB | Only if using 3D |
| `@react-three/fiber` | ~40KB | With three |
| `lenis` | ~10KB | Always |
| `gsap` | ~30KB | If using complex timelines |
| `motion` | ~25KB | Always |
| `react-bits` | ~5KB per component | Selectively |

---

## REFERENCE SITES (Study These)

| Site | Pattern | What to Learn |
|------|---------|---------------|
| [apple.com/iphone](https://apple.com/iphone) | Long scroll + parallax | Product storytelling, image sequence |
| [stripe.com](https://stripe.com) | Long scroll + fixed nav | SaaS value proposition flow |
| [linear.app](https://linear.app) | Dark luxury + 3D | Premium SaaS aesthetic |
| [vercel.com](https://vercel.com) | Long scroll + animations | Developer-focused design |
| [threejs.org](https://threejs.org) | 3D showcases | WebGL product demos |
| [darkroom.engineering](https://darkroom.engineering) | Lenis + R3F | Premium scroll + 3D combo |
| [lusion.co](https://lusion.co) | R3F + scroll | Awwwards-level 3D sites |
