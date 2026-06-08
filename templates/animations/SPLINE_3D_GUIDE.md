# Spline 3D Integration — Complete Guide

> Source: Spline.design skill (spline-3d-integration)
> For embedding interactive 3D scenes into web projects

---

## WHAT IS SPLINE?

Browser-based 3D design tool (like Figma for 3D). Designers create interactive 3D scenes, then export via hosted `.splinecode` URL for web embedding.

---

## STEP 1: IDENTIFY STACK

| Stack | Method |
|-------|--------|
| Vanilla HTML/JS | `<spline-viewer>` web component OR `@splinetool/runtime` |
| React / Vite | `@splinetool/react-spline` |
| Next.js | `@splinetool/react-spline/next` |
| Vue | `@splinetool/vue-spline` |
| iframe | Public URL iframe |

---

## STEP 2: GET SCENE URL

Spline editor → Export → Code Export → copy `prod.spline.design` URL.

**Play Settings (before copying):**
- ✅ Hide Background ON (if site has custom bg)
- ✅ Hide Spline Logo ON (paid plan)
- ✅ Geometry Quality → Performance
- ✅ Disable Page Scroll, Zoom, Pan if not needed
- ✅ Click Promote to Production after changes (URL doesn't auto-update)

---

## STEP 3: EMBED

### React (Recommended)
```bash
npm install @splinetool/react-spline
```

```tsx
import Spline from '@splinetool/react-spline';

export default function Hero() {
  return (
    <Spline
      scene="https://prod.spline.design/XXXXX/scene.splinecode"
      style={{ width: '100%', height: '100vh' }}
    />
  );
}
```

### Next.js (SSR-safe)
```bash
npm install @splinetool/react-spline
```

```tsx
import dynamic from 'next/dynamic';

const Spline = dynamic(() => import('@splinetool/react-spline/next'), {
  ssr: false,
  loading: () => <div style={{ background: '#0a0a0a', height: '100vh' }} />
});

export default function Page() {
  return <Spline scene="https://prod.spline.design/XXXXX/scene.splinecode" />;
}
```

### Vanilla HTML
```html
<script type="module" src="https://unpkg.com/@splinetool/viewer/build/spline-viewer.js"></script>
<spline-viewer url="https://prod.spline.design/XXXXX/scene.splinecode"></spline-viewer>
```

---

## PRODUCTION WRAPPER (React)

```tsx
"use client"
import { lazy, Suspense, useState, useEffect, useRef } from 'react';

const Spline = lazy(() => import('@splinetool/react-spline'));

function shouldLoadSpline(breakpoint = 768) {
  if (typeof window === 'undefined') return false;
  const isMobile = window.innerWidth < breakpoint;
  const isLowEnd = navigator.hardwareConcurrency <= 2;
  const canvas = document.createElement('canvas');
  const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
  return !isMobile && !isLowEnd && !!gl;
}

export default function SplineBg({ sceneUrl, fallbackColor = '#0a0a0a', children }) {
  const [loaded, setLoaded] = useState(false);
  const [failed, setFailed] = useState(false);
  const [canLoad, setCanLoad] = useState(false);
  const timeoutRef = useRef();

  useEffect(() => setCanLoad(shouldLoadSpline()), []);

  useEffect(() => {
    if (!canLoad) return;
    timeoutRef.current = setTimeout(() => { if (!loaded) setFailed(true); }, 8000);
    return () => clearTimeout(timeoutRef.current);
  }, [canLoad, loaded]);

  const showFallback = !canLoad || failed;

  return (
    <div style={{ position: 'relative', width: '100%', height: '100vh' }}>
      <div style={{
        position: 'absolute', inset: 0, zIndex: 0,
        background: fallbackColor,
        opacity: loaded && !showFallback ? 0 : 1,
        transition: 'opacity 0.6s ease',
      }} />
      {canLoad && !failed && (
        <Suspense fallback={null}>
          <Spline scene={sceneUrl} onLoad={() => { clearTimeout(timeoutRef.current); setLoaded(true); }}
            style={{ position: 'absolute', inset: 0, zIndex: 0, opacity: loaded ? 1 : 0,
              transition: 'opacity 0.6s ease', pointerEvents: 'none' }} />
        </Suspense>
      )}
      {children && <div style={{ position: 'relative', zIndex: 1 }}>{children}</div>}
    </div>
  );
}
```

---

## COMMON PROBLEMS & FIXES

| Symptom | Cause | Fix |
|---------|-------|-----|
| Page won't scroll | `overflow: hidden` injected by Spline | `body { overflow: auto !important }` or disable Page Scroll in Play Settings |
| White box behind scene | Background not hidden | Play Settings → Hide Background → regenerate URL |
| Loads sometimes, blank others | CDN flakiness | Add 8s timeout fallback; self-host `.splinecode` |
| Smooth on Mac, laggy elsewhere | GPU gap | Hardware detection, skip on low-end |
| Page jumps on load | No reserved space (CLS) | Set explicit height, `contain: strict` |
| Rotations wrong | Degrees vs radians | `Math.PI / 180 * degrees` |
| Buttons not clickable | Canvas captures clicks | `pointer-events: none` on Spline wrapper |
| Watermark visible | Free plan | Upgrade or CSS: `spline-viewer::part(logo) { display: none }` |
| CORS error | Cross-origin | Self-host `.splinecode` file |
| Hydration error (Next.js) | SSR conflict | `dynamic(() => import(...), { ssr: false })` |
| Old scene showing | Didn't promote | Click Promote to Production in editor |

---

## ROTATION CHEAT SHEET

```js
// Spline uses RADIANS, not degrees
obj.rotation.y = Math.PI / 2;  // 90°
obj.rotation.y = Math.PI;      // 180°
obj.rotation.y = Math.PI * 2;  // 360°

const toRad = (deg) => deg * (Math.PI / 180);
obj.rotation.y = toRad(90);
```

---

## PERFORMANCE RULES

- Scene under 3MB = fine, 3-10MB = optimize, over 10MB = export as video
- Max 1-2 Spline embeds per page
- Less than 3 lights, prefer Matcap materials
- Lazy load: `const Spline = lazy(() => import('@splinetool/react-spline'))`
- Preload: `<link rel="preload" href="SCENE_URL" as="fetch" crossorigin>`
- Mobile: skip entirely or export as MP4 video fallback
- Pre-allocate space to prevent CLS
