# Walkthrough — Pinned 3D Scrollytelling Visual Expansion

Expanded the scrolling layout into a multi-phase, pinned 3D storytelling journey.

## Features Implemented

### 1. Pinned Text Overlay Transitions
- Re-architected the layout to a pinned layout where the scrolly section spans `500vh`.
- Positioned 5 distinct narrative slides absolutely inside the viewport, fading them in/out dynamically on scroll while keeping the canvas visible in the background.

### 2. Laser Mesh Network Connections
- Added laser connection lines (`LineSegments`) linking floating nodes that are within `4.5` units of each other, creating a live 3D mesh network representation.

### 3. Emergency SOS Red Alert Shakes
- Added `redAlertLight` (PointLight). On Phase 5 (SOS section), the timeline pushes its intensity up, shifting ambient colors to red and triggering emergency camera vibrations in the loop.

### 4. Apple System Font Stacks
- Updated `index.css` to fall back to `Inter`, `SF Pro Display`, and standard Apple HIG font stacks.

## Verification

- Built project successfully (`npm run build`).
- Local dev server is serving active HMR on port 3002.
