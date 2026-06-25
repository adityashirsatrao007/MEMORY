# Implementation Plan — Pinned Multi-Section 3D Scrollytelling

Expand the scroll layout and visual depth of the CampusSync 3D homepage (port 3002) to create a longer, slower, and incredibly smooth narrative journey.

## Proposed Changes

### 1. Pinned Scrollytelling Layout Architecture
- Convert the natural scrolling layout into a **pinned canvas + text card stack**.
- The main scrolly container will have a scroll height of `500vh` (5 scroll viewports).
- The text sections will fade in and out at the center-left/center-right of the screen while pinned, ensuring the user stays focused on the 3D canvas transitions in the background.
- Extend the GSAP timeline scrub values for a much slower, smoother transition.

### 2. Expanded 3D Narrative Sections
- **Section 1: Hero Telemetry (0% - 20% scroll)**: Holographic network intro, camera pans downward.
- **Section 2: Node Triangulation (20% - 40% scroll)**: Floating connection lines link the nodes, camera moves closer.
- **Section 3: Morphing Data Terrain (40% - 60% scroll)**: Holographic grid morphs into a dynamic waving data mountain, camera rotates to an angled perspective.
- **Section 4: Dispatcher Control Desk (60% - 80% scroll)**: Dashboard plane aligns to face the user, glowing edge scans.
- **Section 5: SOS Alert Activation (80% - 100% scroll)**: Beacon scales up, particles rotate rapidly, background ambient color pulses red.

### 3. Smooth Scrolling Physics
- Integrate standard smooth scrolling physics (or increase GSAP scrub duration to `2.5s` and add custom momentum handling) to make scrolling feel buttery smooth.

#### [MODIFY] [App.jsx](file:///home/aditya/Desktop/Projects/MEMORY/campussync/src/App.jsx)
- Update JSX layout to wrap text panels in absolute positions, allowing them to fade over the pinned background.
- Expand Three.js meshes: Add custom line paths (wireframe links) connecting the random floating nodes.
- Extend GSAP timeline (`tl`) to cover the 5 distinct phases with precise scroll durations.
- Add an ambient color shift (changing scene background/lights to alert states) on scroll trigger.

## Verification Plan

### Manual Verification
- Scroll through the homepage to verify:
  1. The text sections fade in/out smoothly and do not overlap.
  2. The 3D scene rotates, pans, and morphs at a slow, premium pace.
  3. Parallax mouse tracking stays active throughout the entire scroll.
