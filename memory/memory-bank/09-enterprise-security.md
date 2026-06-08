## 🏗️ Enterprise Architecture & Scaling Protocols

This protocol defines the structural design patterns and scaling practices that must be adhered to for all enterprise-grade backend developments. Reference runnable code blueprints under `/home/aditya/bin/templates/architecture/`.

### 1. Microservices SAGA Pattern
- **When to Use:** Use when a transaction spans multiple physical microservices and requires distributed transactional consistency (atomic commitment) without blocking distributed locks.
- **Implementation Strategy (Orchestration):** Use a central orchestrator that guides transactions through sequential stages. Each stage has an execute function and a corresponding compensator (rollback) function.
- **Rule:** Every state-altering action must have a compensating action that returns the system to its prior state. If a compensator fails, log a `CRITICAL` alert with human intervention telemetry.
- **Blueprint:** [saga_orchestrator.py](file:///home/aditya/bin/templates/architecture/saga_orchestrator.py)

### 2. CQRS (Command Query Responsibility Segregation)
- **When to Use:** Use when there is a significant read/write asymmetry (e.g., reads outnumber writes by 100:1) or when query models differ heavily from command/write models.
- **Implementation Strategy:**
  - **Write Side (Commands):** Handles database modifications, validation, business rules, and writes to a write-optimized database (e.g., PostgreSQL).
  - **Read Side (Queries):** Reads from a read-optimized cache/database (e.g., Redis, Elasticsearch) with simplified flat data structures (views/DTOs).
  - **Sync:** Sync the read model asynchronously or synchronously after write success.
- **Blueprint:** [cqrs_fastapi.py](file:///home/aditya/bin/templates/architecture/cqrs_fastapi.py)

### 3. Event-Driven Architecture (EDA)
- **When to Use:** For decoupling services, handling long-running asynchronous tasks, and streaming telemetry/event data.
- **Implementation Strategy:**
  - **Event Envelope Pattern:** Always wrap event payloads in a structured envelope containing: `event_id`, `event_type`, `correlation_id` (tracks transactional thread across services), and `timestamp`.
  - **Resiliency & Retries:** Implement subscriber loops with exponential backoff retries.
  - **Dead Letter Queue (DLQ):** After exceeding maximum retries (e.g., 3), route the message to a DLQ topic (`dlq:<topic>`) and trigger a `CRITICAL` alert. Never discard unprocessable events.
- **Blueprint:** [event_driven_broker.py](file:///home/aditya/bin/templates/architecture/event_driven_broker.py)

### 4. Blue-Green Deployments
- **When to Use:** To achieve zero-downtime deployments and instant rollbacks.
- **Implementation Strategy:**
  - Standardize two independent environments: **Blue** (current production active) and **Green** (staging/new version).
  - Deploy and test the new release in the Green environment.
  - Use Nginx or a load balancer to atomic-swap traffic from Blue to Green.
  - Keep the Blue environment running for a cooling period (e.g., 1 hour) for instant fallback if anomalies occur.
- **Blueprint:** [blue_green_deploy.sh](file:///home/aditya/bin/templates/architecture/blue_green_deploy.sh)

### 5. Backend Scaling & Performance Engineering
- **Telemetry & Metrics:** Expose an HTTP `/metrics` endpoint scraping CPU/memory metrics and request latencies using Prometheus client.
- **Production Redis Token Bucket Rate Limiting:** Junior developers block traffic; senior backend engineers regulate flow mathematically. Always implement token bucket or sliding-window rate-limiting middleware globally to protect system capacity before business logic, databases, or CPUs overload:
  - **Bucket Parameters:** Define a maximum **Capacity** (governs allowable burst spikes) and **Refill Rate** (governs sustained traffic throughput).
  - **Identity Extraction:** Extract identity using `userId` (for authenticated routes) instead of `IP` to prevent NAT-user collateral blocks, falling back to `IP` / `API key` for anonymous traffic.
  - **Atomic Shared State:** Store bucket states in Redis using atomic operations (Counters, TTLs, or Lua scripts) to prevent race conditions across horizontally-scaled microservice nodes or Kubernetes clusters.
  - **Rejection Protocol:** If token capacity is exhausted, immediately reject with HTTP 429 and include `Retry-After` headers.
  - **Algorithm Suitability Matrix:**
    | Algorithm | Best For | Weakness |
    | :--- | :--- | :--- |
    | **Token Bucket** | Burst + steady traffic regulation | Requires shared state (Redis) |
    | **Leaky Bucket** | Smoothing traffic outputs | Poor handling of legitimate burst needs |
    | **Fixed Window** | Basic usage quotas | Boundary spikes (2x traffic at resets) |
    | **Sliding Window** | Precise, rolling-window fairness | Higher database/memory complexity |
  - **Sample Node.js + Redis Middleware Blueprint:**
    ```javascript
    const rateLimiter = new RateLimiterRedis({
      storeClient: redisClient,
      keyPrefix: 'rate_limit',
      points: 10, // Capacity
      duration: 1, // Refill window (seconds)
    });
    rateLimiter.consume(req.userId || req.ip, 1)
      .then(() => next())
      .catch(() => res.status(429).send({ error: 'Too Many Requests', retryAfter: 1 }));
    ```
- **Resource Pooling:** Always reuse database connections using connection poolers (e.g., PgBouncer, SQLAlchemy connection pool, or custom poolers). Limit max pool sizes.
- **Caching Protocols:** Always inject client/CDN cache-control headers (`Cache-Control: public, max-age=...`) and run local or distributed memory caches (Redis/Memcached) for high-frequency static reads.
- **Blueprint:** [backend_scaling_fastapi.py](file:///home/aditya/bin/templates/architecture/backend_scaling_fastapi.py)

---

## 📄 Latex Resume & ATS Optimization Protocols

When tasked with generating, modifying, or auditing resumes (especially in LaTeX format), the agent must act as an expert ATS engineer and copywriter by applying these 5 key optimization vectors:

### 1. Skills Gap Analysis
- **Action:** Analyze target Job Descriptions (JD) side-by-side with the current resume.
- **Optimization:** Identify the top 5 key skills/responsibilities missing or weakly represented in the current resume. Match each missing skill to 1–2 quantifiable achievements from the user's past experiences, framing them with strong action verbs.

### 2. Tailored Bullet Points
- **Action:** Rewrite the experience section to align precisely with the target JD.
- **Optimization:** Limit descriptions to 4–6 high-impact bullet points per role. Every bullet point must:
  - Start with a strong, active verb (e.g., *Architected*, *Spearheaded*, *Optimized*).
  - Incorporate target keywords naturally in context.
  - Quantify accomplishments wherever possible (e.g., "reduced latency by 35%", "scaled throughput by 4x").
  - Be written in professional, concise, first-person implied voice.

### 3. Readability & ATS Compatibility
- **Action:** Optimize document structure for machine parsers and human recruiters.
- **Optimization:** Use standard section headings (e.g., *Experience*, *Skills*, *Education*). Avoid tables, columns, text boxes, and charts within LaTeX/PDF that break ATS text flow. Ensure standard, high-readability fonts (e.g., Latin Modern, Computer Modern, Arial, Helvetica). Address employment gaps subtly (e.g., highlighting continuous learning, consulting, or project-based work).

### 4. Relevant Professional Summary
- **Action:** Formulate an engaging, hook-like summary (4-5 sentences).
- **Optimization:** Highlight unique value propositions, naturally weave in 3-4 keywords from the job description, and end with a forward-looking commitment showing value-adds to the prospective company.

### 5. ATS Keyword Integration & Ranking Optimization
- **Action:** Analyze JD keyword density and naturally integrate target terminology.
- **Optimization:** Avoid keyword stuffing. Place key terms naturally within Summary, Experience, and Skills sections. Suggest missing sections, certifications, or specialized industry terminology commonly used in top-tier candidate resumes for the target role.

---

## 🎯 AI Job Hunting System — 5-Step Framework (AI Action Letter)

> Source: *AI Action Letter* by Abhijay Arora Vuyyuru (PM @ YouTube/Google, Harvard MBA)
> Newsletter: [AI Action Letter on Substack](https://substack.com/@abhijayaroravuyyuru)

This is a complete AI-powered job hunting system. When the user asks for help with job applications, interviews, or career strategy, apply these protocols.

---

### 🔑 Core Insight
> Mass applying with a generic resume = 0 interviews. Strategy + AI targeting = results.
> 75% of resumes are rejected by ATS before a human ever sees them.

---

### Step 1: ATS-Proof Resume Rules

**Format (non-negotiable):**
- ✅ Single-column layout (multi-column breaks ATS parsing)
- ✅ No icons, tables, images, or graphics
- ✅ Standard section headers EXACTLY: `Education`, `Experience`, `Skills`, `Projects`
- ✅ Reverse chronological order (most recent first)
- ✅ Export as PDF (always)
- ✅ One page (unless 10+ years of experience)

**Bullet Formula:**
```
[Action Verb] + [What You Did] + [Quantified Result]
```

| ❌ Weak | ✅ Strong |
|---------|---------|
| "Responsible for managing social media accounts" | "Grew Instagram following from 2K to 50K in 6 months by implementing a data-driven content strategy, increasing engagement rate by 340%" |

**Rule:** At least **70% of bullets must include a metric.**

**Strong Action Verbs:** Architected, Spearheaded, Optimized, Automated, Delivered, Scaled, Reduced, Increased, Launched, Mentored, Audited, Integrated

---

### Step 2: LinkedIn Optimization — AI Prompt

Copy this prompt into Claude or ChatGPT with the user's LinkedIn content:

```
Here is the scraped content of a LinkedIn profile:
<profile>
{{PASTE LINKEDIN PROFILE CONTENT HERE}}
</profile>

The user's goal is: {{GOAL}}
(e.g., "attract PM roles at FAANG", "get recruited for senior engineering roles",
"build thought leadership in AI")

Please analyze the profile across these dimensions and give specific
rewrites, not just suggestions:

1. Headline — Is it keyword-rich, role-specific, and value-forward? Rewrite it.
2. About/Summary — Does it tell a compelling story with a clear hook in line 1? Rewrite it.
3. Experience bullets — Are they outcome-driven with numbers? Flag weak ones and rewrite 2–3 examples.
4. Featured section — What should be pinned here given their goal?
5. Skills & Keywords — What's missing for SEO and recruiter/algorithm discoverability?
6. Creator/Posting signals — Any gaps in how they present their content or niche authority?
7. CTA — Does the profile have a clear next step for visitors?

Format output as:
[Section] → [Issue] → [Rewrite or Recommendation]
```

---

### Step 3: Automate Job Discovery

**Problem:** By the time you see a job posting on LinkedIn/Indeed, hundreds have applied. Early applicants get interviews.

**Solution — n8n + Apify pipeline (~$7/month):**
- Scrapes LinkedIn for jobs posted in the **last 24 hours**
- Filters by role, location, industry
- Returns top 5 most recent listings per search
- Delivers results daily — no manual searching

**Hiring Manager Search Patterns (LinkedIn):**

| Pattern | Search String |
|---------|--------------|
| Direct Intent | `"I'm hiring"` OR `"looking for a"` OR `"open role on my team"` |
| Call to Action | `"DM me"` OR `"send me your resume"` OR `"drop your portfolio"` |
| Team Growth | `"growing the team"` OR `"excited to announce"` OR `"just opened a req"` |

> A **direct LinkedIn DM to a hiring manager** is 10x more effective than Easy Apply.

**Reference guides:**
- [AI Agent That Job Hunts While You Sleep](https://substack.com/@abhijayaroravuyyuru) — n8n + Apify setup
- [Use LLMs in Your Job Search](https://substack.com/@abhijayaroravuyyuru) — LinkedIn search patterns

---

### Step 4: Auto-Tailor Resume Per Job (One-Click Workflow)

**Why:** ATS doesn't know "project management" = "program management". Mirror JD language exactly.

**n8n Automation Stack:**
| Tool | Cost | Role |
|------|------|------|
| n8n | ~$7/mo | Workflow orchestration |
| Apify | Free tier | LinkedIn job scraping |
| Google Gemini API | Free tier | Resume rewriting |
| Google Docs | Free | Tailored resume output |
| Gmail | Free | Daily summary emails |

**Workflow:**
1. Job descriptions fetched from Step 3 pipeline
2. AI extracts keywords — skills, tools, qualifications, action verbs
3. Base resume rewritten to match JD language (never invents experience)
4. New Google Doc created per tailored resume
5. Summary email sent with links to all tailored resumes + job postings

> You wake up to an email with tailored resumes ready to submit.

---

### Step 5: LinkedIn Content Strategy

**Why post during job search:**
- Signals to recruiters you're active in your field
- Creates inbound opportunities (hiring managers find you)
- Builds professional brand — when Googled, you have substance

**Cadence:** 3x per week

**Post Formula:**
- Bold/punchy first line (hook)
- Short paragraphs (1-2 sentences max)
- End with a question or CTA

**90 Post Ideas — Organized by Category:**

#### 🔄 Reintroduction (1-10)
1. "I've been lurking on LinkedIn for 3 years. Here's what I've learned just by reading."
2. "I've never posted here before. So let me finally introduce myself properly."
3. "I've consumed content on LinkedIn for years. Time to contribute something."
4. "I kept drafting posts and deleting them. This one's staying up."
5. "I used to think posting on LinkedIn was for people with big titles. I was wrong."
6. "I told myself I'd post 'when the time was right.' Turns out there's no perfect moment."
7. "Most of my career wins happened while I was silent on here. Here's a quick recap."
8. "I'm not a natural poster. But I have things worth saying. Starting today."
9. "If you've wondered who the quiet person in your network is — that's been me. Until now."
10. "I've been at [company] for X years. Here's what I wish I'd shared sooner."

#### 💡 Lessons Learned (11-20)
11. "The one career lesson I had to learn the hard way."
12. "3 things I know now that I wish someone told me on day one of my career."
13. "The best piece of advice I ever got — and why I ignored it for years."
14. "What I learned in my first 90 days at my current job."
15. "A mistake I made early in my career that actually shaped everything."
16. "The thing nobody tells you about [your industry]."
17. "I spent 5 years trying to be the smartest person in the room. Here's what changed."
18. "What I learned from a boss I absolutely hated."
19. "The meeting that changed how I think about my career."
20. "One habit that made me significantly better at my job."

#### 🎯 Hot Takes & Contrarian Views (21-30)
21. "Unpopular opinion: hustle culture is making us worse at our jobs."
22. "Cold emails work better than job boards. Change my mind."
23. "The 'follow your passion' advice is incomplete. Here's the missing part."
24. "Networking events are mostly a waste of time. Here's what isn't."
25. "The soft skills that companies say they want vs. the ones they actually reward."
26. "Being likable at work matters more than being competent. (Let's talk about it.)"
27. "Your resume is not your story. Here's what I think is."
28. "Work-life balance is the wrong framing. Here's a better one."
29. "We over-celebrate busyness. Here's what I think actually matters."
30. "I don't think the 10,000-hour rule applies the way we think it does."

#### 📖 Personal Story Arc (31-40)
31. "I almost quit my career in [field] 3 years ago. Here's what stopped me."
32. "My career didn't go according to plan. Here's the version that actually happened."
33. "I got laid off. Here's what that week looked like — and what came next."
34. "I changed industries at [age]. Everyone thought I was crazy. Here's how it went."
35. "The promotion I didn't get — and why I'm grateful for it now."
36. "From [starting point] to [current role] — the version nobody puts on their resume."
37. "I said yes to something terrifying at work. Here's what happened."
38. "The conversation that completely changed my career trajectory."
39. "How a random connection on LinkedIn led to [a major opportunity]."
40. "I relocated for a job. It didn't work out. Here's what I learned."

#### 📊 Industry Insight & Trends (41-50)
41. "Something I'm seeing shift in [your industry] that nobody's talking about enough."
42. "3 skills that will matter most in [your field] over the next 5 years."
43. "Why [a common industry practice] is overrated."
44. "The part of the AI conversation that I think is missing from most discussions."
45. "What companies in [industry] keep getting wrong about [topic]."
46. "The role that didn't exist 5 years ago that every company now needs."
47. "An outdated belief in [your industry] that's still being taught like it's gospel."
48. "Why I think [emerging trend] is more important than most people realize."
49. "The thing that separates good companies from great ones in [your industry]."
50. "Here's how [your field] has changed in the last 3 years — and what that means."

#### 🤝 People & Management (51-60)
51. "The best manager I ever had did one thing differently."
52. "What I look for when I'm hiring — and it's probably not what you'd expect."
53. "I've interviewed hundreds of people. The candidates who stand out all do this."
54. "The type of teammate that makes every project better."
55. "Something I noticed great leaders do that average leaders don't."
56. "Why I started asking 'what do you need from me?' more than 'how's it going?'"
57. "The feedback conversation that was hard to give — and why I'm glad I did."
58. "How I think about building trust with a new team quickly."
59. "The most underrated quality in a professional: [your answer]."
60. "What managing people taught me about myself."

#### 🛠️ Tools, Systems & Productivity (61-70)
61. "The one tool that made my work dramatically more efficient this year."
62. "How I structure my week to protect time for deep work."
63. "My personal framework for making decisions at work."
64. "I started doing [small habit] 6 months ago. Here's what changed."
65. "The way I take notes has completely changed how I retain information."
66. "How I use AI in my actual workflow — not the hype version, the real one."
67. "The system I use to track my wins throughout the year (for performance reviews)."
68. "What I do in the first 30 minutes of every workday."
69. "The question I ask at the end of every project to get better over time."
70. "Why I started writing a 'failure log' — and what it's taught me."

#### 🌍 Values, Purpose & Identity (71-80)
71. "The moment I realized my job title isn't my identity."
72. "What I believe about work that I think most companies get wrong."
73. "Why I turned down a higher-paying job — and what that decision taught me."
74. "Something I protect no matter how busy work gets."
75. "What 'meaningful work' actually means to me."
76. "Why I stopped optimizing for status and started optimizing for [something else]."
77. "The values I want to still have in 20 years — and how I try to practice them now."
78. "A thing I'm genuinely proud of at work that wasn't a promotion or raise."
79. "The part of your career that has nothing to do with your resume."
80. "What I think about when I'm deciding whether an opportunity is right for me."

#### 🎓 Learning & Growth (81-90)
81. "The book that most changed how I think about work. (And the idea that stuck.)"
82. "What I learned from 30 days of [challenge or experiment]."
83. "I took a course on [topic] expecting one thing and got something completely different."
84. "The mentor who shaped my career — and the one piece of advice they kept repeating."
85. "What I'm actively trying to get better at this year."
86. "The question I asked that unlocked a completely new way of thinking for me."
87. "Something I believed at 22 about work that I've completely unlearned."
88. "The podcast/newsletter/resource that I'd recommend to everyone in [field]."
89. "What I'm learning right now — and why it feels uncomfortable."
90. "The thing I realized I was bad at — and what I did about it."

---

### Quick-Start Checklist (When User Asks for Job Hunt Help)
- [ ] Step 1: Create ATS-friendly resume (single column, PDF, 70%+ quantified bullets)
- [ ] Step 2: Run LinkedIn profile through AI optimization prompt above
- [ ] Step 3: Set up Apify + n8n for daily job scraping (24h postings)
- [ ] Step 4: Configure auto-tailoring workflow (Gemini API + Google Docs)
- [ ] Step 5: Pick 3 post ideas and publish first LinkedIn post this week

### Visa Note for International Candidates
For H-1B alternatives: **EB-1A** and **O-1 visas** are viable paths for STEM candidates. Free 15-min consultation available via Manifest Law.

---

## 🎨 Claude UI Design Skills Playbook & Workflow

When designing premium SaaS interfaces, landing pages, mobile apps, or performing audits, the agent MUST leverage these 9 key design commands/skills and follow the structured workflow to output startup-level, Stripe-quality, and Vercel-style UIs.

### 1. Key Design Commands & Skills

| Command / Prompt | Core Action | Typical Target Prompt Example |
|------------------|-------------|-------------------------------|
| `/awesome-design-md` | **Premium SaaS UI Components** | "Design a premium SaaS dashboard for an AI startup with modern spacing, clean hierarchy, Stripe-level UI, and startup-quality components." |
| `/design-mastery` | **Better UX & Onboarding Audits** | "Audit my SaaS onboarding flow and redesign it for better conversion, accessibility, and user experience." |
| `/mobile-app-ui-design` | **Premium Mobile App UI** | "Design a modern AI productivity app inspired by Airbnb and Spotify with premium onboarding and smooth mobile UX." |
| `/ux-ui-mastery` | **UX Psychology & Conversions** | "Redesign my SaaS checkout flow to improve conversion, trust, and reduce drop-off using cognitive psychology." |
| `/design-system-extractor` | **Extract Tokens from Image/UI** | "Extract the exact design system from this Stripe screenshot and recreate the spacing, typography, and color system." |
| `/UI/UX Pro Max` | **Interactive App UX Audits** | "Audit this SaaS dashboard and show me the top UX mistakes hurting conversions with actionable fixes." |
| `/Vercel Web Design Guidelines` | **High-Converting Landing Pages** | "Create a premium landing page for my AI SaaS with modern Vercel-style UI and high-converting copy." |
| `/Vercel React Best Practices` | **Clean React + Tailwind Code** | "Convert this Figma UI into reusable React + Tailwind components using production-grade code structure." |

### 2. Winning Claude UI Design Workflow

The agent MUST follow this exact sequence to ensure professional, pixel-perfect results on every web/mobile project:

1. **Base UI (`/awesome-design-md`):** Build the foundation and primary pages using premium design tokens and Stripe-level components.
2. **Onboarding & UX (`/design-mastery`):** Audit the onboarding flow, fix accessibility, and clean up layouts.
3. **Design Tokens (`/design-system-extractor`):** Extract and lock down key design elements (color palette, spacing grid, type scale) from reference screenshots.
4. **Mobile Adaptations (`/mobile-app-ui-design`):** Adapt layouts using Airbnb/Spotify-style mobile paradigms where necessary.
5. **Checkout & Conversion (`/ux-ui-mastery`):** Optimize call-to-actions, pricing tables, and checkout screens using cognitive psychology principles.
6. **Final Audit (`/UI/UX Pro Max`):** Scan the UI to catch the top 5 common UX/visual hierarchy mistakes before staging.
7. **Landing Page Copy (`/Vercel Web Design Guidelines`):** Structure high-converting sections, headlines, and sub-copy in a minimal Vercel-style layout.
8. **Code Generation (`/Vercel React Best Practices`):** Convert the polished layouts into clean, modular, production-grade React + Tailwind code.
9. **Ship!**

### 3. Mistakes to Avoid
- 🚫 Going straight to writing code without establishing spacing systems or color tokens first.
- 🚫 Using random, generic colors without a cohesive color system/palette.
- 🚫 Ignoring mobile-first viewports and native gesture/spacing grids.
- 🚫 Allowing inconsistent vertical and horizontal grid spacing across container boundaries.
- 🚫 Skipping accessibility audits (like tap targets, text contrast ratios) before deployment.
- 🚫 Building landing pages without high-converting UX copy.

---

## 🎬 TEXTURA / Claude Code Website Pipeline (Premium Animated Websites)

When tasked with designing and implementing high-converting landing pages or animated websites, the agent must leverage the **TEXTURA / Claude Code Website Pipeline** to build premium animated websites with AI — from finding a design reference to deploying on a host.

### 1. Antigravity vs. Claude Code Layout Paradigm
* **Antigravity Browser Flow:** Takes a screenshot, generates UI components in the browser, allowing visual editing before code export. Avoids vendor lock-in.
* **Claude Code Command Flow:** Takes a screenshot, translates it into clean code, allowing conversational iterations directly in the codebase for Next.js/HTML, providing full control and ownership.

### 2. The 11-Step Step-by-Step Pipeline

#### Step 01: Brief & Copywriting (Phase 1 — Brief & Strategy)
Define the brand, audience, and tone of voice. Generate all page copy with AI (Perplexity or Claude.ai) *before* touching any code or design.
* **Copywriting Prompt:**
  ```
  "You are a senior copywriter. Write hero headline, subheadline, 3 feature descriptions, CTA and footer copy for [BRAND]. Tone: [cinematic / bold / minimal]. Output JSON."
  ```

#### Step 02: Find a Section Reference (Phase 2 — Reference Selection)
Browse Dribbble, Behance, or Awwwards for strong hero sections. Use search tags: `landing page`, `hero`, `product`, `dark UI`.

#### Step 03: Strip the Background — Clean UI Only (Phase 2 — Reference Cleaning)
Use GPT-4o or OpenArt to strip all background graphics, keeping only typography, buttons, and navigation on a solid black background. This serves as a precise layout reference for Claude Code without background noise.
* **Background Stripping Prompt:**
  ```
  "A high-fidelity mockup based on [screenshot]. Only UI elements on solid black background. All background imagery removed. Text and buttons in strict black and white. Stark, minimal, high-contrast monochrome."
  ```

#### Step 04: Recreate the Layout from Screenshot (Phase 3 — Build in Claude Code)
Attach the stripped monochrome screenshot and describe the task to recreate the layout.
* **Layout Recreation Prompt:**
  ```
  "You are a senior web designer and developer. Recreate the referenced layout one-to-one using Next.js 16. Match fonts (use similar creative typefaces), spacing, proportions and element positioning. Use React Spring to animate elements sequentially on load."
  ```
* **Pro Tip:** Attach the cleaned B&W reference and the original screenshot together. Command Claude Code to use the clean version for layout/positioning, and the original version for colors, mood, visual texture, and typographic intent.

#### Step 05: Typography (Phase 4 — Fonts & Color)
Pick trending display fonts on Google Fonts and the Awwwards Free Fonts collection (e.g., Condensed, Black, Extended).

#### Step 06: Color Palettes (Phase 4 — Fonts & Color)
Find trending color combinations on Coolors (Trending Palettes), export as CSS variables, and apply them.
* **Color Prompt:**
  ```
  "Take this palette [HEX list] and apply it to the project. Update all CSS custom properties. Primary CTA button — [COLOR]."
  ```

#### Step 07: 3D Models (Phase 4 — 3D Models)
Search for free 3D models on Sketchfab. Download GLB / GLTF and embed them via Three.js, React Three Fiber, or Spline.

#### Step 08: Image & Video Generation (Phase 5 — Visual Assets)
Generate hero illustrations, 3D characters, or looping background assets. Use OpenArt or Kling 3.0 to produce seamless looping background videos.
* **Asset Prompt:**
  ```
  "3D render, [description], dark cinematic background, soft rim lighting, 4K, transparent bg. Style: Clay / Glossy / Neon."
  ```

#### Step 09: Animations Referenced from Pinterest (Phase 6 — Animations)
Collect reference clips of transitions, hover states, scroll reveals, marquees, or sticky sections on Pinterest. Feed them to Claude Code to implement with GSAP or Framer Motion.
* **Animation Prompt:**
  ```
  "Implement these animation references with GSAP ScrollTrigger. Hero text: staggered reveal on load. Cards: fade + lift on scroll into view. Marquee: infinite horizontal loop, pause on hover. Respect prefers-reduced-motion."
  ```

#### Step 10: Asset Compression & Optimization (Phase 7 — Optimization)
Compress all assets with Squoosh and optimize resources:
* **Optimization Prompt:**
  ```
  "Audit /public: convert all images to WebP, add lazy loading. Video: MP4+WebM under 2MB. Preload hero font. Reserve space for hero image to prevent layout shift (CLS)."
  ```
* **Optimization Rules:**
  - PNG/JPG to WebP (Squoosh at quality 80%)
  - Video loops: MP4 + WebM formats, max 2MB total size
  - Fonts: preload in `<head>`
  - Images: lazy loading + explicit width/height attributes (prevent CLS)
  - Accessibility: add `@media (prefers-reduced-motion)` and maintain minimum AA (4.5:1) text contrast.

#### Step 11: Host & Deploy the Site (Phase 8 — Deploy)
* **Vercel Configuration Prompt:**
  ```
  "Generate vercel.json: cache /public/* immutable 1 year, redirect www → apex domain, 404 → index.html for SPA routing."
  ```
* **Deployment Workflow:**
  1. Next.js: `npm run build` ➔ `vercel deploy` or Vercel Git integration.
  2. Custom Domain: Configure A-record or CNAME in DNS settings (e.g. Hostinger).
  3. HTTPS: Automatically provisioned by host.
  4. Validation: Run Lighthouse and ensure a 90+ Performance score.

---

## 🛡️ Repository Hygiene & Security Guardrails (Zero-Vulnerability Codebase)

The agent MUST enforce strict repository hygiene and security guardrails to ensure no secrets, internal assets, or architectural flaws are exposed. Every code write and commit must be audited against this checklist:

### 1. Repository Hygiene & Git Cleanliness
- **Zero Secrets committed:** NEVER commit `.env`, `.env.local`, or any credentials/keys. Use `.env.example` as a template.
- **Strict `.gitignore` enforcement:** Ensure `node_modules/`, build output (`dist/`, `build/`, `.next/`, `out/`), and system files (`.DS_Store`, Thumbs.db) are ignored.
- **No raw design assets:** Keep Photoshop (`.psd`), Sketch, or Illustrator raw files out of the repository. Store them in cloud storage or `docs/images/` only if flattened (PNG/WebP).
- **No operational leaks:** Keep production deployment files separated from source directories.
- **Pre-flight Commit check:** Always run `git status` or audit staged files using linters to verify that no build artifacts, lockfiles, or config overrides are accidentally staged.

### 2. Authentication & Authorization Security
- **Secure Cookie Configuration:** When setting session cookies/JWT tokens, they MUST carry the following flags:
  - `HttpOnly` (prevents XSS access to tokens).
  - `Secure` (ensures cookies are only sent over HTTPS).
  - `SameSite=Lax` or `SameSite=Strict` (prevents CSRF attacks).
- **Secure Auth Responses:** NEVER return the full user object or fields containing password hashes, internal roles, salt, or database metadata. Explicitly project/serialize safe fields (e.g., username, public ID).
- **Safe Error Handling:** Catch all database and authentication exceptions. Never return raw stack traces, database query logs, or server internal details in error responses. Use clean, user-friendly messages while logging the raw stack trace securely to stdout/files.

### 3. API Security & Infrastructure Protection
- **Input Validation & Rate Limiting:** All endpoints (especially `/login`, `/register`, and transaction endpoints) must enforce input validation (e.g., using Pydantic, Zod, or Joi) and rate limiting (e.g., token bucket pattern) to block automated brute-force attacks and DDoS.
- **Zero Default Credentials:** Never document default admin credentials in README files or scripts. Use dynamic initialization scripts or secure configuration variables.
- **Conceal Architecture details:** Avoid exposing detailed infrastructure files (`nginx.conf`, custom `docker-compose.yml` exposing default ports) publicly. Ensure production setups run in separate private deployment pipelines or carry obfuscated, variable-driven parameters.
- **Automated Scanning Guardrails:** Run static analysis checks (`semgrep`), secret checks (`gitleaks`), and vulnerability scanning (`trivy`) in local Git hooks (`pre-commit`) and cloud CI to enforce early-exit failure on violations.
- **"Clean Commit" Workflow:** Perform a local code review (`git diff | delta`) before pushing. Reject the "Push First, Fix Later" pattern.

---

## 🧠 Long-Term Project Context & Code Maintenance (AI Maintainability Protocol)

To prevent codebases from becoming unmaintainable due to context drift, duplicate logic, and messy state management, the agent MUST strictly enforce long-term memory structures and modular feature development.

### 1. Mandatory Context & Memory Files
Before generating code for any feature, verify or initialize these active memory files in the project root (or inside the `memory-bank/` directory):
* **`PROJECT_CONTEXT.md` / `progress.md`:** Tracks the used tech stack, app flow, API/route registry, auth flow, schema, dependencies, completed features, and active task lists.
* **`ARCHITECTURE.md`:** Maps the layers (frontend, backend, database relationships), reusable services, state management, and AI abstractions to keep files modular and replaceable.
* **`CODING_RULES.md` / `.cursorrules` / `GEMINI.md`:** Declares naming conventions, folder structure, import rules, component patterns, API response formats, TypeScript rules, and styling system parameters.
* **`FEATURE_LOG.md` / `walkthrough.md`:** Logs all added features, removed subsystems, major refactors, dependency updates, and architectural changes.

### 2. Code Generation Directive (Pre-Flight System Prompt)
Before writing or modifying any production code, the agent MUST act in accordance with this strict system directive:
> *"You are a senior software architect working on an existing production-grade project. Follow the current architecture strictly. Maintain modular layered architecture. Keep frontend, backend, APIs, auth, database logic, and AI services separated. Reuse existing components and utilities whenever possible. Avoid duplicate logic. Follow existing naming conventions and coding patterns. Generate scalable, maintainable, production-ready code only. Update PROJECT_CONTEXT.md and ARCHITECTURE.md after major changes."*

### 3. Modular Development & Micro-Commits
- **Break Down Monoliths:** Never implement massive systems in a single run (e.g., *"build full SaaS app with payment, auth, and dashboard"* is strictly forbidden). Instead, build in atomic, isolated layers:
  1. Auth Module
  2. Database Schema & API Layer
  3. UI Layout & Dashboard System
  4. Payment Integration
  5. AI Service Abstraction
  6. Telemetry & Analytics
- **Incremental Commits:** Commit and verify each stable feature layer before moving to the next. This prevents complex, destructive AI refactors from breaking unrelated subsystems.

---

## 🎭 Playwright Autonomous QA & Self-Healing Loop

When tasked with QA, end-to-end testing, or preparing a repository for production deployment, the agent MUST act as an autonomous QA + Fix Engineer and execute the following 6-phase Playwright testing and code-healing loop.

### Phase 0 — Environment & Project Discovery
1. **Detect Stack:** Inspect `package.json` / `pyproject.toml` / `go.mod` to identify framework, package manager (npm/bun/pnpm/yarn), test runners, dev server commands, and default port.
2. **Project Report:** Log a brief stack overview, routes, entry points, and existing tests in `AGENT_NOTES.md`.
3. **Docs Check:** Read README, CONTRIBUTING, and DEV docs before making code changes.

### Phase 1 — Playwright Installation & Configuration
1. **Install Playwright:** Run appropriate package commands to add `@playwright/test` and download browser binaries with dependencies (`playwright install --with-deps`).
2. **Setup Config:** Create `playwright.config.ts` configured for:
   - Chromium, WebKit, and Firefox.
   - `baseURL` pointing to the local dev server.
   - Trace on first retry, screenshots only on failure, video retained on failure.
   - `webServer` block that automatically starts the dev server.
3. **Folders:** Create `tests/e2e`, `tests/visual`, `tests/a11y`, and `test-results/screenshots/`.

### Phase 2 — Static Analysis
- Run the linter and type-checker (`eslint`, `tsc --noEmit`, `ruff`, etc.).
- Build the project (`npm run build` or equivalent) and capture compilation errors.
- Document suspicious files, TODOs, missing env parameters, or structural flaws in `AGENT_NOTES.md`.

### Phase 3 — Generate Test Suite
Generate Playwright tests that cover:
1. **Smoke Tests:** Every public route loads with HTTP 200 and zero console errors.
2. **User Journeys:** Auth flows, CRUD pages, forms, navigation, and payment/checkouts.
3. **Responsive Testing:** Verify viewports: Mobile (375x667), Tablet (768x1024), and Desktop (1440x900).
4. **Visual Regression:** Save full-page screenshots to `test-results/screenshots/<route>__<viewport>.png`.
5. **Accessibility (a11y):** Integrate `@axe-core/playwright` and fail on serious/critical violations.
6. **Network Check:** Assert no 4xx/5xx responses in the network log for happy paths.

### Phase 4 — The Agentic Testing & Fixing Loop
Repeat this loop for up to 8 iterations until exit criteria are met:
- **Run:** Execute `npx playwright test --reporter=list,html`.
- **Collect:** Parse all failures, console logs, a11y violations, and screenshots.
- **Diagnose:** For each failure, open relevant code files, form a hypothesis, and log it in `AGENT_NOTES.md` under *"Iteration N — Findings"*.
- **Fix:** Apply minimal, surgical code fixes to resolve root causes. Never change tests to pass unless the test itself was incorrect.
- **Verify:** Re-run failed tests, followed by the entire suite to verify fixes.
- **Visual Diff:** Compare new screenshots to previous iterations and note regressions.
- **Commit:** Commit fixed code per iteration with convention: `fix(iter-N): <summary>`.

*Exit Criteria (All must hold):*
- `npm run build` succeeds with zero errors/new warnings.
- Linter and type-checker pass clean.
- 100% of Playwright tests pass on chromium, webkit, and firefox.
- Zero console errors on any tested route.
- Zero serious/critical axe violations.

If convergence fails after 8 iterations, stop and produce a remediation report listing remaining failures and recommendations.

### Phase 5 — Production Verification & Report
1. **Production Build:** Run `npm run build` and launch the production server.
2. **Parity Check:** Re-run smoke and critical-journey tests against the production bundle to ensure parity with the dev server.
3. **Final Report:** Generate `AGENT_REPORT.md` including:
   - Initial state summary.
   - Bugs found (grouped by severity) and the fixing commit hashes.
   - Pass counts and test durations.
   - Links to screenshots.
   - Remaining known issues or recommendations.
   - Confirmation that the build is production-ready.

---

## 🔄 Multi-Provider LLM Proxy & Router Patterns (FreeLLMAPI Blueprints)

When building systems that aggregate, load-balance, or failover across multiple LLM API providers (e.g. OpenAI, Anthropic, Gemini, Groq, Cerebras), the agent MUST implement these production-grade resilient proxy patterns.

### 1. Dynamic Priority Routing with Penalty Decay
To handle upstream provider outages or rate-limit hits (HTTP 429/5xx) gracefully, do not hardcode static routing chains. Instead, sort candidate providers dynamically using a base priority combined with a decaying penalty score.

* **Formula:** `effective_priority = base_priority + rate_limit_penalty`
* **On Failure (429/5xx):** Increment the model's penalty: `penalty = Math.min(penalty + PENALTY_AMOUNT, MAX_PENALTY)` (e.g., `+3` per hit, capped at `10`).
* **Time-Based Decay:** Decay the penalty gradually so working providers can recover their original priority ranking over time:
  ```typescript
  const DECAY_INTERVAL_MS = 2 * 60 * 1000; // 2 minutes
  const DECAY_AMOUNT = 1;

  function getDecayedPenalty(modelId: number, lastHitMs: number, currentPenalty: number): number {
    const elapsed = Date.now() - lastHitMs;
    const decaySteps = Math.floor(elapsed / DECAY_INTERVAL_MS);
    if (decaySteps > 0) {
      return Math.max(0, currentPenalty - (decaySteps * DECAY_AMOUNT));
    }
    return currentPenalty;
  }
  ```

### 2. Escalating Cooldown Quarantining
Prevent infinite retry loops that consume all fallback capacity when a key/account has fully exhausted its quota. Implement an escalating cooldown array based on failures within a rolling 24-hour window.

* **Cooldown Progression:** `[2 min, 10 min, 1 hour, 24 hours]`
* **Key-Level Tracking:** Track recent rate-limit timestamps per key:
  ```typescript
  const COOLDOWN_DURATIONS = [
    2 * 60 * 1000,       // 2 minutes
    10 * 60 * 1000,      // 10 minutes
    60 * 60 * 1000,      // 1 hour
    24 * 60 * 60 * 1000, // 24 hours
  ];

  export function getNextCooldownDuration(keyHits: number[]): number {
    const now = Date.now();
    const hitsInLast24h = keyHits.filter(t => t > now - 24 * 60 * 60 * 1000);
    const index = Math.min(hitsInLast24h.length, COOLDOWN_DURATIONS.length - 1);
    return COOLDOWN_DURATIONS[index];
  }
  ```

### 3. Conversation Sticky Sessions
Multi-turn conversations suffer high hallucination rates and prompt formatting errors if routed to different models mid-dialogue. Pin multi-turn requests to the same model for the duration of the conversation.

* **Session Identifier:** Derive the session key from a SHA1 hash of the first user message. Since client applications re-send the full history each turn, the first user message remains stable.
  ```typescript
  import crypto from 'crypto';

  function getSessionKey(messages: ChatMessage[]): string {
    const firstUserMsg = messages.find(m => m.role === 'user');
    if (!firstUserMsg || typeof firstUserMsg.content !== 'string') return '';
    return crypto.createHash('sha1').update(firstUserMsg.content).digest('hex');
  }
  ```
* **Session TTL:** Store the model ID mapped to the session key in-memory with a 30-minute TTL. Auto-route is bypassed in favor of the pinned model for any subsequent messages matching that session hash.

### 4. Resilient Streaming and SSE Error Handling
When proxying Server-Sent Events (SSE), standard HTTP errors cannot be returned if the stream has already started.
* **Pre-stream Errors:** Catch provider startup errors before emitting the first chunk. This allows the proxy to fall back and try other providers/keys transparently before committing to headers.
* **Mid-stream Errors:** If a provider fails mid-response after headers are written, write a structured JSON error payload as an SSE chunk followed by `data: [DONE]\n\n` to prevent hanging sockets:
  ```typescript
  try {
    for await (const chunk of upstreamGenerator) {
      if (!headersSent) {
        res.setHeader('Content-Type', 'text/event-stream');
        res.setHeader('X-Routed-Via', `${platform}/${model}`);
        headersSent = true;
      }
      res.write(`data: ${JSON.stringify(chunk)}\n\n`);
    }
    res.write('data: [DONE]\n\n');
    res.end();
  } catch (err: any) {
    if (headersSent) {
      // Stream started: inject error event cleanly
      const payload = { error: { message: `Stream interrupted: ${err.message}`, type: 'stream_error' } };
      res.write(`data: ${JSON.stringify(payload)}\n\n`);
      res.write('data: [DONE]\n\n');
      res.end();
    } else {
      // Stream hasn't started: let the outer retry/fallback loop handle it
      throw err;
    }
  }
  ```

### 5. Timing-Safe Key Verification
Never use direct `===` operators to validate incoming authorization tokens. Plain comparisons exit early on mismatches, leaking timing data that a network attacker can exploit to reconstruct the API token.
* **Implementation:** Always use constant-time byte array comparisons:
  ```typescript
  import crypto from 'crypto';

  export function timingSafeStringEqual(provided: string, expected: string): boolean {
    const a = Buffer.from(provided);
    const b = Buffer.from(expected);
    const compareA = a.length === b.length ? a : Buffer.alloc(b.length);
    return crypto.timingSafeEqual(compareA, b) && a.length === b.length;
  }
  ```

### 6. AES-256-GCM Envelope Encryption for Stored API Keys
Never store third-party provider API keys in plaintext inside databases (SQLite/Postgres). Encrypt them at-rest using AES-256-GCM and store initialization vectors (IVs) and authentication tags alongside the ciphertexts.
* **Initialization:** Require a 64-character (32-byte) hex `ENCRYPTION_KEY` at startup. Validate length and character bounds immediately.
* **In-Memory Decryption:** Load encrypted keys into memory and decrypt them *only* at the moment of forwarding the request. Keep plaintexts out of databases.

---

## 🤖 Claude Code Engine & Plugin System (Official Extension Blueprints)

When extending or customizing agent behavior within the official **Claude Code** runtime or compatible CLI environments, the agent MUST leverage the following official plugin paradigms and extension patterns.

### 1. Plugin Directory Structure
Every Claude Code plugin must conform to this standard directory structure:
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata (JSON schema)
├── commands/                # Custom slash commands (Markdown syntax)
├── agents/                  # Specialized subagents (YAML/JSON configurations)
├── skills/                  # Core executable skills (Markdown/Markdown code)
├── hooks/                   # Lifecycle event hooks (Shell/Node scripts)
├── .mcp.json                # Custom MCP servers (local or remote)
└── README.md                # Plugin documentation
```

### 2. Custom Markdown Slash Commands
Define custom slash commands directly in Markdown files within `commands/` using YAML frontmatter metadata:
```markdown
---
description: "Start custom task run"
argument-hint: "PROMPT [--max-iterations N] [--completion-promise TEXT]"
allowed-tools: ["Bash(${CLAUDE_PLUGIN_ROOT}/scripts/setup-task.sh:*)"]
hide-from-slash-command-tool: "true"
---

# My Custom Command

Run the task setup script:
```!
"${CLAUDE_PLUGIN_ROOT}/scripts/setup-task.sh" $ARGUMENTS
```
```
* **Command Syntax:** The `description` and `argument-hint` are parsed by the CLI to provide tab-completion and help guides. The `allowed-tools` array limits tool execution permissions during command setup.

### 3. Session Exit Interception & Stop-Hook Blocking (The Ralph Wiggum Pattern)
To implement autonomous self-healing loops or force an agent to iterate repeatedly on a task until a specific condition or verification promise is satisfied, intercept session exits using a `Stop` hook.
* **State Verification:** Maintain a local state file (e.g. `.claude/loop-state.md`) containing the target prompt, iteration index, and a target `completion_promise`.
* **Exit Interception (`stop-hook.sh`):**
  1. The CLI calls the `Stop` hook when the agent attempts to exit the session.
  2. The script parses the session transcript (in JSONL format) and extracts the text of the last assistant message.
  3. If a completion promise is active, check if the assistant output contains a specific verification block (e.g. `<promise>PROMISE_TEXT</promise>`).
  4. If verified, delete the state file and exit `0` (allowing exit).
  5. If not verified, increment the iteration index in the state file and block exit by printing a structured JSON block to stdout:
     ```json
     {
       "decision": "block",
       "reason": "<original_prompt_text>",
       "systemMessage": "🔄 Loop Iteration N | Action: Continue working until condition is met."
     }
     ```
     This forces the runner to block the exit and automatically prompts the agent again with the original request, achieving autonomous iteration.

### 4. Security Guidance Hooks (`PreToolUse` Monitoring)
Implement real-time security warnings or pre-flight blockers using the `PreToolUse` hook.
* **Scan Modified Files:** Before any tool execution (such as editing or executing code), scan the modified code blocks against common security vulnerability patterns (e.g. command injection, XSS, `eval()`, dangerous innerHTML, raw pickle loading, or system execution calls).
* **Warn and Block:** Warn the agent or block execution if dangerous code elements are detected, forcing remediation before commit.

### 5. Bold Frontend Design Philosophy
Avoid generic "AI slop" aesthetics (such as default Inter typography, white backgrounds with generic purple gradients, or identical Bento grid layouts without character). Commit to a BOLD, intentional conceptual direction:
* **Typography:** Avoid overused system fonts (Arial, Inter, Space Grotesk). Pair a distinctive, characterful display font with a refined body font.
* **Layout:** Leverage spatial composition including asymmetry, grid-breaking elements, overlap, and diagonal flow.
* **Atmosphere:** Build depth using creative textures and overlays (gradient meshes, noise textures, layered transparencies, dramatic shadows, custom cursors, and grain overlays) rather than flat solid backgrounds.
* **Motion:** Focus on high-impact CSS-only entry transitions with staggered delays (`animation-delay`) and scroll-driven revelations rather than chaotic micro-interactions.

---

## 🎛️ Antigravity Awesome Skills Catalog & Installation Protocol

This protocol governs how the agent installs, activates, and leverages the curated library of 1,470+ installable agentic capabilities from the **Antigravity Awesome Skills** catalog.

### 1. Installation Targets and Flags
Install the repository dependencies or copy skills to specific AI client directories using `npx antigravity-awesome-skills`:
* **Claude Code:** `npx antigravity-awesome-skills --claude` (installs to `~/.claude/skills/`)
* **Gemini CLI:** `npx antigravity-awesome-skills --gemini` (installs to `~/.gemini/skills/`)
* **Cursor:** `npx antigravity-awesome-skills --cursor` (installs to `~/.cursor/skills/`)
* **Antigravity 2.0:** `npx antigravity-awesome-skills --antigravity` (installs to `~/.agents/skills/`)
* **Codex CLI:** `npx antigravity-awesome-skills --codex` (installs to `~/.codex/skills/`)
* **Kiro CLI:** `npx antigravity-awesome-skills --kiro` (installs to `~/.kiro/skills/`)
* **Custom Path:** `npx antigravity-awesome-skills --path <directory>`
* **Claude Code Plugin Installer:** `/plugin marketplace add sickn33/antigravity-awesome-skills` or `/plugin install antigravity-awesome-skills`

### 2. Context Optimization & Reduced Installs
To prevent agent performance degradation or memory overload due to too many active skills, apply category, tag, or risk filters during installation:
* **Category Filters:** `--category development,backend,security,ai-ml`
* **Risk Exclusions:** `--risk safe,none` (excludes critical, offensive, or unknown skills)
* **Tag Filters/Exclusions:** `--tags debugging,typescript-` (a trailing `-` excludes that tag)
* **Linux/macOS Activation Scripts:** In local cloned environments, run `./scripts/activate-skills.sh` to archive most skills and activate only specific bundles required by the active task.

### 3. Trust & Safety Classifications
Understand and respect the risk designations of installed skills:
* `none`: Pure text-based reasoning guidance with no system execution.
* `safe`: Read-only actions or low-risk operational queries.
* `critical`: State-changing or deployment-impacting actions (e.g. database updates, active builds).
* `offensive`: Authorized-use-only pentesting or red-team capabilities.
* `unknown`: Legacy/unclassified code waiting for audit validation.

### 4. Curated Role-Based Bundles
* **Web Wizard:** Radix UI design systems, Tailwind CSS patterns, minimalist UI layout components.
* **Hacker Pack:** OWASP security checks, threat modeling, pentest checklists.
* **Product Pack:** Feature planning, copywriting briefs, SEO content optimization, business strategy.
* **Essentials:** Clean code validation, systematic debugging, test-driven development (TDD) loops.

---

## 💰 Open-Source Monetization (OSM) Repository Index

When the user asks about "OSM" or "Open-Source Monetization", the agent must present the repository details in the following structured format. This indexes the active repositories set up for open-source bounty/mentorship work, mapping their tech stacks, payout structures, original URLs, and local user forks:

| Original Repository | Tech Stack | Payment Structure / Bounty Payout | User Fork Link (keyring-scoped) |
| :--- | :--- | :--- | :--- |
| [rudderlabs/rudder-server](https://github.com/rudderlabs/rudder-server) | Go, TypeScript | **$2,000 USD** per bounty | [adityashirsatrao007/OSM-rudder-server](https://github.com/adityashirsatrao007/OSM-rudder-server) |
| [Expensify/App](https://github.com/Expensify/App) | JavaScript, Android/iOS | **$250 - $500** per bounty | [adityashirsatrao007/OSM-App](https://github.com/adityashirsatrao007/OSM-App) |
| [AppFlowy-IO/AppFlowy](https://github.com/AppFlowy-IO/AppFlowy) | Flutter, Rust | **$500 / month** (Mentorship) | [adityashirsatrao007/OSM-AppFlowy](https://github.com/adityashirsatrao007/OSM-AppFlowy) |
| [triggerdotdev/trigger.dev](https://github.com/triggerdotdev/trigger.dev) | Next.js, TypeScript | **$50 - $200** per bounty | [adityashirsatrao007/OSM-trigger.dev](https://github.com/adityashirsatrao007/OSM-trigger.dev) |
| [ether/etherpad-lite](https://github.com/ether/etherpad-lite) | JavaScript | **~$80 USD** per bounty | [adityashirsatrao007/OSM-etherpad-lite](https://github.com/adityashirsatrao007/OSM-etherpad-lite) |
| [BusKill/buskill-app](https://github.com/BusKill/buskill-app) | Shell, Python | **~$2,340 USD** per bounty | [adityashirsatrao007/OSM-buskill-app](https://github.com/adityashirsatrao007/OSM-buskill-app) |
| [oliexdev/openScale](https://github.com/oliexdev/openScale) | Java, C++ | **~$30 USD** per bounty | [adityashirsatrao007/OSM-openScale](https://github.com/adityashirsatrao007/OSM-openScale) |
| [chozorho/conquest](https://gitlab.com/chozorho/conquest) | C++ | **$50+ USD** per bounty | *No Fork (Hosted on GitLab only)* |

### 🛠️ Execution Protocol for OSM Tasks
When the user requests to inspect or work on an "OSM" repository:
1. **Locate Target Fork:** Reference the user's fork above and run checking/git operations locally.
2. **Read CONTRIBUTING.md:** Prior to writing code, always locate and read `CONTRIBUTING.md` inside the project to align with contribution rules (coding standard, tests, issue assignment).
3. **Autonomous Setup:** Run system setups (dependencies, environments) autonomously using correct language package managers (`bun install`, `npm install`, `pip install`, `flutter pub get`, etc.).
4. **Conventional Commits:** Commit code changes using conventional structures (`fix(bounty-12): <description>`).






---

## 🔐 Password Security — Hashing, Salting, Bcrypt & Argon2

### Core Concepts

**Password Hashing** is a one-way cryptographic transformation. The same input always produces the same output (deterministic). This is why plain hashes alone are **never enough** for password storage.

**Why unsalted hashes fail:**
- Hash tables: pre-computed databases mapping passwords → hashes (instant lookup)
- Rainbow tables: compressed version (space-time tradeoff via reduction chains)
- Dictionary attacks: pre-computed wordlists + common patterns
- Modern GPUs can compute **billions of hashes/second** — unsalted SHA-256 is trivial to crack

**Salting** adds a cryptographically random value per credential before hashing:
```
hash(password + salt) → stored_hash
```
This forces attackers to compute a new hash table per user — making bulk cracking computationally infeasible.

### Salting Rules (OWASP-Compliant)
- ✅ Generate a **new unique salt per credential** (not per user, not system-wide)
- ✅ Use a **CSPRNG** (Cryptographically Secure Pseudo-Random Number Generator)
- ✅ Salt size: **32-64 bytes** minimum
- ✅ Store: `username | salt (cleartext) | hash` together
- ✅ Re-salt on every password reset
- ❌ Never use system-wide salts (defeats the purpose)
- ❌ Never reveal if two users share a password (correlation attack)

### Algorithm Comparison

| Algorithm | Memory Hard | GPU Resistant | OWASP Rec. | Use Case |
|-----------|-------------|----------------|------------|----------|
| **MD5** | ❌ | ❌ | ❌ NEVER | Legacy only |
| **SHA-256** | ❌ | ❌ | ❌ NEVER | Data integrity, NOT passwords |
| **bcrypt** | ✅ (moderate) | ✅ | ✅ Yes | Most production apps |
| **scrypt** | ✅ (high RAM) | ✅ | ✅ Yes | High-security, CPU+RAM bound |
| **Argon2id** | ✅ (best) | ✅ | ✅ **Top Pick** | Modern systems, winner of PHC 2015 |
| **PBKDF2** | ❌ | Partial | ✅ (FIPS context) | FIPS compliance, old systems |

### Argon2 Deep Dive
**Argon2id** = hybrid of Argon2d (data-dependent, GPU-resistant) + Argon2i (data-independent, side-channel resistant)
- **Parameters:** `time` (iterations), `memory` (RAM in KB), `parallelism` (threads)
- **Winner of Password Hashing Competition (2015)**
- Recommended minimum params (2024): `time=2, memory=65536 (64MB), parallelism=2`

### bcrypt Deep Dive
- **Cost factor** (work factor) is adjustable — scales with hardware
- Embeds salt within the output hash string (`$2b$12$...`)
- Max password length: **72 bytes** (silently truncates longer passwords!)
- Widely supported across all languages: Node.js `bcrypt`, Python `bcrypt`, Go `golang.org/x/crypto/bcrypt`
- Recommended cost: **12+** (adjust so hash takes ~100-300ms on your server)

### Production Code Patterns

**Node.js — bcrypt:**
```js
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;

// Storing
const hash = await bcrypt.hash(password, SALT_ROUNDS);

// Verifying
const match = await bcrypt.compare(candidatePassword, storedHash);
```

**Node.js — Argon2:**
```js
const argon2 = require('argon2');

// Storing
const hash = await argon2.hash(password, {
  type: argon2.argon2id,
  memoryCost: 65536,  // 64MB
  timeCost: 2,
  parallelism: 2,
});

// Verifying
const match = await argon2.verify(storedHash, candidatePassword);
```

**Python — bcrypt:**
```python
import bcrypt
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
match = bcrypt.checkpw(candidate.encode(), hash)
```

**Python — Argon2:**
```python
from argon2 import PasswordHasher
ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=2)
hash = ph.hash(password)
ph.verify(hash, candidate)  # raises VerifyMismatchError if wrong
```

### Decision Tree: Which to Use
```
New project (2025)?
  → Use Argon2id (best security, PHC winner)

Legacy Node.js/PHP stack?
  → Use bcrypt (excellent support, battle-tested)

FIPS compliance needed (US government, finance)?
  → Use PBKDF2-SHA256 (FIPS 140-2 certified)

High-security + lots of RAM available?
  → Use scrypt (memory-hard, used by Litecoin)
```

### Breach Response Protocol
If a database breach occurs:
1. **Immediately** treat all passwords as compromised (even if salted)
2. Notify users — force password reset
3. Generate new salts during reset
4. Increase bcrypt cost factor / Argon2 memory if possible
5. Enable MFA for all accounts

### Reference Sources
- Auth0: [Adding Salt to Hashing](https://auth0.com/blog/adding-salt-to-hashing-a-better-way-to-store-passwords/)
- Proton: [Password Hashing and Salting](https://proton.me/blog/password-hashing-salting)
- Stytch: [Argon2 vs bcrypt vs scrypt](https://stytch.com/blog/argon2-vs-bcrypt-vs-scrypt/)
- GitHub: [chandanagrawal23/System-Design](https://github.com/chandanagrawal23/System-Design) — PDFs: `PasswordHashing_Notes.pdf`, `BcryptArgon2_Notes.pdf`, `JWT_Notes.pdf`

---

## 📊 AlgoTracker — DSA Practice Platform

**URL:** [algotracker.in](https://www.algotracker.in)
**Creator:** Chandan Agrawal
**Tech Stack:** HTML, CSS, JavaScript (Materialize CSS + Google Fonts Inter)

### What AlgoTracker Is
A free web-based DSA practice tracker with:
- **800+ DSA problems** organized by topic
- **Blind75** curated list (best for 2-week interview prep)
- **LeetCode 150** list (best for 1-2 month prep)
- **SQL** challenges
- **System Design (LLD & HLD)** section
- **C++ solutions** bundled
- Progress tracking (mark problems as solved)
- Google Analytics integration for usage tracking

### Architecture Notes
- Pure HTML/JS frontend — no framework, uses Materialize CSS v1.0.0
- SEO optimized (full meta tags, canonical URLs, OG tags)
- Lightweight — loads fast, no backend required
- All content is client-side JavaScript rendered

### How to Use for Interview Prep
- **2 weeks to interview:** Focus on Blind75 list
- **1-2 months:** Work through LeetCode150
- **Ongoing:** Use the DSA tab to systematically cover all topics
- Track progress by marking problems complete
- Reference bundled C++ solutions to understand optimal patterns

### Reference for Agent
When building similar DSA/coding tools, model structure after AlgoTracker:
- Topic-based organization (Arrays, Trees, DP, Graphs, etc.)
- Visual progress tracking
- Clean, mobile-responsive design
- No auth required for basic tracking (localStorage)


---

## 🗺️ AI Engineering Roadmap 2026 — 5-Month Production Track

> Source: *Realistic AI Engineering Roadmap for 2026*
> Philosophy: **Fundamentals → Retrieval → Agents → Production → Safety** (in this exact order)

---

### ⚠️ Core Warning (Encode This Permanently)
- Do NOT touch LangChain/frameworks until you've built RAG from primitives
- Do NOT skip foundation phase — it's why most people get stuck on agents
- Prototypes ≠ Production. Production = traceability + observability + evals + rollback

---

### Phase 1: Foundation (Month 1–2)

**Goal:** Technical base before touching any orchestration framework.

| Topic | What to Do |
|-------|-----------|
| **Python Mastery** | Async programming, decorators, type hints, clean modular code. Move beyond tutorials. |
| **Git + APIs + SQL** | Non-negotiable. Build FastAPI/Flask apps. Practice SQL with PostgreSQL or DuckDB. |
| **Docker Fundamentals** | Containerize local env. Multi-stage builds to keep AI images small. |
| **LLM Mechanics** | Tokens, context windows, temperature, sampling, embeddings — before any framework. |
| **Raw API Integration** | Call OpenAI/Claude APIs directly with raw `requests`. No frameworks yet. |

**YouTube Channels:**
- `Corey Schafer` — Python fundamentals and practical projects
- `ArjanCodes` — Clean Python engineering, architecture, type-safe coding
- `3Blue1Brown` — Visual intuition for neural networks and math
- `DeepLearning.AI` — Structured beginner-to-intermediate AI education
- `Krish Naik` — Practical AI, ML, Python, deployment

**Courses:**
- Python for Everybody — Python basics and momentum
- DeepLearning.AI: AI for Everyone — AI landscape without deep math
- DeepLearning.AI: ChatGPT Prompt Engineering for Developers

---

### Phase 2: Core Skills & Infrastructure (Month 2–3)

**Goal:** Retrieval, vector storage, context handling, agent primitives — from scratch.

| Topic | What to Do |
|-------|-----------|
| **RAG from Scratch** | Build retrieval-augmented generation pipeline manually — no LangChain |
| **Vector Databases** | Pinecone, ChromaDB, or pgvector. Understand HNSW and IVF indexing concepts |
| **GPU Infrastructure** | Local model runtimes: Ollama or vLLM. NVIDIA container tooling basics |
| **Context Engineering** | Dynamic context windows, relevant memory, retrieval quality — beyond prompt writing |
| **Agent Primitives** | Build a small ReAct loop from scratch — understand reasoning, tool use, execution |

**YouTube Channels:**
- `Matthew Berman` — local models, AI tooling, practical infra
- `James Briggs` — RAG systems, retrieval, embeddings, vector databases
- `AssemblyAI` — LLM internals, embeddings, AI engineering explainers

**Courses:**
- DeepLearning.AI: Building Systems with the ChatGPT API
- Pinecone learning resources — hands-on retrieval
- Hugging Face course (selected sections) — tokenization, embeddings, transformers

---

### Phase 3: Agentic AI & Orchestration (Month 3–4)

**Goal:** Multi-agent systems, tool use, memory, MCP, evaluation — after building single agent from scratch.

| Topic | What to Do |
|-------|-----------|
| **Multi-Agent Systems** | CrewAI, LangGraph — ONLY after building single-agent loop from scratch |
| **Tool Use & Function Calling** | Understand how agents call tools under the hood, not just framework wrappers |
| **MCP (Model Context Protocol)** | Emerging standard for connecting models to tools and context — learn it now |
| **Memory Architectures** | Short-term, long-term, and episodic memory patterns |
| **Agent Evaluation** | Reliability, task completion, hallucination rates, failure case testing |

**YouTube Channels:**
- `AI Jason` — practical agent workflows and applied AI building
- `LangChain official` — orchestration patterns (only after you know primitives)
- `Simon Willison` — high-signal AI, tool-use, product-grade AI thinking

**Courses:**
- DeepLearning.AI short courses on agents and orchestration
- LangGraph tutorials (after single-agent comfort)

---

### Phase 4: Production, MLOps & AIOps (Month 4–5)

**Goal:** Ship and operate. This is where tutorials stop and real engineering starts.

| Topic | Tool / Action |
|-------|--------------|
| **Fine-tuning** | LoRA / QLoRA — parameter-efficient, works on GTX 1650 Ti with 4GB VRAM |
| **LLMOps** | Version prompts, configs, datasets, and evaluations — not just code |
| **Monitoring & Tracing** | Langfuse or Helicone — track traces, latency, quality, cost |
| **Evaluation Frameworks** | RAGAS or golden test sets — measure if system improves over time |
| **Experiment Tracking** | MLflow or Weights & Biases — prompt, run, and model tracking |
| **Data Versioning** | DVC — if datasets or retrieval corpora change often |
| **CI/CD for AI** | GitHub Actions — run tests/evals when prompts, retrieval, or models change |
| **Scalable Serving** | KServe or Seldon Core — Kubernetes-based model serving |
| **Cloud Deployment** | Pick ONE: AWS / GCP / Azure — Docker + basic deployment |
| **Semantic Caching** | GPTCache — cut costs and improve repeated-response speed |
| **AIOps** | AI for log analysis, anomaly detection, auto-remediation |

**YouTube Channels:**
- `MLOps.community` — production ML and LLMOps
- `Hugging Face` — fine-tuning, open models, inference, deployment
- `Unsloth` — fast LoRA and QLoRA experimentation
- `TechWorld with Nana` — DevOps, Docker, Kubernetes, cloud

**Courses:**
- Hugging Face course — transformers, fine-tuning, inference
- Weights & Biases learning content — experiment tracking and observability
- Terraform beginner courses — reproducible cloud infrastructure

---

### Phase 5: Safety, Ethics & Governance (Ongoing — Not a Separate Phase)

**Build this alongside everything else — not at the end.**

| Topic | Action |
|-------|--------|
| **Prompt Injection** | Treat as real production risk — especially with tool-using agents and RAG |
| **Jailbreaking & Output Filtering** | Understand manipulation vectors, add practical safeguards |
| **Data Privacy** | Never send PII/sensitive data to external APIs without strict controls |
| **Guardrails** | NeMo Guardrails or custom filtering pipelines for risky outputs |
| **Compliance** | EU AI Act basics — companies increasingly ask about governance in interviews |
| **Red Teaming** | Regularly test: prompt injection, tool abuse, unsafe outputs, retrieval leaks |

**Resources:**
- `Learn Prompting` — attack patterns, prompt injection, defensive thinking
- `Simon Willison` — safety commentary, model behavior, ecosystem changes
- EU AI Act official summaries

---

### 5-Month Execution Plan (Compressed Reference)

```
Month 1: Python seriously + Git daily + 1 API app + SQL basics + raw LLM calls
Month 2: RAG from scratch + 1 vector DB deep + Ollama local + simple ReAct agent
Month 3: Multi-agent workflow + memory + tool use + MCP basics + start evals
Month 4: Fine-tune small model (LoRA) + Langfuse + experiment tracking + CI/CD for prompts
Month 5: Deploy full AI app + monitoring + semantic caching + safety/red-team + write architecture note
```

---

### Resource Priority Matrix

| Category | Why It Matters | Best Channels |
|----------|----------------|---------------|
| Python Engineering | AI engineers ship code, not notebooks | Corey Schafer, ArjanCodes |
| AI Intuition | Understand failures by understanding internals | 3Blue1Brown, AssemblyAI |
| Structured Learning | Prevent random learning, build sequence | DeepLearning.AI, Hugging Face |
| Hands-on Projects | Makes concepts stick, becomes portfolio proof | Krish Naik, Matthew Berman, James Briggs |
| Agentic Systems | Tool use, memory, orchestration — now central | AI Jason, LangGraph |
| Production AI | What companies actually hire for | MLOps.community, TechWorld with Nana |
| Safety & Governance | Enterprise AI requires this from day one | Learn Prompting, EU AI Act |

### For Absolute Beginners — Start With These 3 Only
1. **3Blue1Brown** — intuition and fundamentals
2. **DeepLearning.AI** — structured guided learning
3. **Krish Naik** — practical implementation and projects

---

### Tools Installed in `/home/aditya/.venvs/ml` for This Roadmap
| Tool | Phase | Purpose |
|------|-------|---------|
| `ollama` (v0.24.0) | Phase 2 | Local LLM runtime — run Llama, Mistral, Phi locally |
| `chromadb` | Phase 2 | Vector database for RAG pipelines |
| `langchain` + `langgraph` | Phase 3 | Orchestration (after primitives) |
| `crewai` | Phase 3 | Multi-agent framework |
| `langfuse` | Phase 4 | LLM tracing, monitoring, cost tracking |
| `ragas` | Phase 4 | RAG evaluation framework |
| `mlflow` | Phase 4 | Experiment tracking |
| `dvc` | Phase 4 | Data versioning |
| `fastapi` + `uvicorn` | Phase 1 | API building |

---

