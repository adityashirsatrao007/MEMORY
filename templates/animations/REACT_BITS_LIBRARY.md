# ReactBits.dev — Animated UI Components Reference

> Source: https://reactbits.dev | GitHub: DavidHDev/react-bits | 40k+ stars
> 110+ free, customizable animations for text, backgrounds, and UI
> Install via: `npx shadcn@latest add @react-bits/<Component>-TS-TW`

---

## CATEGORIES

### 1. TEXT ANIMATIONS
| Component | Description | Install |
|-----------|-------------|---------|
| `BlurText` | Text blur reveal | `npx shadcn@latest add @react-bits/BlurText-TS-TW` |
| `SplitText` | Character/word split animation | `npx shadcn@latest add @react-bits/SplitText-TS-TW` |
| `DecryptText` | Matrix-style decrypt effect | `npx shadcn@latest add @react-bits/DecryptText-TS-TW` |
| `ShuffleText` | Scramble/shuffle characters | `npx shadcn@latest add @react-bits/ShuffleText-TS-TW` |
| `GradientText` | Animated gradient text | `npx shadcn@latest add @react-bits/GradientText-TS-TW` |
| `Typewriter` | Typing effect | `npx shadcn@latest add @react-bits/Typewriter-TS-TW` |
| `RotatingText` | Rotating word display | `npx shadcn@latest add @react-bits/RotatingText-TS-TW` |
| `CountUp` | Number counting animation | `npx shadcn@latest add @react-bits/CountUp-TS-TW` |

### 2. BACKGROUND ANIMATIONS
| Component | Description | Install |
|-----------|-------------|---------|
| `GradientBg` | Animated gradient background | `npx shadcn@latest add @react-bits/GradientBg-TS-TW` |
| `ParticleField` | Floating particles | `npx shadcn@latest add @react-bits/ParticleField-TS-TW` |
| `WavesBg` | Wave animation background | `npx shadcn@latest add @react-bits/WavesBg-TS-TW` |
| `NoiseBg` | Noise texture overlay | `npx shadcn@latest add @react-bits/NoiseBg-TS-TW` |
| `RippleBg` | Ripple effect background | `npx shadcn@latest add @react-bits/RippleBg-TS-TW` |
| `AuroraBg` | Aurora borealis effect | `npx shadcn@latest add @react-bits/AuroraBg-TS-TW` |
| `Globe` | 3D interactive globe | `npx shadcn@latest add @react-bits/Globe-TS-TW` |
| `PixelMap` | Pixelated map animation | `npx shadcn@latest add @react-bits/PixelMap-TS-TW` |

### 3. UI COMPONENTS
| Component | Description | Install |
|-----------|-------------|---------|
| `TiltCard` | 3D tilt on hover | `npx shadcn@latest add @react-bits/TiltCard-TS-TW` |
| `Magnet` | Magnetic hover effect | `npx shadcn@latest add @react-bits/Magnet-TS-TW` |
| `Spotlight` | Cursor spotlight effect | `npx shadcn@latest add @react-bits/Spotlight-TS-TW` |
| `HoverBorder` | Animated border on hover | `npx shadcn@latest add @react-bits/HoverBorder-TS-TW` |
| `AnimatedCard` | Card with entrance animation | `npx shadcn@latest add @react-bits/AnimatedCard-TS-TW` |
| `Parallax` | Scroll parallax wrapper | `npx shadcn@latest add @react-bits/Parallax-TS-TW` |
| `ScrollReveal` | Fade in on scroll | `npx shadcn@latest add @react-bits/ScrollReveal-TS-TW` |
| `Marquee` | Infinite scroll text | `npx shadcn@latest add @react-bits/Marquee-TS-TW` |

### 4. ANIMATION UTILITIES
| Component | Description | Install |
|-----------|-------------|---------|
| `AnimatedGroup` | Staggered group entrance | `npx shadcn@latest add @react-bits/AnimatedGroup-TS-TW` |
| `AnimatedText` | Word-by-word reveal | `npx shadcn@latest add @react-bits/AnimatedText-TS-TW` |
| `FadeIn` | Simple fade in wrapper | `npx shadcn@latest add @react-bits/FadeIn-TS-TW` |
| `ScaleIn` | Scale + fade entrance | `npx shadcn@latest add @react-bits/ScaleIn-TS-TW` |
| `SlideIn` | Slide from direction | `npx shadcn@latest add @react-bits/SlideIn-TS-TW` |

---

## CREATIVE TOOLS (Free, Browser-Based)

### Background Studio
- URL: https://reactbits.dev/tools
- Explore animated backgrounds, customize effects
- Export as video/image/code

### Shape Magic
- URL: https://reactbits.dev/tools
- Create inner rounded corners between shapes
- Export as SVG, React code, or clip-path

### Texture Lab
- URL: https://reactbits.dev/tools
- Apply 20+ effects (noise, dithering, ASCII) to images/videos
- Export in high quality

---

## QUICK USAGE EXAMPLES

### BlurText (Text Reveal)
```tsx
import { BlurText } from "@/components/react-bits/BlurText"

<BlurText
  text="Hello World"
  className="text-5xl font-bold text-white"
  animateBy="words"
  direction="top"
  delay={0.2}
/>
```

### SplitText (Character Animation)
```tsx
import { SplitText } from "@/components/react-bits/SplitText"

<SplitText
  text="Premium Experience"
  className="text-6xl font-bold text-white"
  charClassName="inline-block hover:text-blue-400 transition-colors"
/>
```

### GradientBg (Animated Background)
```tsx
import { GradientBg } from "@/components/react-bits/GradientBg"

<div className="relative">
  <GradientBg colors={["#667eea", "#764ba2", "#f093fb"]} />
  <div className="relative z-10">Content here</div>
</div>
```

### TiltCard (3D Hover)
```tsx
import { TiltCard } from "@/components/react-bits/TiltCard"

<TiltCard className="p-8 bg-white/5 border border-white/10 rounded-xl">
  <h3 className="text-white font-bold text-xl">Hover me</h3>
  <p className="text-white/60 mt-2">3D tilt effect</p>
</TiltCard>
```

### Marquee (Infinite Scroll)
```tsx
import { Marquee } from "@/components/react-bits/Marquee"

<Marquee speed={30} pauseOnHover className="py-4">
  {["React", "Next.js", "TypeScript", "Tailwind", "Motion"].map((tech) => (
    <span key={tech} className="mx-8 text-2xl text-white/20 font-bold">
      {tech}
    </span>
  ))}
</Marquee>
```

### Spotlight (Cursor Effect)
```tsx
import { Spotlight } from "@/components/react-bits/Spotlight"

<div className="relative group">
  <Spotlight className="opacity-0 group-hover:opacity-100 transition-opacity" />
  <div className="relative z-10 p-8">Content with spotlight</div>
</div>
```

---

## TECH VARIANTS (Choose Your Stack)

Each component comes in 4 variants:
- `JS-CSS` — JavaScript + CSS modules
- `JS-TW` — JavaScript + Tailwind CSS
- `TS-CSS` — TypeScript + CSS modules
- `TS-TW` — TypeScript + Tailwind CSS (RECOMMENDED)

Always use **TS-TW** variant for new projects.
