# Motion.dev — Animation Library Reference

> Source: https://motion.dev | MIT License | v12.40.0
> 370+ copy-paste examples for React, JavaScript, Vue

## Installation
```bash
bun add motion
# or
npm install motion
```

## Import
```tsx
import { motion, AnimatePresence, useScroll, useTransform, useSpring, useMotionValue, stagger } from "motion/react"
```

---

## CORE PATTERNS (Use in Every Project)

### 1. Scroll-Linked Hero Zoom
```tsx
"use client"
import { useRef } from "react"
import { motion, useScroll, useTransform } from "motion/react"

export function ScrollHero() {
  const ref = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] })
  const scale = useTransform(scrollYProgress, [0, 1], [1, 1.5])
  const opacity = useTransform(scrollYProgress, [0, 0.8], [1, 0])
  const blur = useTransform(scrollYProgress, [0, 1], [0, 10])

  return (
    <div ref={ref} className="h-[200vh]">
      <motion.div
        style={{ scale, opacity, filter: useTransform(blur, v => `blur(${v}px)`) }}
        className="sticky top-0 h-screen flex items-center justify-center"
      >
        <h1 className="text-7xl font-bold text-white">Hero Content</h1>
      </motion.div>
    </div>
  )
}
```

### 2. Staggered Fade-In List
```tsx
"use client"
import { motion } from "motion/react"

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

export function StaggerList({ items }: { items: string[] }) {
  return (
    <motion.ul variants={container} initial="hidden" whileInView="show" viewport={{ once: true }}>
      {items.map((text, i) => (
        <motion.li key={i} variants={item} className="text-white/80">
          {text}
        </motion.li>
      ))}
    </motion.ul>
  )
}
```

### 3. Magnetic Button (Hover + Tap)
```tsx
"use client"
import { motion } from "motion/react"

export function MagneticButton({ children }: { children: React.ReactNode }) {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      transition={{ type: "spring", stiffness: 400, damping: 17 }}
      className="px-6 py-3 bg-white/10 text-white rounded-lg border border-white/20"
    >
      {children}
    </motion.button>
  )
}
```

### 4. Parallax Scroll Sections
```tsx
"use client"
import { useRef } from "react"
import { motion, useScroll, useTransform } from "motion/react"

export function ParallaxSection() {
  const ref = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] })
  const y = useTransform(scrollYProgress, [0, 1], ["-20%", "20%"])

  return (
    <div ref={ref} className="relative h-screen overflow-hidden">
      <motion.div style={{ y }} className="absolute inset-0">
        <img src="/hero.jpg" className="w-full h-full object-cover" alt="" />
      </motion.div>
      <div className="relative z-10 flex items-center justify-center h-full">
        <h2 className="text-5xl font-bold text-white">Parallax Content</h2>
      </div>
    </div>
  )
}
```

### 5. Text Reveal on Scroll
```tsx
"use client"
import { useRef } from "react"
import { motion, useInView } from "motion/react"

export function TextReveal({ text }: { text: string }) {
  const ref = useRef<HTMLDivElement>(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })

  return (
    <div ref={ref} className="overflow-hidden">
      <motion.p
        initial={{ y: "100%" }}
        animate={isInView ? { y: 0 } : {}}
        transition={{ duration: 0.8, ease: [0.33, 1, 0.68, 1] }}
        className="text-4xl font-bold text-white"
      >
        {text}
      </motion.p>
    </div>
  )
}
```

### 6. Spring Physics Animation
```tsx
"use client"
import { motion } from "motion/react"

export function SpringCard() {
  return (
    <motion.div
      whileHover={{ y: -8, boxShadow: "0 20px 40px rgba(0,0,0,0.3)" }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className="p-6 bg-white/5 border border-white/10 rounded-xl"
    >
      <h3 className="text-white font-semibold">Spring Card</h3>
    </motion.div>
  )
}
```

### 7. AnimatePresence (Mount/Unmount)
```tsx
"use client"
import { useState } from "react"
import { motion, AnimatePresence } from "motion/react"

export function TogglePanel() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <button onClick={() => setOpen(!open)} className="text-white">Toggle</button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="p-4 bg-white/5 rounded-lg text-white">Panel content</div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
```

### 8. Scroll-Triggered Image Reveal
```tsx
"use client"
import { useRef } from "react"
import { motion, useScroll, useTransform } from "motion/react"

export function ImageReveal() {
  const ref = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start 80%", "end 20%"] })
  const clipPath = useTransform(scrollYProgress, [0, 1], ["inset(0 100% 0 0)", "inset(0 0% 0 0)"])

  return (
    <div ref={ref} className="relative h-[60vh]">
      <motion.img
        src="/product.jpg"
        style={{ clipPath }}
        className="w-full h-full object-cover"
        alt=""
      />
    </div>
  )
}
```

---

## COMPONENT CATEGORIES (372 total)

| Category | Count | Key Examples |
|----------|-------|-------------|
| **Basics** | 97 | State updates, keyframes, transitions, gestures, variants |
| **Scroll** | 10 | Hide header, horizontal gallery, image reveal, text lines, zoom hero |
| **Text** | 35 | Split text, typewriter, scramble, wavy, reveal, scatter |
| **Ticker** | 18 | Infinite scroll, draggable, cursor, RTL, vertical, text hover |
| **Carousel** | 30 | Loop, autoplay, coverflow, parallax, pagination, lightbox |
| **Cursor** | 24 | Magnetic, follow, trail, custom content, floating target |
| **Buttons** | 12 | Floating action, dots morph, copy, create |
| **Loading** | 23 | Spinner, progress bar, ripple, line reveal, dots pulse |
| **Layout** | 10 | Layout animation, shared layout, reorder, anchor |
| **Lists** | 8 | Reorder items, staggered grid |
| **Navigation** | 10 | Mega menu, context menu, radial menu |
| **Dialog** | 11 | Modal, sheet, command palette |
| **Forms** | 9 | Checkbox, switch, tabs, toast, tooltip |
| **Radix** | 30 | All Radix primitives animated |
| **Base UI** | 13 | All Base UI primitives animated |
| **Experimental** | 10 | iOS app folder, iOS pointer, Apple Watch |

---

## KEY APIs

| API | Purpose | When to Use |
|-----|---------|-------------|
| `motion.div` | Animated element | Any element that needs animation |
| `AnimatePresence` | Exit animations | Modal, toast, panel mount/unmount |
| `useScroll` | Scroll progress | Parallax, scroll-linked effects |
| `useTransform` | Map values | Convert scroll progress to any value |
| `useSpring` | Spring physics | Smooth following, natural motion |
| `useMotionValue` | Raw value | Drive animations imperatively |
| `useInView` | Viewport detection | Trigger on scroll into view |
| `stagger` | Stagger children | List animations, card reveals |
| `variants` | Named states | Parent-child orchestration |
| `layout` | Layout animation | Shared layout, morphing |
| `whileHover` | Hover gesture | Button, card hover effects |
| `whileTap` | Tap gesture | Button press feedback |
| `whileInView` | Scroll trigger | Fade in on scroll |
| `whileDrag` | Drag gesture | Drag and drop, swipe |

---

## TRANSITION PRESETS

```tsx
// Spring (natural, physics-based)
transition={{ type: "spring", stiffness: 300, damping: 20 }}

// Tween (duration-based)
transition={{ duration: 0.5, ease: "easeOut" }}

// Custom bezier
transition={{ duration: 0.4, ease: [0.33, 1, 0.68, 1] }}

// Stagger children
transition={{ staggerChildren: 0.1 }}

// Spring with delay
transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.2 }}
```
