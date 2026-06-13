"use client"

import { useRef } from "react"
import { motion, useScroll, useTransform } from "motion/react"

/**
 * Apple-Level Scrollytelling Product Showcase
 * 
 * Architecture:
 * - Sticky canvas pinned with position: sticky inside a 400vh container
 * - Scroll-linked frame playback: frameIndex = scrollProgress * totalFrames
 * - Background color matches frame backgrounds for seamless blending
 * - Text overlays appear/disappear at scroll thresholds
 * 
 * Usage:
 * 1. Generate image sequence using Google Whisk (AI image gen)
 * 2. Convert video to frames using EZGif (30 FPS, JPG)
 * 3. Place frames in /public/frames/ directory
 * 4. Adjust FRAME_COUNT to match your frame count
 */

const FRAME_COUNT = 120 // Total frames in your sequence
const STORY_BEATS = [
  { start: 0, end: 0.15, label: "hero" },
  { start: 0.15, end: 0.4, label: "engineering" },
  { start: 0.4, end: 0.65, label: "technology" },
  { start: 0.65, end: 0.85, label: "sound" },
  { start: 0.85, end: 1, label: "cta" },
]

export default function ProductScrollytelling() {
  const containerRef = useRef<HTMLDivElement>(null)
  const canvasRef = useRef<HTMLDivElement>(null)

  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"],
  })

  // Map scroll progress to frame index
  const frameIndex = useTransform(scrollYProgress, [0, 1], [0, FRAME_COUNT - 1])

  // Text section opacities
  const heroOpacity = useTransform(scrollYProgress, [0, 0.1, 0.15], [1, 1, 0])
  const heroY = useTransform(scrollYProgress, [0, 0.15], [0, -50])

  const engineeringOpacity = useTransform(scrollYProgress, [0.12, 0.15, 0.35, 0.4], [0, 1, 1, 0])
  const engineeringX = useTransform(scrollYProgress, [0.12, 0.2], [-100, 0])

  const techOpacity = useTransform(scrollYProgress, [0.37, 0.4, 0.6, 0.65], [0, 1, 1, 0])
  const techX = useTransform(scrollYProgress, [0.37, 0.45], [100, 0])

  const soundOpacity = useTransform(scrollYProgress, [0.62, 0.65, 0.8, 0.85], [0, 1, 1, 0])
  const soundY = useTransform(scrollYProgress, [0.62, 0.7], [50, 0])

  const ctaOpacity = useTransform(scrollYProgress, [0.82, 0.85], [0, 1])
  const ctaScale = useTransform(scrollYProgress, [0.82, 0.9], [0.95, 1])

  return (
    <div ref={containerRef} className="relative" style={{ height: "500vh" }}>
      {/* Sticky Canvas Container */}
      <div className="sticky top-0 h-screen overflow-hidden" style={{ background: "#050505" }}>
        {/* Image Sequence Canvas */}
        <ImageSequenceCanvas frameIndex={frameIndex} />

        {/* Hero Text (0-15%) */}
        <motion.div
          style={{ opacity: heroOpacity, y: heroY }}
          className="absolute inset-0 flex flex-col items-center justify-center text-center z-10 pointer-events-none"
        >
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-sm font-mono tracking-widest text-[#00D6FF] mb-6 uppercase"
          >
            Flagship Wireless Noise Cancelling
          </motion.p>
          <h1 className="text-6xl md:text-8xl font-bold tracking-tight text-white/90">
            Product Name
          </h1>
          <p className="mt-6 text-xl text-white/60 max-w-lg">
            Silence, perfected.
          </p>
        </motion.div>

        {/* Engineering Section (15-40%) */}
        <motion.div
          style={{ opacity: engineeringOpacity, x: engineeringX }}
          className="absolute left-8 md:left-24 top-1/2 -translate-y-1/2 max-w-md z-10 pointer-events-none"
        >
          <p className="text-xs font-mono tracking-widest text-[#0050FF] mb-4 uppercase">
            01. Engineering
          </p>
          <h2 className="text-3xl md:text-5xl font-bold text-white/90 tracking-tight leading-tight">
            Precision-engineered for silence.
          </h2>
          <p className="mt-4 text-sm text-white/50 leading-relaxed">
            Custom drivers, sealed acoustic chambers, and optimized airflow
            deliver studio-grade clarity. Every component is tuned for balance,
            power, and comfort—hour after hour.
          </p>
        </motion.div>

        {/* Technology Section (40-65%) */}
        <motion.div
          style={{ opacity: techOpacity, x: techX }}
          className="absolute right-8 md:right-24 top-1/2 -translate-y-1/2 max-w-md z-10 pointer-events-none text-right"
        >
          <p className="text-xs font-mono tracking-widest text-[#00D6FF] mb-4 uppercase">
            02. Technology
          </p>
          <h2 className="text-3xl md:text-5xl font-bold text-white/90 tracking-tight leading-tight">
            Adaptive noise cancelling, redefined.
          </h2>
          <div className="mt-4 space-y-2 text-sm text-white/50">
            <p>Multi-microphone array listens in every direction.</p>
            <p>Real-time noise analysis adjusts to your environment.</p>
            <p>Your music stays pure—planes, trains, and crowds fade away.</p>
          </div>
        </motion.div>

        {/* Sound Section (65-85%) */}
        <motion.div
          style={{ opacity: soundOpacity, y: soundY }}
          className="absolute left-1/2 -translate-x-1/2 bottom-24 max-w-lg text-center z-10 pointer-events-none"
        >
          <p className="text-xs font-mono tracking-widest text-[#0050FF] mb-4 uppercase">
            03. Sound
          </p>
          <h2 className="text-3xl md:text-5xl font-bold text-white/90 tracking-tight leading-tight">
            Immersive, lifelike sound.
          </h2>
          <p className="mt-4 text-sm text-white/50 leading-relaxed">
            High-performance drivers unlock detail, depth, and texture in every
            track. AI-enhanced upscaling restores clarity to compressed audio.
          </p>
        </motion.div>

        {/* CTA Section (85-100%) */}
        <motion.div
          style={{ opacity: ctaOpacity, scale: ctaScale }}
          className="absolute inset-0 flex flex-col items-center justify-center text-center z-10 pointer-events-none"
        >
          <h2 className="text-5xl md:text-7xl font-bold tracking-tight text-white/90">
            Hear everything.
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#0050FF] to-[#00D6FF]">
              Feel nothing else.
            </span>
          </h2>
          <p className="mt-6 text-lg text-white/50">
            Designed for focus, crafted for comfort.
          </p>
          <div className="mt-8 flex gap-4 pointer-events-auto">
            <button className="px-8 py-3 bg-gradient-to-r from-[#0050FF] to-[#00D6FF] text-white font-semibold rounded-lg hover:opacity-90 transition-opacity">
              Experience Now
            </button>
            <button className="px-8 py-3 border border-white/20 text-white rounded-lg hover:bg-white/5 transition-colors">
              See Specs
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

/**
 * Image Sequence Canvas Component
 * 
 * Renders frames from /public/frames/ directory.
 * Frame naming convention: frame-001.jpg, frame-002.jpg, ..., frame-120.jpg
 * 
 * To generate frames:
 * 1. Use Google Whisk to generate product images
 * 2. Use Google Veo Flow to animate between frames
 * 3. Use EZGif to extract frames at 30 FPS
 * 4. Download as ZIP and extract to /public/frames/
 */
function ImageSequenceCanvas({ frameIndex }: { frameIndex: any }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const imagesRef = useRef<HTMLImageElement[]>([])

  // Preload frames
  // In production, use useMotionValueEvent to reactively draw frames
  // For now, this is a placeholder showing the architecture

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 w-full h-full"
      style={{ background: "#050505" }}
    />
    /*
     * Implementation:
     * 1. Preload all FRAME_COUNT images into imagesRef
     * 2. useMotionValueEvent(frameIndex, "change", (latest) => {
     *      const ctx = canvasRef.current?.getContext("2d")
     *      const img = imagesRef.current[Math.round(latest)]
     *      if (ctx && img) ctx.drawImage(img, 0, 0, width, height)
     *    })
     * 3. Handle resize for responsive canvas sizing
     */
  )
}
