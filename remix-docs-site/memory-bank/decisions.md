# Remix Docs Site — Decisions Log

## 1. Framework-less Static Core with Express Server
- **Decision:** Use vanilla HTML, CSS, and JS served by a lightweight Node/Express server instead of full framework systems like Next.js or Remix itself for this showcase.
- **Rationale:** Minimizes bundle overhead, loads instantly, and cleanly demonstrates the raw design tokens and custom micro-interactions (keyboard modal loops, spotlight proximity cards) without build-tool complications. Express allows us to satisfy production API requirements (graceful shutdown, CSP, HSTS, CORS, and `/health` + `/ready` endpoints) in a few lines of self-contained code.

## 2. Vanilla CSS Design Tokens
- **Decision:** Use native CSS custom properties (`--color-text-tertiary`, etc.) rather than Tailwind utility frameworks.
- **Rationale:** Ensures complete customization control, reduces external stylesheet weight, and aligns with the user's styling rules preferring vanilla CSS for flexibility.

## 3. Git Hooks Gitleaks Flag Compatibility Patch
- **Decision:** Remove the `-q` flag from the gitleaks shell checker within `.git/hooks/pre-commit`.
- **Rationale:** The system-wide `gitleaks` version failed with exit status `1` when reading `-q` (flag not recognized), which blocked valid git commits. Removing it resolved the execution pipeline error.

## 4. Text Content Contrast & Textures
- **Decision:** Apply a dynamic radial mask gradient spotlight card inside nested layouts, and overlay a global high-performance SVG turbulence noise filter.
- **Rationale:** Eliminates flat gradients, giving the developer-focused dark mode a tactile, premium surface texture while maintaining WCAG 2.2 AA contrast compliance.
