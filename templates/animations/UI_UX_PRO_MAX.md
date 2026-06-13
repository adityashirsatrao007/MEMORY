# UI/UX Pro Max — AI Design Intelligence Framework

> Source: AntiGravity / UI/UX Pro Max Skill (67+ styles, 95+ palettes)
> 5 Dimensions: Pattern, Style, Color, Typography, Animations

---

## THE 5 DIMENSIONS FRAMEWORK

When requesting a design from an AI agent, structure prompts using these 5 dimensions:

1. **PATTERN & LAYOUT** — The skeleton (functional structure)
2. **STYLE & AESTHETIC** — The skin (visual personality)
3. **COLOR & THEME** — The palette (emotional tone)
4. **TYPOGRAPHY** — The voice (brand personality)
5. **ANIMATIONS & INTERACTIONS** — The soul (life and delight)

---

## DIMENSION 1: PATTERN & LAYOUT

### Product-Specific Patterns

| Product | Pattern | Focus | Layout |
|---------|---------|-------|--------|
| **SaaS** | Hero + Features + Social Proof + CTA | Value proposition first | Full-width hero, 3-col features, testimonial carousel, sticky CTA |
| **Micro SaaS** | Minimal & Direct + Live Demo | Show don't tell | Centered hero with embedded demo, minimal nav, single CTA |
| **E-commerce Luxury** | Feature-Rich Showcase + Immersive Gallery | Large imagery, storytelling | Full-screen hero slider, grid gallery, product zoom |
| **Fintech/Crypto** | Conversion-Optimized + Trust Signals | Data viz, security badges | Split hero, live stats dashboard, trust indicators |
| **Analytics Dashboard** | Bento Grid + Actionable Insights | Data density with clarity | Modular card system, hierarchical info, quick filters |
| **Portfolio/Agency** | Storytelling + Case Studies | Visual impact, personality | Full-screen sections, horizontal scroll galleries |

---

## DIMENSION 2: STYLE & AESTHETIC

### Core Styles (Pick One)

| Style | Keywords | Technical | Use When | Avoid |
|-------|----------|-----------|----------|-------|
| **Glassmorphism** | Frosted glass, transparent layers, blurred background | `backdrop-filter: blur(10px)`, rgba backgrounds | Modern apps, dashboards | Low-contrast, accessibility issues |
| **Aurora UI** | Vibrant gradients, Northern Lights, mesh gradient | Multi-stop gradients, animated hue rotation | Landing pages, creative portfolios | Text-heavy, corporate |
| **Soft UI 2.0** | Soft shadows, subtle gradients, tactile | `box-shadow: inset + outset`, same-color palette | Mobile apps, wellness | Complex data, accessibility |
| **Linear/Vercel** | Dark mode, subtle borders, minimalist | `#0A0A0A` bg, `#1A1A1A` cards, `#333` borders | Developer tools, SaaS | Consumer, playful |
| **Bento Grid** | Modular, organized, information-dense | CSS Grid, varying card sizes, 16-24px gaps | Dashboards, feature showcases | Simple pages |
| **Liquid Glass** | Fluid shapes, organic movement, glossy | SVG blobs, backdrop-filter, animated transforms | Creative agencies, interactive | Traditional industries |
| **Brutalism** | Raw, bold, unconventional, geometric | High contrast, monospace, sharp corners | Creative agencies, art | Conservative |
| **Y2K Revival** | Metallic, chrome, retro-futuristic | Chrome gradients, bold colors | Gen Z brands, experimental | Corporate |
| **Claymorphism** | 3D inflated, soft shadows, playful | Multi-layer box-shadows, extreme border-radius | Task apps, consumer tools | Data-heavy |
| **Gradient Mesh** | Complex multi-color, organic flow | Multi-stop animated gradients | Hero sections, backgrounds | Text-heavy |
| **Minimalist Luxury** | Maximum white space, serif, gold accents | Generous padding, thin serifs | Fashion, premium services | Budget brands |
| **Cyberpunk** | Neon colors, glitch, tech-noir | CSS glitch, neon glows, high energy | Gaming, crypto | Professional |
| **Organic/Biomorphic** | Nature-inspired, earth tones, flowing | SVG organic shapes, earth palette | Wellness, sustainability | Tech/corporate |

---

## DIMENSION 3: COLOR & THEME

### Color Psychology Palettes

#### Trust & Professionalism (Finance, Healthcare, Enterprise)
```css
--primary: #0F172A    /* Navy */
--cta: #0369A1        /* Blue */
--background: #F8FAFC /* Light Grey */
--text: #1E293B       /* Slate */
--accent: #3B82F6     /* Bright Blue */
Mood: Reliable, secure, established
```

#### Vibrant & Modern (Tech Startups, Creative Tools)
```css
--primary: #6366F1    /* Indigo */
--cta: #10B981        /* Emerald */
--background: #FFFFFF /* Pure White */
--text: #1E293B       /* Slate */
--accent: #F59E0B     /* Amber */
Mood: Innovative, energetic, forward-thinking
```

#### Luxury & Premium (High-end Products, Fashion)
```css
--primary: #1C1917    /* Stone Dark */
--cta: #CA8A04        /* Gold */
--background: #FAFAF9 /* Cream */
--text: #292524       /* Warm Black */
--accent: #78716C     /* Taupe */
Mood: Sophisticated, exclusive, timeless
```

#### Healthcare/Wellness (Medical, Fitness, Mental Health)
```css
--primary: #0891B2    /* Cyan */
--cta: #059669        /* Health Green */
--background: #FFFFFF /* Clean White */
--text: #0F172A       /* Deep Blue */
--accent: #06B6D4     /* Bright Cyan */
Mood: Calm, trustworthy, clean
```

#### Creative/Playful (Consumer Apps, Entertainment)
```css
--primary: #EC4899    /* Pink */
--cta: #8B5CF6        /* Purple */
--background: #FEF3C7 /* Warm Cream */
--text: #1F2937       /* Charcoal */
--accent: #F59E0B     /* Orange */
Mood: Fun, approachable, energetic
```

#### Dark Mode Excellence
```css
--background: #0A0A0A     /* True Black */
--surface: #1A1A1A        /* Card Background */
--border: #333333         /* Subtle Borders */
--text: #FFFFFF            /* Pure White */
--text-secondary: #A3A3A3 /* Grey */
--accent: #3B82F6         /* Blue */
Contrast ratio: 15:1 for text
```

### Color System Rules
- Use **60-30-10 rule** (60% dominant, 30% secondary, 10% accent)
- Ensure **WCAG AA compliance** (4.5:1 for text)
- Create **semantic tokens** (`--color-success`, `--color-error`)
- Test in both light and dark modes
- Never more than 3 primary colors
- Never pure black on pure white (too harsh)

---

## DIMENSION 4: TYPOGRAPHY

### Font Pairings by Brand Voice

| Personality | Headings | Body | Mono | Use For |
|-------------|----------|------|------|---------|
| **Modern/Tech** | Inter (Variable) | Roboto / System UI | JetBrains Mono | SaaS, developer tools |
| **Elegant/Luxury** | Playfair Display | Montserrat | — | Fashion, premium services |
| **Friendly/Consumer** | Poppins | Open Sans | — | Apps, e-commerce |
| **Brutalist/Bold** | Space Grotesk | JetBrains Mono / IBM Plex | — | Creative agencies, art |
| **Editorial/Content** | Merriweather | Source Sans Pro | — | Blogs, news |

### Typography Rules
- Max 2 font families per site
- Use font weight contrast (light headings + regular body, or bold headings + light body)
- Line height: 1.5-1.6 for body, 1.1-1.2 for headings
- Letter spacing: tight for headings (-0.02em), normal for body
- Font sizes: use a modular scale (1.25x or 1.333x)

---

## DIMENSION 5: ANIMATIONS & INTERACTIONS

### Micro-Interactions

#### Button Effects
```
Hover: scale(1.02), translateY(-2px), shadow increase
Tap: scale(0.98), 150ms duration
Timing: cubic-bezier(0.4, 0, 0.2, 1)
Border beam: Animated gradient border (Linear-style)
Glow: Outer glow on hover with brand color
```

#### Input Focus
```
Ring: 2-4px outline with brand color at 50% opacity
Glow: Soft box-shadow with brand color
Border shift: Color change + subtle scale
Label float: Animated label moving up on focus
Always visible focus indicators (accessibility)
```

#### Card Hover
```
Lift + Shadow: translateY(-4px) + shadow increase
Tilt: 3D perspective tilt (subtle, 2-3deg)
Glow border: Animated gradient border reveal
Image zoom: Scale 1.05x inside container
Content reveal: Hidden content slides in on hover
```

### Scroll Animations

#### Reveal on Scroll
```
Fade up: opacity 0→1 + translateY(20px→0)
Stagger delay: 100ms between elements
Trigger: When element is 20% in viewport
Duration: 600ms, easing: ease-out
```

#### Parallax
```
Hero background: Scroll speed 0.5x
Foreground elements: Scroll speed 1.2x
Max movement: 20-30px (subtle only)
Performance: Use transform, not position
```

#### Progress Indicators
```
Top bar: Fixed position, width based on scroll %
Circular: SVG circle with stroke-dashoffset
Smooth: transition: width 100ms linear
```

### Page Transitions
```
Fade: opacity 200ms
Slide: translateX(-100%→0) 300ms
Blur: filter: blur(0→10px→0)
Modal: backdrop 200ms + content scale(0.95→1) 300ms
```

### Loading States
```
Skeleton: Shimmer gradient animation, 1.5s infinite
Spinner: Rotating circle with gradient
Pulse: Scale + opacity animation
Match final content layout shape
```

### Advanced Effects
```
Border beams: Animated gradient border (Linear/Vercel style)
Mesh gradients: Multi-color gradient, slow hue rotation 60s+
Glassmorphism: backdrop-filter: blur(10px) saturate(180%)
```

### Animation Performance Rules
- **DO**: Use `transform` and `opacity` (GPU accelerated), set `will-change`, use `requestAnimationFrame`, debounce scroll events, prefer CSS over JS, test on low-end devices
- **DON'T**: Animate width/height/position, animations >500ms for interactions, animate during user input, too many simultaneous animations, forget `prefers-reduced-motion`, animate on scroll without throttling

---

## ANTI-PATTERNS (Tell Agent What NOT to Do)

### Design Anti-Patterns
```
❌ Flash Over Function — no animations blocking user action
❌ Low Contrast — no #CCC on white, ensure 4.5:1 minimum
❌ Over-Cluttered — no more than 3 colors, 2 fonts, 5 sizes
❌ Mystery Meat Nav — icons must have labels, no hamburger on desktop
❌ Mobile Hostility — min 44x44px tap targets, no hover-dependent
❌ Performance Sins — no unoptimized images, no CLS > 0.1
```

### UX Anti-Patterns
```
❌ Form Frustrations — labels outside inputs, validate on blur not submit
❌ Content Crimes — no walls of text, no auto-playing carousels
❌ Accessibility Failures — no keyboard traps, no missing alt text
```

---

## PROMPT TEMPLATE (Copy-Paste for AI Agents)

```
Create a [PRODUCT TYPE] website with:

LAYOUT: [Pattern from Dimension 1]
STYLE: [Style from Dimension 2]
COLORS: [Palette from Dimension 3]
TYPOGRAPHY: [Pairing from Dimension 4]
ANIMATIONS: [Effects from Dimension 5]

DO NOT: [Anti-patterns to avoid]

The site should feel like [REFERENCE SITE] but for [YOUR PRODUCT].
```
