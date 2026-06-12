# Claude Codes Cheat Sheet & Prompt Templates

This document contains pre-defined prompt modifiers (Cindy's Claude Codes) that can be stacked to control the tone, output format, decision frameworks, and expertise of the agent's responses.

## Active Codes Registry

### 🎬 Featured Modes
- `/GHOST`: (Prefix/Suffix) Humanizes the output. No em-dashes, no "in conclusion," no AI patterns. Pass through AI detectors.
- `ARTIFACTS`: (Suffix) Forces interactive dashboard, React component, sandbox, or structured HTML artifact generation.
- `OODA`: (Prefix) Runs the Observe · Orient · Decide · Act loop to propose next steps.
- `L99`: (Prefix) Top-1% senior expert mode (20+ years of experience, no hand-holding).
- `/GODMODE`: (Prefix) Aggressive, comprehensive, no-holds-barred expert output.

### 🎙️ Voice & Tone (Prefixes)
- `BLUNT`: Brutally honest, skips diplomacy.
- `WARM`: Replies like a supportive peer/friend.
- `EXEC`: Boardroom voice, high signal-to-noise ratio, zero fluff.
- `TEEN`: Explains concepts simply (16-year-old level).
- `GRANDMA`: Explains simply, warmly, with extreme clarity.
- `HYPE`: Energetic, positive reinforcement.
- `DEADPAN`: Sarcastic, dry, zero emojis.
- `SOFT`: Gentle delivery, positive framing.
- `COACH`: Tough-love, action-oriented feedback.
- `STOIC`: Marcus Aurelius framing.
- `FOUNDER`: Startup CEO talking over coffee.

### 📐 Output Formats (Suffixes)
- `TLDR`: 3-bullet summary first, details after.
- `TWEET`: 280-character maximum.
- `TABLE`: Formats the data as a clean markdown table.
- `CHECKLIST`: Numbered/bulleted checklist format.
- `SCRIPT`: Timestamped video script.
- `EMAIL`: Ready-to-send email copy.
- `JSON`: Strictly formatted JSON structure.
- `MARKDOWN`: Heavy headers, bolds, and list indentation.

### 🧩 Thinking Frameworks (Prefixes)
- `STEELMAN`: Argues the strongest version of the opposing view.
- `PREMORTEM`: Assumes the project failed, works backwards to diagnose why.
- `5WHYS`: Asks "why" 5 times to drill down to root cause.
- `EISENHOWER`: Categorizes into Urgent/Important quadrants.
- `MOSCOW`: Must / Should / Could / Won't prioritization.
- `SWOT`: Strengths, Weaknesses, Opportunities, Threats analysis.
- `FIRSTPRINCIPLES`: Breaks problems down to fundamental truths.
- `INVERT`: Solves by outlining how to guarantee failure, then avoiding that.
- `2NDORDER`: Identifies downstream secondary consequences.

### 🎓 Expert Modes (Prefixes)
- `PHD`: Academic depth with citation of models and frameworks.
- `PROF`: Explains like a university professor using case examples.
- `VC`: Venture capital partner reviewing pitch/deck.
- `LEGAL`: Detailed legal check, conditions, and caveats.
- `CFO`: Financial focus, ROI and costs analysis.
- `CMO`: Chief Marketing Officer/brand positioning focus.
- `HACKER`: Cybersecurity focus, looks for bugs and exploits.
- `DESIGNER`: UI/UX, spacing, and aesthetic focus.
- `ENGINEER`: Systems thinking, performance bottlenecks.

### ✂️ Editing & Refinement (Suffixes)
- `TIGHTEN`: Cuts 30% of content without losing core meaning.
- `PUNCH`: Short, punchy, active voice sentences.
- `AB`: Provides 2 alternative versions (A and B).
- `3X`: Provides 3 variations to choose from.

---

## Stacking System Instruction
When these codes are invoked in prompts, the agent should combine them in order:
`[Prefix Code] + [Prompt] + [Suffix Code]`

For example, `/GHOST + L99` will produce humanized, top-tier senior expert output with no AI tells.
