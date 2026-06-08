# 4 Types of Website Scrolling Patterns

> Source: UXPin (2026) — https://www.uxpin.com/studio/blog/4-types-creative-website-scrolling-patterns/

---

## PATTERN 1: Long Scrolling

All content on a single continuous page. Users scroll down through sections sequentially — no clicks needed.

**When to use:**
- Storytelling and narrative content (case studies, product launches, brand stories)
- Landing pages with a single conversion goal
- Mobile-first designs (scrolling is primary interaction)
- Single-page applications with sequential content flow

**Best practices:**
- Chunk content visually — distinct sections with headings, background color changes, or horizontal rules
- Provide orientation cues — sticky nav, progress indicators, "back to top" button
- Front-load value — most important content + CTA above the fold
- Lazy load images and defer off-screen content

**Gold standard:** Apple product pages — each section reveals a feature with bold visuals and minimal text.

**Implementation (Motion.dev):**
```tsx
// Simple long scroll with staggered reveals
<motion.section initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }}>
  {/* Section content */}
</motion.section>
```

---

## PATTERN 2: Fixed Long Scrolling (Sticky)

Long scroll + fixed/pinned elements (headers, sidebars, CTAs) that stay visible as user scrolls.

**When to use:**
- Documentation/tutorial pages where navigation must persist
- E-commerce product pages with persistent "Add to Cart"
- Dashboards and data-heavy interfaces
- Any long page where users need persistent access to key actions

**Best practices:**
- Keep fixed elements minimal — one sticky header/sidebar, not multiple competing elements
- Account for mobile — fixed elements consume more screen space on small devices
- Use scroll-triggered transitions — fixed elements can change state on scroll
- Respect accessibility — ensure fixed elements don't obscure content or break keyboard nav

**Gold standard:** React docs (fixed sidebar), SaaS pricing pages (pinned comparison header).

**Implementation (Motion.dev):**
```tsx
// Sticky header that appears on scroll
<motion.header
  initial={{ y: -100 }}
  animate={{ y: 0 }}
  transition={{ type: "spring", stiffness: 300, damping: 30 }}
  className="fixed top-0 left-0 w-full z-50 backdrop-blur-md bg-black/75"
>
  {/* Nav content */}
</motion.header>

// Pinned sidebar
<aside className="sticky top-24 h-fit">
  {/* Sidebar content */}
</aside>
```

---

## PATTERN 3: Infinite Scrolling

Automatically loads new content as user approaches bottom — no "next page" button.

**When to use:**
- Social media feeds and content discovery platforms
- Image/video galleries (Pinterest, Unsplash)
- News aggregators and blog indexes
- Browsing-focused contexts

**When NOT to use:**
- Goal-oriented tasks (e-commerce search, knowledge bases) — use pagination
- Pages with important footer links — users will never reach it
- SEO-critical pages — dynamic content may not be indexed without fallbacks

**Best practices:**
- Provide "Load More" alternative — explicit user control
- Implement SEO fallbacks — server-rendered HTML + pagination URLs
- Show loading indicators — skeleton screens or spinners
- Save scroll position — restore position when user navigates back

**Implementation (React):**
```tsx
// Intersection Observer based infinite scroll
useEffect(() => {
  const observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) loadMore()
  }, { threshold: 0.1 })
  if (loaderRef.current) observer.observe(loaderRef.current)
  return () => observer.disconnect()
}, [])

// With skeleton loading
{loading && <div className="animate-pulse bg-white/5 h-48 rounded-xl" />}
```

---

## PATTERN 4: Parallax Scrolling

Background and foreground layers move at different speeds — creates depth and dimensionality.

**When to use:**
- Brand storytelling and marketing sites
- Portfolio sites and creative showcases
- Product launch pages needing memorable first impression
- Interactive data visualizations and infographics

**When NOT to use:**
- Content-heavy pages where readability is priority
- Applications/dashboards where users work efficiently
- Accessibility-sensitive contexts — can trigger vestibular disorders

**Best practices:**
- CSS-only parallax where possible — `background-attachment: fixed`, `transform: translateZ()`
- Respect `prefers-reduced-motion` — always provide fallback
- Optimize assets — compress aggressively, use WebP/AVIF
- Simplify on mobile — disable or reduce effect on small screens
- Don't overdo it — one or two tasteful sections, not entire page

**Implementation (Motion.dev):**
```tsx
// Parallax background
const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] })
const y = useTransform(scrollYProgress, [0, 1], ["-30%", "30%"])

<motion.div style={{ y }} className="absolute inset-0">
  <img src="/bg.jpg" className="w-full h-[130%] object-cover" alt="" />
</motion.div>

// CSS-only parallax (no JS)
<div className="relative h-screen overflow-hidden">
  <div className="absolute inset-0 bg-fixed bg-cover bg-center" style={{ backgroundImage: "url(/bg.jpg)" }} />
  <div className="relative z-10">{/* Foreground content */}</div>
</div>
```

---

## DECISION MATRIX

| Factor | Long Scroll | Fixed Scroll | Infinite Scroll | Parallax |
|--------|-------------|--------------|-----------------|----------|
| **Best for** | Narrative, landing pages | Docs, e-commerce, dashboards | Feeds, galleries | Brand stories, portfolios |
| **Mobile** | Excellent | Good (with care) | Good | Use sparingly |
| **SEO** | High | High | Needs fallbacks | High |
| **Performance** | Low-Medium | Low | Medium | Medium-High |
| **Accessibility** | Good | Good | Needs a11y work | Needs motion fallbacks |

---

## COMBINED PATTERNS (Premium Sites Use 2-3 Together)

### Pattern Combos for Awwwards-Level Sites:
1. **Long Scroll + Parallax** — Apple product pages (narrative + depth)
2. **Fixed Scroll + Parallax** — Documentation with hero parallax (navigation + visual interest)
3. **Long Scroll + Fixed** — Landing page with sticky CTA (narrative + conversion)
4. **Fixed + Parallax + Scrollytelling** — Sony/Apple flagship product pages (all three combined)

### Implementation Rule:
> Never use infinite scroll on the same page as parallax — infinite scroll's auto-loading conflicts with parallax's precise scroll positions. Pick one or the other.
