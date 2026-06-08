# Global Lessons Learned & Error Memory

This file serves as the permanent, cross-project memory bank for all errors encountered by the agent. 

**Protocol for the Agent:**
Every time a command fails, a script crashes, or a bug is resolved, the agent MUST log the error signature and its standardized solution here. Before starting any new task, the agent will implicitly cross-reference this memory bank to ensure historical mistakes are never repeated.

### 1. `apt-get update` 404 Errors on Unsupported OS Versions
**Error Signature:**
```
Err:19 https://packages.microsoft.com/repos/azure-cli resolute Release
  404  Not Found [IP: 2620:1ec:46::68 443]
E: The repository '...' does not have a Release file.
```
**Root Cause:**
When running `sudo apt-get update && sudo apt-get install <pkg>`, the entire command chain fails if ANY third-party PPA or package repository returns a 404 or fails to resolve (which happens frequently on new OS versions like Ubuntu 26.04 "resolute" where packages aren't released yet).

**Standard Resolution:**
Never strictly chain `apt-get update && apt-get install`. If an update is required, handle the update failure gracefully or remove broken PPAs. If the package cache is already warm, just run `sudo apt-get install -y <pkg>` directly to bypass the unmaintained repository blockers.

### 2. Broken Agent Symlinks Pointing to Wrong Target After GEMINI.md Restructure
**Error Signature:**
```
opencode/AGENTS.md -> ../../GEMINI.md
But resolved to: ~/Desktop/Projects/MEMORY/LESSONS_LEARNED.md (WRONG!)
Expected: ~/Desktop/Projects/MEMORY/GEMINI.md
git status showing 197KB files as "modified" (type changed T)
```
**Root Cause:**
When a session agent converts multiple regular files (`.clinerules`, `.cursorrules`, `AGENTS.md`, `CLAUDE.md`, `opencode/AGENTS.md`, etc.) into symlinks targeting GEMINI.md, the relative path for files in subdirectories (like `opencode/AGENTS.md`) must be calculated from that subdirectory. Using `../../GEMINI.md` from `opencode/` goes up 2 levels to `MEMORY/../` which is wrong — it accidentally resolves to whatever file was previously at the parent symlink level.

**Standard Resolution:**
Never use `../../` relative symlinks for files inside the repo. Use either:
- A) Absolute path: `ln -sf /home/aditya/Desktop/Projects/MEMORY/GEMINI.md opencode/AGENTS.md`
- B) Correct relative: From `opencode/`, the correct path is `../GEMINI.md` (one level up, not two)
- C) Verify after creation: `readlink -f opencode/AGENTS.md` must equal `readlink -f GEMINI.md`
- Before finalizing, always run a batch verification:
  ```bash
  for f in .clinerules .cursorrules .windsurfrules AGENTS.md CLAUDE.md opencode/AGENTS.md .github/copilot-instructions.md; do
    [ "$(readlink -f "$f")" = "$(readlink -f GEMINI.md)" ] || echo "BROKEN: $f"
  done
  ```

### 3. Using Legacy CLI Tools Instead of Modern Alternatives (ZERO-TOKEN Violation)
**Error Signature:**
```
Used: ls, head, cat, echo, grep
Should have used: eza, bat, rg, glow, sd
```
**Root Cause:**
The agent has a comprehensive zero-token CLI rulebook installed (in GEMINI.md) that mandates `eza` over `ls`, `bat` over `cat`, `rg` over `grep`, `glow` over `cat` for markdown, `sd` over `sed`, `procs` over `ps`, `dust` over `du`, etc. Using legacy tools wastes tokens on verbose output and bloats context.

**Standard Resolution:**
- Before every bash call, stop and ask: "Is there a modern CLI for this?"
- `ls` → `eza -la --git`
- `cat file` → `bat file`
- `grep -r` → `rg`
- `cat README.md` → `glow README.md`
- `head/tail file` → `bat --line-range N:M file`
- `sed` → `sd`
- `ps aux` → `procs`
- `du -sh` → `dust`
- `find` → `fd`

### 4. OpenCode Delegation Violation — Ran Heavy Edits in Antigravity Context (Wasted Tokens)
**Error Signature:**
```
Task: Convert 7 duplicated 197KB files to symlinks
Method: Direct Antigravity execution (rm + ln -sf for each file)
Should have used: opencode run "convert all duplicated GEMINI.md copies to symlinks"
```
**Root Cause:**
GEMINI.md rule mandates: "NEVER do multi-file edits, refactoring, or heavy coding directly in Antigravity's context. ALWAYS delegate via `opencode run`." Multi-file symlink operations consumed Antigravity tokens that should have been delegated to OpenCode's credit system.

**Standard Resolution:**
- Any task involving 2+ files → `opencode run "<task>"`
- Only use Antigravity for: coordination, single-line fixes, CLI commands, answering questions
- Fallback: If OpenCode fails → silently fall back, never stop work

### 5. Skipped Project Pre-Flight Sequence (onefetch → eza --tree → tokei → rg)
**Error Signature:**
```
Entered MEMORY repo. Did:
  ❌ ls (wrong tool)
  ❌ head (wrong tool)
  ❌ Read tool (token-heavy)
  ❌ git log --oneline (without onefetch first)

Should have done:
  ✅ onefetch        — instant repo summary
  ✅ eza --tree      — structure overview
  ✅ tokei           — code breakdown by language
  ✅ rg "TODO|FIXME" — find known issues
  ✅ glow progress.md — current status
```
**Root Cause:**
GEMINI.md section "AGENT TOKEN-SAVING PRIORITY ORDER" prescribes a specific 5-step sequence before touching any codebase. Skipping it means reading files blind and wasting context tokens.

**Standard Resolution:**
Every time I enter a new repo (or a known one):
```bash
onefetch && eza --tree --level 2 --git-ignore && tokei && rg "TODO|FIXME|HACK" . && glow memory-bank/progress.md
```
This is 5 CLI calls, reads zero files, and gives full context.

### 6. Used Read Tool Instead of CLI-First Approach (Token Bloat)
**Error Signature:**
```
Used Read tool to open: GEMINI.md (multiple sections via bat --line-range)
Should have done: grep/rg for specific sections, bat --line-range for headers only
Read README.md via Read tool instead of: glow README.md
```
**Root Cause:**
GEMINI.md "CLI-first" rule: "Never use view_file or read_file to search code or inspect logs when commands like grep, tail, head, or find can isolate the exact output." Reading 1400+ lines of GEMINI.md in 7 Read calls consumed ~200K input tokens that CLI equivalents could have done with <5K.

**Standard Resolution:**
- Need a section of GEMINI.md? → `rg "^## " GEMINI.md` for TOC, `bat --line-range X:Y GEMINI.md` for specific section
- Need to understand a file? → `glow` for markdown, `bat` for code
- Read tool ONLY for: binary inspection, images, PDFs, or files that CLI tools cannot handle

### 7. Used `git diff` Without `| delta` (Missed Syntax Highlighting)
**Error Signature:**
```
Used: git diff (plain, no pipe)
Should have used: git diff | delta
```
**Root Cause:**
GEMINI.md mandates `delta` for all git diffs — it provides syntax highlighting, word-level diffs, and side-by-side view. Plain `git diff` wastes context on unformatted output.

**Standard Resolution:**
Every diff: `git diff | delta` or `git diff --stat` for summary.

### 8. Did Not Run Quality Checks Before Declaring Work Done
**Error Signature:**
```
Skipped: sober check ., agentlint check, pre-commit run --all-files
```
**Root Cause:**
GEMINI.md "Code Review & Documentation Protocol" mandates running sobriety audit, AI-friendliness audit, and pre-commit hooks before declaring any task done.

**Standard Resolution:**
Before any "done" marker:
```bash
semgrep scan --config auto .  # SAST + logic bugs (replaces sober)
pre-commit run --all-files     # lint/format/secret scan
```

### 9. Documented Tools That Aren't Actually Installed
**Error Signature:**
```
GEMINI.md section "Specialized Tool Matrix" mentions:
  - hackingtool (NOT INSTALLED)
  - feast (NOT INSTALLED)
  - milvus (NOT INSTALLED)
  - sober (npm package sober-coding, NOT INSTALLED)
Agent reads these rules, tries to use them, command fails with "not found"
```

**Root Cause:**
Tools get documented in agent rules during research/planning but never verified with `which <tool>` before committing to GEMINI.md. Over time, documented tools drift from installed reality.

**Standard Resolution:**
After any edit to the "Specialized Tool Matrix" or "Installed Agent Tools" sections, run:
```bash
for tool in $(rg "^\`([a-z-]+)\`" GEMINI.md -o --no-filename); do which "$tool" >/dev/null || echo "MISSING: $tool"; done
```
If any tool returns "MISSING", either install it or remove the reference.

### 10. Hardcoded Absolute Paths Break After Directory Restructure
**Error Signature:**
```
GEMINI.md had:  /home/aditya/Desktop/Projects/MEMORY/memory-bank/progress.md
After restructure:  /home/aditya/Desktop/Projects/MEMORY/memory/memory-bank/progress.md
Path references in GEMINI.md still point to old location → broken links
```

**Root Cause:**
Hardcoding absolute paths to repo files in GEMINI.md rules. When directories are reorganized (e.g., memory-bank/ → memory/memory-bank/), all absolute path references break silently.

**Standard Resolution:**
Use relative paths from repo root for internal references:
```
BAD:  /home/aditya/Desktop/Projects/MEMORY/memory-bank/progress.md
GOOD: memory/memory-bank/progress.md
```
After any directory restructure, grep for old paths:
```bash
rg "/home/aditya/Desktop/Projects/MEMORY/old-path" GEMINI.md
```

### 11. Reference Projects & Bloat Creep Into Config Repo
**Error Signature:**
```
templates/ contains 200+ files of full Next.js reference projects
  - frontend-v0-reference (100+ TSX/TS files, 0 references anywhere)
  - fullstack-bolt-reference (100+ TS/TSX files, 0 references anywhere)
Purpose of MEMORY repo: agent configs + rules. NOT reference apps.
```

**Root Cause:**
During coding sessions, agent generates reference/template projects to demonstrate patterns, then stores them in the MEMORY repo "for later use" — but nothing ever references them. They silently bloat the repo by 200+ files.

**Standard Resolution:**
Before committing to the MEMORY repo, every new file must pass the "MEMORY test":
```
Is this file a config, rule, tool script, or doc for agent behavior?
  → YES: belongs here
  → NO (e.g. full app source, reference project, generated scaffold):
    → Delete it or move it to /tmp/ or a dedicated project repo
```

### 12. Agentignore / Gitignore Paths Not Updated After Restructure
**Error Signature:**
```
.agentignore had:  vector_db/
Actual location:   memory/vector_db/
Agent reads the directory, finds a 164K binary SQLite file → wasted tokens
```

**Root Cause:**
When directories are moved during restructure, `.agentignore` and `.gitignore` patterns that reference old paths silently stop matching. The agent then wastes tokens reading ignored-now-tracked files.

**Standard Resolution:**
After any file/directory move, run:
```bash
# Check if .agentignore paths still resolve
for pattern in $(rg "^[a-z_]" .agentignore -o); do
  find . -path "./${pattern}" -type f 2>/dev/null | head -1 && echo "  → STILL MATCHES"
done

# Same for .gitignore
for pattern in $(rg "^[a-z_]" .gitignore -o); do
  find . -path "./${pattern}" -type f 2>/dev/null | head -1 && echo "  → STILL MATCHES"
done
```

### 13. Empty Directories Survive Cleanup

### 14. NEVER Delete Files Based on Assumptions — Full Verification Required
**Error Signature:**
```
Files deleted: 26 files across config/, docs/, memory-bank/, templates/, dotfiles/
Method: read first 5 lines + grep headers → assumed "stale" → deleted
Should have done: read each file fully, compare line-by-line with modules
```

**Root Cause:**
Systematic assumption error — files classified as "stale" based on path + header grep only. None of these constitute "complete knowledge."

**Standard Resolution — The "Zero Assumption" Protocol:**
Before ANY deletion of existing tracked files, ALL 5 checks must pass:

```
1. READ THE FULL FILE — `bat file.md` or `glow file.md` (never head/tail only)

2. COMPARE CONTENT — for every section, verify it exists in modules:
   → `rg "unique phrase from paragraph" memory/modules/*.md`
   If any phrase is NOT found → file has UNIQUE content → DO NOT DELETE.

3. TRACE DEPENDENCIES — check if anything depends on this file:
   → `rg "filename" .` — symlinks, references, imports
   → `find ~ -type l 2>/dev/null | xargs -I{} sh -c 'readlink "{}" | grep -q "filename" && echo "{}"'`

4. CHECK VECTOR DB — file might be chunked into ChromaDB:
   → `curl -s "http://localhost:8082/api/search?q=key+phrase"`

5. THE 24-HOUR RULE (files > 100 lines):
   → If uncertain, leave it. Tag for next session.
   → If > 500 lines and not fully read → DO NOT DELETE.

EXECUTE ONLY AFTER ALL 5 PASS. Failure = critical error.
```
**Error Signature:**
```
scratch/          — empty
docs/images/      — empty
docs/diagrams/    — empty
graphify-out/     — empty
4 empty dirs wasting `ls`/`eza` output lines
```

**Root Cause:**
During restructuring, source directories get emptied (content moved or deleted), but the empty directory remains. Agents then list them, see nothing, and waste a line of output per empty dir.

**Standard Resolution:**
At the end of any session, run:
```bash
find . -type d -empty -not -path './.git/*' -delete 2>/dev/null
```
