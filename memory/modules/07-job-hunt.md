# Job Hunting — ATS Resume Optimization & LinkedIn Strategy

> Extracted from `GEMINI.md`.

---

## 📄 Latex Resume & ATS Optimization Protocols

When tasked with generating, modifying, or auditing resumes (especially LaTeX format), apply these 5 key vectors:

### 1. Skills Gap Analysis
- Analyze target JDs side-by-side with current resume
- Identify top 5 missing skills and map to quantifiable achievements

### 2. Tailored Bullet Points
- 4-6 high-impact bullets per role
- Start with strong active verb (Architected, Spearheaded, Optimized)
- Incorporate target keywords naturally
- Quantify accomplishments (e.g., "reduced latency by 35%")

### 3. Readability & ATS Compatibility
- Standard section headings: `Education`, `Experience`, `Skills`, `Projects`
- No tables, columns, text boxes, or charts
- Standard fonts (Latin Modern, Computer Modern, Arial, Helvetica)

### 4. Relevant Professional Summary
- 4-5 sentence hook
- Natural keyword integration from JD
- Forward-looking value proposition

### 5. ATS Keyword Integration
- Avoid keyword stuffing
- Place key terms naturally in Summary, Experience, Skills
- Suggest missing sections, certifications

---

## 🎯 AI Job Hunting System — 5-Step Framework (AI Action Letter)

> Source: *AI Action Letter* by Abhijay Arora Vuyyuru
> Newsletter: [AI Action Letter on Substack](https://substack.com/@abhijayaroravuyyuru)

### Core Insight
> Mass applying with a generic resume = 0 interviews. 75% of resumes rejected by ATS.

### Step 1: ATS-Proof Resume Rules

**Format (non-negotiable):**
- ✅ Single-column layout (multi-column breaks ATS)
- ✅ No icons, tables, images, or graphics
- ✅ Standard headers: `Education`, `Experience`, `Skills`, `Projects`
- ✅ Reverse chronological
- ✅ Export as PDF
- ✅ One page (unless 10+ years)

**Bullet Formula:**
```
[Action Verb] + [What You Did] + [Quantified Result]
```

| ❌ Weak | ✅ Strong |
|---------|-----------|
| "Responsible for managing social media accounts" | "Grew Instagram following from 2K to 50K in 6 months (+340% engagement)" |

**Rule:** At least **70% of bullets must include a metric.**

**Strong Action Verbs:** Architected, Spearheaded, Optimized, Automated, Delivered, Scaled, Reduced, Increased, Launched, Mentored, Audited, Integrated

### Step 2: LinkedIn Optimization — AI Prompt

Copy this prompt into Claude/ChatGPT with LinkedIn content:

```
Here is the scraped content of a LinkedIn profile:
<profile>
{{PASTE LINKEDIN PROFILE CONTENT HERE}}
</profile>

The user's goal is: {{GOAL}}

Please analyze across these dimensions:
1. Headline — Rewrite for keyword-rich, role-specific value
2. About/Summary — Compelling story with clear hook in line 1
3. Experience bullets — Outcome-driven with numbers
4. Featured section — What should be pinned?
5. Skills & Keywords — What's missing for SEO?
6. Creator/Posting signals — Gaps in niche authority?
7. CTA — Clear next step for visitors?

Format: [Section] → [Issue] → [Rewrite or Recommendation]
```

### Step 3: Automate Job Discovery

**Solution — n8n + Apify pipeline (~$7/month):**
- Scrapes LinkedIn for jobs posted in **last 24 hours**
- Filters by role, location, industry
- Returns top 5 most recent listings per search
- Delivers daily

**Hiring Manager Search Patterns:**
| Pattern | Search String |
|---------|--------------|
| Direct Intent | `"I'm hiring"` OR `"looking for a"` OR `"open role on my team"` |
| Call to Action | `"DM me"` OR `"send me your resume"` OR `"drop your portfolio"` |
| Team Growth | `"growing the team"` OR `"excited to announce"` OR `"just opened a req"` |

> A **direct LinkedIn DM to a hiring manager** is 10x more effective than Easy Apply.

### Step 4: Auto-Tailor Resume Per Job (One-Click Workflow)

**n8n Automation Stack:**
| Tool | Cost | Role |
|------|------|------|
| n8n | ~$7/mo | Workflow orchestration |
| Apify | Free tier | LinkedIn job scraping |
| Google Gemini API | Free tier | Resume rewriting |
| Google Docs | Free | Tailored resume output |
| Gmail | Free | Daily summary emails |

**Workflow:**
1. JDs fetched from Step 3
2. AI extracts keywords (skills, tools, qualifications)
3. Base resume rewritten to match JD language
4. New Google Doc per tailored resume
5. Summary email with all links

### Step 5: LinkedIn Content Strategy

**Cadence:** 3x per week

**Post Formula:**
- Bold/punchy first line (hook)
- Short paragraphs (1-2 sentences)
- End with a question or CTA

### Quick-Start Checklist
- [ ] Step 1: Create ATS-friendly resume (single column, PDF, 70%+ quantified bullets)
- [ ] Step 2: Run LinkedIn through AI optimization prompt
- [ ] Step 3: Set up Apify + n8n for daily job scraping
- [ ] Step 4: Configure auto-tailoring workflow (Gemini API + Google Docs)
- [ ] Step 5: Pick 3 post ideas and publish first LinkedIn post this week

### Visa Note
For H-1B alternatives: **EB-1A** and **O-1 visas** are viable paths for STEM candidates.
