# Scrollytelling Production Toolchain

> Complete pipeline for building Apple-level product showcase websites

---

## PIPELINE OVERVIEW

```
Google Whisk (AI Image Gen)
        ↓
Google Veo Flow (Video/Animation)
        ↓
EZGif (Video → Frame Extraction)
        ↓
Anti-Gravity / Gemini 3 Pro (Code Generation)
        ↓
NodeJS (Local Development)
        ↓
Premium Scrollytelling Website
```

---

## TOOL 1: Google Whisk — AI Image Generation

**URL:** https://whisk.google.com
**Purpose:** Generate premium product shots with AI

### Workflow
1. Upload reference product photo
2. Use prompt for desired angle/style
3. Generate horizontal (hero) and vertical (detail) versions
4. Generate exploded/disassembled views for technical showcase

### Prompt Templates

**Hero Product Shot:**
```
Premium product photography, [PRODUCT] in matte black, three-quarter angle,
cinematic rim lighting, deep black background #050505, dramatic shadows,
Apple-level product rendering, photorealistic, 8K detail, studio lighting,
soft reflections, corporate luxury tech aesthetic
```

**Exploded View:**
```
Technical exploded view of [PRODUCT], all components separated and floating,
hyper-realistic internal structure visible, drivers microphones PCBs cushions,
dramatic rim lighting on each component, deep black background #050505,
engineering diagram aesthetic, premium corporate style
```

**Component Detail:**
```
Extreme close-up of [COMPONENT], macro photography, dramatic lighting,
studio black background, Sony/Apple corporate aesthetic, premium product detail
```

### Settings
- Orientation: Landscape for hero, Portrait for detail
- Style: Photorealistic
- Resolution: Maximum available

---

## TOOL 2: Google Veo Flow — Video/Animation

**URL:** https://veo.google.com
**Purpose:** Generate smooth animations between static frames

### Workflow
1. Upload start frame (assembled product)
2. Upload end frame (exploded view)
3. Use transition prompt
4. Generate smooth animation
5. Download upscaled version at 30 FPS

### Prompt Templates

**Product Disassembly:**
```
Smooth cinematic transition, product components gracefully separate and float
apart, each piece moves to its position in the exploded view, slow deliberate
motion, Apple-style product reveal animation, premium corporate feel,
dramatic lighting maintained throughout
```

**Product Reassembly:**
```
Reverse animation, floating components gracefully glide back into place,
product reassembles perfectly, final resting position, premium feel,
smooth buttery motion, cinematic product reveal
```

### Settings
- Duration: 4-8 seconds
- FPS: 30 (recommended for scroll-linked playback)
- Resolution: Highest available
- Style: Cinematic, smooth

---

## TOOL 3: EZGif — Frame Extraction

**URL:** https://ezgif.com/video-to-jpg
**Purpose:** Convert video to image sequence for web playback

### Workflow
1. Upload generated video from Veo Flow
2. Select "Video to JPG" converter
3. Set FPS to 30 (matches scroll-linked playback)
4. Convert and download as ZIP
5. Extract to `/public/frames/` in project

### Settings
- Output format: JPG (smaller file size)
- FPS: 30 (240 frames = 8 seconds of scroll)
- Quality: 90% (balance quality vs file size)
- Naming: Automatic sequential (frame-001.jpg, frame-002.jpg, etc.)

### File Organization
```
/public/frames/
├── frame-001.jpg
├── frame-002.jpg
├── ...
└── frame-240.jpg
```

---

## TOOL 4: Anti-Gravity / Gemini 3 Pro — Code Generation

**URL:** https://antigravity.dev (or use Gemini 3 Pro directly)
**Purpose:** Generate Next.js scrollytelling code from frames + prompt

### Workflow
1. Create project folder
2. Import frame folder (ZIP or directory)
3. Paste complete scrollytelling prompt
4. Use Gemini 3 Pro High model
5. Generate code

### Terminal Commands
```bash
cd project-folder
npm install
npm run dev
# Access at http://localhost:3000
```

### Prompt Template for Code Generation
```
Build a hyper-premium, Apple-level, cinematic scrollytelling landing page.
The experience uses a sticky full-screen canvas playing a [N]-frame image
sequence of [PRODUCT] exploding (disassembling) into a floating technical
diagram and then reassembling as the user scrolls.

Technical requirements:
- Next.js 14+ with App Router
- HTML5 Canvas for frame playback
- Scroll-linked animation (scroll progress maps to frame index)
- Background color #050505 matching frame backgrounds
- Text overlays with opacity/position animations at scroll thresholds
- Apple-style glassmorphism navbar
- Premium dark mode aesthetic
- Smooth, buttery scroll, hardware-accelerated
- No third-party animation libraries (vanilla JS + CSS)

Story beats:
- 0-15%: Hero with product name and tagline
- 15-40%: Engineering reveal, left-aligned text
- 40-65%: Technology section, right-aligned text
- 65-85%: Sound quality, centered text
- 85-100%: CTA with gradient button
```

---

## TOOL 5: NodeJS — Local Development

**Install via nvm:**
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20
```

**Or use existing Node.js installation (already on this machine).**

---

## COLOR PALETTE REFERENCE

| Token | Hex | Usage |
|-------|-----|-------|
| Primary BG | `#050505` | Main background, matches frame BG |
| Secondary BG | `#0A0A0C` | Section variations |
| Heading Text | `rgba(255,255,255,0.9)` | Headlines |
| Body Text | `rgba(255,255,255,0.6)` | Descriptions |
| Primary Accent | `#0050FF` | Sony deep blue |
| Secondary Accent | `#00D6FF` | Electric cyan highlights |
| Gradient Start | `#0050FF` | CTA buttons |
| Gradient End | `#00D6FF` | CTA buttons |

---

## TYPOGRAPHY REFERENCE

| Element | Font | Size | Weight | Tracking |
|---------|------|------|--------|----------|
| Hero H1 | Inter/SF Pro | 64-96px | Bold | Tight (-0.03em) |
| Section H2 | Inter/SF Pro | 36-56px | Bold | Tight (-0.02em) |
| Body | Inter/SF Pro | 16-18px | Regular | Normal |
| Mono/Labels | JetBrains Mono | 10-12px | Medium | Wide (0.1em) |

---

## SCROLL-LINKED ARCHITECTURE

```tsx
// Core scroll-to-frame mapping
const { scrollYProgress } = useScroll({ target: containerRef })
const frameIndex = useTransform(scrollYProgress, [0, 1], [0, FRAME_COUNT - 1])

// Story beat thresholds
const opacity = useTransform(scrollYProgress,
  [threshold.start - 0.03, threshold.start, threshold.end, threshold.end + 0.03],
  [0, 1, 1, 0]
)

// Canvas draws frame based on current index
useMotionValueEvent(frameIndex, "change", (latest) => {
  const ctx = canvasRef.current?.getContext("2d")
  const img = imagesRef.current[Math.round(latest)]
  if (ctx && img) ctx.drawImage(img, 0, 0, width, height)
})
```
