# Astro Website Starterkit — Design System & Patterns

> Source: Vibecoded Website Starterkit v110 by Albert Bozesan
> Astro framework, "Barely-there UI" design philosophy

---

## PHILOSOPHY: "BARELY-THERE UI" WITH CONTROLLED BOLDNESS

Minimal chrome, let content breathe. Subtle borders, low-contrast secondary elements, high-contrast focal points. Negative space as a design element.

---

## DESIGN TOKENS

### Colors
```css
--bg: #1a1a1a;
--bg-elevated: #242424;
--bg-card: #2a2a2a;
--text: #ffffff;
--text-muted: rgba(255, 255, 255, 0.6);
--accent: #3b82f6;
--accent-hover: #60a5fa;
```

### Typography
```css
/* Clean modern */
--font-display: 'Inter', system-ui, sans-serif;
--font-body: 'Inter', system-ui, sans-serif;

/* Hierarchy */
h1: clamp(2.5rem, 8vw, 5rem), weight 700
h2: clamp(1.75rem, 4vw, 2.5rem), weight 700
h3: 1.25rem, weight 700
Body: 1rem, line-height 1.6
Small/Tags: 0.75rem, uppercase, letter-spacing 0.08em
```

### Spacing Scale
```css
--space-xs: 0.5rem;   /* 8px */
--space-sm: 1rem;     /* 16px */
--space-md: 1.5rem;   /* 24px */
--space-lg: 3rem;     /* 48px */
--space-xl: 6rem;     /* 96px */
```

### Animation
```css
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);
--transition-fast: 0.2s var(--ease-out);
--transition: 0.4s var(--ease-out);
```

### Border Radius
- Cards: 16px
- Buttons/pills: 100px (fully rounded)
- Small elements: 4px or 8px

---

## KEY COMPONENT PATTERNS

### 1. Glass Border Effect (Conic Gradient)
```css
.element {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
}

.element::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1px;
  background: conic-gradient(
    from 45deg,
    rgba(255, 255, 255, 0.15) 0deg,
    rgba(255, 255, 255, 0.03) 45deg,
    rgba(255, 255, 255, 0.15) 90deg,
    rgba(255, 255, 255, 0.03) 135deg,
    rgba(255, 255, 255, 0.15) 180deg,
    rgba(255, 255, 255, 0.03) 225deg,
    rgba(255, 255, 255, 0.15) 270deg,
    rgba(255, 255, 255, 0.03) 315deg,
    rgba(255, 255, 255, 0.15) 360deg
  );
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  pointer-events: none;
  z-index: 2;
}
```

### 2. Cursor-Following Image Zoom
```javascript
// Track cursor position → set transform-origin
card.addEventListener('mousemove', (e) => {
  const rect = card.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 100;
  const y = ((e.clientY - rect.top) / rect.height) * 100;
  img.style.transformOrigin = `${x}% ${y}%`;
});

card.addEventListener('mouseleave', () => {
  img.style.transformOrigin = 'center center';
});
```

```css
.card-img {
  transition: transform 0.4s var(--ease-out), transform-origin 0.8s ease-out;
}
.card:hover .card-img {
  transform: scale(1.05);
}
```

### 3. Card Hover States
```css
.card:hover {
  transform: scale(1.02);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.25);
}
```

### 4. Fullscreen Modal (Native Dialog)
```css
dialog::backdrop {
  background: rgba(0, 0, 0, 0);
  backdrop-filter: blur(0px);
  animation: backdrop-fade-in 0.4s var(--ease-out) forwards;
}

@keyframes backdrop-fade-in {
  to {
    background: rgba(0, 0, 0, 0.95);
    backdrop-filter: blur(20px);
  }
}
```

### 5. Background Blur
```css
filter: blur(20px) brightness(0.3);  /* on fixed background */
backdrop-filter: blur(8px);          /* on floating UI elements */
```

### 6. Card Overlay Gradient (Text Protection)
```css
background: linear-gradient(
  to top,
  rgba(0, 0, 0, 0.95) 0%,
  rgba(0, 0, 0, 0.85) 25%,
  rgba(0, 0, 0, 0.4) 50%,
  transparent 75%
);
```

### 7. Divider Lines
```css
background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
```

---

## 2026 DESIGN TRENDS (From GUIDE-CC.md)

### Barely-There UI
- Minimal chrome, let content breathe
- Subtle borders using glass effects (conic gradients with mask compositing)
- Low-contrast secondary elements, high-contrast focal points
- Negative space as a design element

### Depth Without Skeuomorphism
- Layered surfaces with slight elevation differences
- Backdrop blur on floating elements
- Soft, diffused shadows (large blur radius, low opacity)
- Background blur behind hero sections

### Responsive Motion
- Cursor-following interactions (transform-origin follows mouse)
- Smooth easing: `cubic-bezier(0.16, 1, 0.3, 1)`
- Scale transforms on hover (1.02-1.05)
- Staggered animations for lists/grids

### Glass Morphism (Modern)
- Conic gradient borders with brighter corners
- CSS mask compositing for border-only effects
- Semi-transparent backgrounds with blur
- Works on both light and dark themes

### Typography
- Fluid type scaling with `clamp()`
- Clear hierarchy (3-4 distinct levels max)
- Generous line-height (1.5-1.7)
- Letter-spacing on small/uppercase text

### Dark Mode First
- Dark backgrounds reduce eye strain
- Accent colors pop more on dark
- Light mode as option, not default

---

## DATA ARCHITECTURE (Astro + JSON)

Content as JSON arrays in `src/data/`:
```json
[
  {
    "slug": "my-post",
    "title": "My Post",
    "date": "2024-06-15",
    "excerpt": "A short description.",
    "image": "/images/posts/my-post.jpg",
    "tags": ["design", "web"]
  }
]
```

Benefits: human-readable, easy filtering, no build-time parsing, simple migrations.

### Best For
- Portfolios, small business sites, landing pages
- Content that changes monthly or less
- Developer-maintained sites

### For Active Blogs
Use Astro Content Collections instead:
- Markdown files in `src/content/`
- Frontmatter-based metadata
- Native RSS support
- Headless CMS integration (Decap, Tina, Sanity)

---

## SEO CHECKLIST (Every Site)

1. Meta tags in layout head
2. Structured data (JSON-LD) for posts/articles
3. Sitemap via `@astrojs/sitemap`
4. Canonical URLs
5. Open Graph / Twitter cards
6. Robots.txt

---

## PERFORMANCE PRIORITIES

1. **Images**: Use Astro `<Image />`, lazy load below-fold, provide width/height
2. **CSS**: Scoped component styles, minimal global, no CSS-in-JS runtime
3. **JavaScript**: Astro islands, vanilla JS over frameworks, no hydration unless necessary

---

## STABILITY CHECKLIST

- [ ] All pages render without errors
- [ ] Build completes (`npm run build`)
- [ ] No TypeScript errors
- [ ] Images optimized + lazy-loaded
- [ ] SEO meta tags on all pages
- [ ] Sitemap generates correctly
- [ ] 404 page exists
- [ ] Mobile responsive (375px, 768px, 1024px, 1440px)
- [ ] Keyboard navigation works
- [ ] No console errors
- [ ] Lighthouse 90+ on all metrics

---

## FILE NAMING CONVENTIONS

- Components: `PascalCase.astro`
- Pages: `kebab-case.astro` or `[slug].astro`
- Data files: `camelCase.json`
- Styles: `kebab-case.css`
- Images: `kebab-case.jpg`

---

## YOUTUBE NO-COOKIE VIDEO MODAL

- Single `GlobalVideoModal.astro` component in base layout
- Event delegation catches all YouTube link clicks
- Extracts video IDs from youtu.be, youtube.com/watch, /embed/
- Uses `youtube-nocookie.com` (Enhanced Privacy Mode)
- Desktop (>768px): native `<dialog>` modal with autoplay
- Mobile (<=768px): opens YouTube in new tab
- Clears iframe `src` on close to stop playback

---

## CONTACT FORMS (Formspree)

Static sites have no backend — use Formspree:
```html
<form action="https://formspree.io/f/{form_id}" method="POST">
  <input name="email" type="email" required />
  <textarea name="message" required></textarea>
  <button type="submit">Send</button>
</form>
```
