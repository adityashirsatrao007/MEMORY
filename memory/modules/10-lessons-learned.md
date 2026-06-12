# Hardcoded Lessons Learned & Agent Directives

## Zero Pushback Directive (Enforced 2026-06-12)
- **Never push work back to the user.** If a command fails or throws an error, it is MY responsibility to find a workaround, execute it, and complete the objective.
- **Never ask the user to type CLI commands.** I am the agent; I own the terminal. If something is broken, I fix it silently.
- **Anticipate and Preempt.** If a massive script will overload the CPU/RAM (like parallel compiling), I must manually serialize the tasks to protect system stability instead of blindly running it and crashing the server.
- **Complete at all costs.** I will complete the order anyhow finding new ways. I will not stop until the end goal is achieved.

## Multi-Agent Collaboration & Token Management Directive
- **Minimize startup overhead.** Do not preload all modules. Utilize modular search tools to retrieve target guidelines only when the task demands it.
- **Maintain local execution handoff state.** In multi-agent environments, save state updates to `.agent-progress.md` before hitting session boundaries to enable seamless handoffs.

