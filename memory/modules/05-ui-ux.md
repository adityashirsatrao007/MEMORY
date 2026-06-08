# UI/UX Design Standards & Web Development

> Extracted from `GEMINI.md`. See `memory/modules/02-cli-tools.md` for frontend tool stack, `memory/modules/06-web-dev.md` for project setup and SEO.

---

## 🎨 UI/UX Standard (Default — Never Needs to Be Asked)

Every web interface MUST be premium quality:
- **Font:** `-apple-system, BlinkMacSystemFont, "SF Pro Display", Inter, sans-serif`
- **Dark mode:** Default background `#1C1C1E`, surface `#2C2C2E`
- **Glass effects:** `backdrop-filter: blur(20px)` on cards and modals
- **Animations & Micro-Interactions:** Scale 0.98 on press, 150ms transitions, shake on errors
- **Auto-Sizing Typography:** Scale down dynamically based on string length
- **Physical Keyboarding:** Keyboard shortcut mapping for critical UI operations
- **Colors:** HSL-tuned, harmonious palettes
- **Icons:** SVG or Lucide only — never raw emoji as icons
- **Background Visibility:** Transparent backgrounds on sections when WebGL layers are active

---

## 🎨 High-End Web Development & Design Standards (Mandatory)

### 1. The Core Philosophy
> *"Do not build a website; build a digital instrument."*

### 2. Design System & Aesthetic (The "Nura Health" Standard)
- **Primary Palette:** Moss (`#2E4036`), Clay (`#CC5833`), Cream (`#F2F0E9`), Charcoal (`#1A1A1A`)
- **Typography:** `Plus Jakarta Sans` & `Outfit` for headings, `Cormorant Garamond` for drama
- **Visual Texture:** CSS Noise overlays (SVG turbulence at 0.05 opacity)
- **Border Radius:** `rounded-[2rem]` to `rounded-[3rem]`

### 3. Component Architecture & Micro-Interactions
- **Navbar:** Floating pill-shaped, glassmorphic blur on scroll
- **Hero Sections:** 100dvh height, dramatic typography scale, GSAP staggered fade-ups
- **Features:** Interactive "Functional Artifacts" — diagnostic shufflers, telemetry feeds
- **Scroll Storytelling:** Parallax textures, GSAP SplitText reveals
- **Sticky Stacking:** GSAP ScrollTrigger with card scaling/blur/fade
- **Buttons:** "Magnetic" hover feel, overflow-hidden sliding backgrounds
- **Radial Mask Reveal:** Cursor-driven feathered gradient mask via GSAP `quickTo`
- **Dot-Grid Toggle Morph:** 2x2 dots → X via GSAP rotation/scaling

### 4. Technical Execution
- **Stack:** React 19, Tailwind CSS, GSAP 3 (with ScrollTrigger), Lucide React
- **Animation Lifecycle:** `gsap.context()` or `@gsap/react` `useGSAP()` within `useEffect`
- **Media:** Real image URLs (Unsplash), sophisticated SVG icons

---

## 🎨 Autonomous Web Design & Vibe Coding Engine (Mandatory)

### 1. Aesthetic Selection Matrix
| Aesthetic | When | Key Traits |
|-----------|------|------------|
| **Glassmorphism** | SaaS landing pages | Vivid gradients, frosted glass, white text |
| **Dark Luxury** | Premium SaaS | `#0A0A0A`, accent color, soft borders |
| **Minimalism** | Portfolios, blogs | Off-white, serif font, zero decoration |
| **Brutalism** | Dev tools, indie | White/yellow bg, 3px black borders, monospace |
| **Bento Grid** | Product showcases | Varying card sizes, dark + accent mix |
| **Claymorphism** | Task apps, consumer | Candy colors, extreme border-radius, 3D shadows |
| **Retro/Y2K** | Experimental | Hot pink/cyan, pixel fonts, metallic chrome |

### 2. Layout Engine
- **Hero + Feature Grid:** Default for SaaS
- **Asymmetric Split (60/40):** Product explanations
- **Sidebar + Content:** Dashboards, admin panels (240px sidebar)
- **Masonry:** Photo galleries (`columns: 3`)
- **F-Pattern:** Long-form articles (68% left, 28% right sidebar)

### 3. Animation & Scroll Physics
- **Smooth Scroll:** Lenis
- **Scroll-Triggered Reveals:** IntersectionObserver or GSAP, staggered
- **Text Reveal:** SplitType.js + GSAP
- **Parallax:** 30% bg / 60% mid / 100% foreground

### 4. Navigation Architecture
- **Sticky Frosted Navbar:** Transparent at top, blurs on scroll > 60px
- **Fullscreen Hamburger:** Animated SVG to X, staggered link reveals

### 5. Authentication & Backend Decision Engine
- **Web App / Hackathon** → **Clerk** (default 90%)
- **Data-Heavy / SQL** → **Supabase**
- **Mobile / IoT** → **Firebase**
- **Zero-Cost / Total Ownership** → **Auth.js (NextAuth)**

### 6. API Key Interaction Protocol
1. Generate `.env.example` listing all required keys with URLs
2. Send ONE message with ALL keys — never one-by-one
3. Place keys in `.env.local` and continue without interruption
4. NEVER pause mid-build for keys

### 7. ZERO-INTERRUPTION EXECUTION PROTOCOL
- No open questions — make executive decisions
- No feedback blocks — set `request_feedback = false`
- READ, DECIDE, ACT — full pipeline without stopping

### 8. SELF-HEALING & ERROR MEMORY PROTOCOL
- Document every mistake and fix in global "Error Learnings"
- Pre-flight check against past mistakes before complex implementation

---

## 🎭 Premium Frontend Library Stack (Mandatory — Every Web Project)

### Core Stack
```bash
bun add next@latest react@19 react-dom@19
bun add lenis
bun add motion
bun add gsap @gsap/react
bun add three @types/three @react-three/fiber @react-three/drei
bun add tailwindcss @tailwindcss/vite
bun add zustand
npx shadcn@latest init
```

### Library Selection Matrix
| Need | Library |
|------|---------|
| Smooth scroll | **Lenis** |
| Basic animations | **Motion.dev** |
| Complex timelines | **GSAP** |
| 3D scenes | **Three.js + R3F** |
| 3D helpers | **Drei** |
| Post-processing | **R3F Postprocessing** |
| Text animations | **ReactBits** |
| UI components | **ReactBits** |
| Backgrounds | **ReactBits** |
| State management | **Zustand** |

### Scrolling Patterns
| Pattern | Implementation |
|---------|---------------|
| Long Scroll | Lenis + Motion `whileInView` |
| Fixed Scroll | CSS `sticky` + Lenis |
| Parallax | Lenis + `useTransform` |
| Scrollytelling | Canvas image sequence + scroll-linked playback |
| Infinite Scroll | Intersection Observer + API pagination |

### Long Scroll Best Practices
1. Chunk content visually
2. Front-load value above fold
3. Provide sticky nav + progress indicators
4. Lazy load images
5. Break text blocks with images/videos
6. Clear CTAs throughout
7. Mobile-first
8. Optimize speed (WebP/AVIF)
9. Monitor with Hotjar
10. Respect `prefers-reduced-motion`

---

## Claude UI Design Skills Playbook & Workflow

### Key Design Commands
| Command | Action |
|---------|--------|
| `/awesome-design-md` | Premium SaaS UI components |
| `/design-mastery` | UX & onboarding audits |
| `/mobile-app-ui-design` | Premium mobile app UI |
| `/ux-ui-mastery` | UX psychology & conversions |
| `/design-system-extractor` | Extract tokens from image |
| `/UI/UX Pro Max` | Interactive app UX audits |
| `/Vercel Web Design Guidelines` | High-converting landing pages |
| `/Vercel React Best Practices` | Clean React + Tailwind code |

### Winning Claude UI Design Workflow
1. Base UI (`/awesome-design-md`)
2. Onboarding & UX (`/design-mastery`)
3. Design Tokens (`/design-system-extractor`)
4. Mobile Adaptations (`/mobile-app-ui-design`)
5. Checkout & Conversion (`/ux-ui-mastery`)
6. Final Audit (`/UI/UX Pro Max`)
7. Landing Page Copy (`/Vercel Web Design Guidelines`)
8. Code Gen (`/Vercel React Best Practices`)
9. Ship!

---

## TEXTURA / Claude Code Website Pipeline (Premium Animated Websites)

### The 11-Step Pipeline
1. **Brief & Copywriting** — Generate all page copy first
2. **Find Section Reference** — Dribbble, Behance, Awwwards
3. **Strip Background** — Clean UI reference with GPT-4o
4. **Recreate Layout** — Next.js 16, React Spring animations
5. **Typography** — Google Fonts, Awwwards Free Fonts
6. **Color Palettes** — Coolors, export as CSS variables
7. **3D Models** — Sketchfab GLB/GLTF via Three.js or R3F
8. **Image & Video Generation** — OpenArt, Kling 3.0
9. **Animations** — GSAP ScrollTrigger from Pinterest references
10. **Asset Optimization** — Squoosh → WebP, lazy loading
11. **Host & Deploy** — Vercel, vercel.json, Lighthouse 90+

---

## Remix UI Implementation Guidance: Documentation Site

### Design Tokens
```json
{
  "font": {
    "family": "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, Monaco",
    "size": { "xs": "10px", "sm": "12px", "base": "16px", "lg": "56px", "xl": "84px" }
  },
  "color": {
    "text": { "primary": "#dee2e6", "secondary": "#ffffff", "tertiary": "#57cda4" },
    "surface": { "base": "#000000", "muted": "#1e2226" },
    "border": { "default": "#c8c8c8" }
  },
  "space": { "1": "4px", "2": "6px", "3": "10px", "4": "16px", "5": "19px", "6": "20px", "7": "24px", "8": "27px" },
  "radius": { "xs": "24px", "sm": "999px" },
  "motion": { "duration": { "instant": "150ms" } }
}
```

### Component Density Per Page
- **Links:** 24/page
- **Navigation blocks:** 3/page (Top Nav, Sidebar, ToC)
- **Buttons:** 2/page (Copy, Version switcher)
- **Inputs:** 1/page (Search)
- **Lists:** 1/page (Sidebar categories)

### Accessibility Requirements (WCAG 2.2 AA)
- Interactive elements: 4.5:1 contrast ratio
- Logical tab order
- Focus isolation in modals
- ARIA roles: `aria-expanded`, `role="searchbox"`, `<nav>` with `aria-label`

### Anti-Patterns
- ❌ No Tailwind default colors — use semantic tokens only
- ❌ No `outline: none` without custom focus style
- ❌ No arbitrary spacing — must use mapped `space.[1-8]`
- ❌ No `<div>`/`<span>` for clickable actions — use `<button>` or `<a>`

---

## Immersive & 3D Web Design Principles

### Immersive UX Mindset
- Active participation over passive consumption
- Narrative-driven storytelling — 3D is not a gimmick

### Implementation Methodologies
1. **Pre-rendered 3D Video** — Cinematic, no interactivity
2. **Interactive Image Sequences** — Lightweight 3D rotation
3. **Real-Time WebGL (Three.js, R3F, Spline)** — Full interactivity

### Technical Layering Rules
- WebGL canvases: `position: fixed`, `z-index: -1`
- Canvas pointer events: `pointer-events: none` for background layers
- Transparent wrappers: `bg-transparent` over WebGL backgrounds
- Maintain WCAG 4.5:1 contrast even with interactive lighting effects

### Optimization
- Draco compression on GLTF/GLB
- Texture maps max 2K
- Progressive loaders for WebGL assets
- Graceful fallback for incompatible browsers

### Reference Templates (in this repo)
| File | Lines | What It Contains |
|------|-------|-----------------|
| `templates/animations/FRONTEND_LIBRARY_STACK.md` | 324 | Install commands, code samples for Three.js, Lenis, Motion, GSAP, ReactBits |
| `templates/animations/MOTION_DEV_LIBRARY.md` | 282 | Motion.dev patterns and API reference |
| `templates/animations/REACT_BITS_LIBRARY.md` | 156 | ReactBits component catalog (text, backgrounds, UI) |
| `templates/animations/SCROLLING_PATTERNS.md` | 173 | 4 scroll patterns with decision guide |
| `templates/animations/SPLINE_3D_GUIDE.md` | 181 | Spline 3D interactive design guide |
| `templates/animations/UI_UX_PRO_MAX.md` | 273 | Premium UI critique and design system guide |
| `templates/animations/SCROLLYTELLING_TEMPLATE.tsx` | ~120 | React scrollytelling component (image sequence) |
| `templates/animations/SCROLLYTELLING_TOOLCHAIN.md` | ~120 | Image sequence + scroll pipeline docs |
| `templates/ASTRO_STARTERKIT.md` | 308 | Astro starter kit with design system |
| `templates/DEPLOYMENT_WORKFLOW.md` | 142 | GitHub + Vercel deployment workflow |
