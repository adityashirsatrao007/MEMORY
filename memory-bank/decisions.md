# MEMORY — Key Decisions

> Records WHY things were built a certain way.
> Prevents the agent from second-guessing or redoing past decisions.

## Design Decisions
| Decision | Reason | Date |
|----------|--------|------|
| <!-- Agent fills --> | | |

## Technology Choices
| Choice | Alternatives Considered | Why This One |
|--------|------------------------|-------------|
| **OpenCode CLI Delegation** | Executing code edits and multi-file generations directly in Antigravity. | Runs `opencode run "<task>"` for large edits/generation tasks, utilizing local OpenCode billing/tokens instead of Antigravity's tokens. Falls back to direct Antigravity execution if OpenCode runs out of limits or fails. |


