# 🧮 Calculator App

A **premium dark-mode calculator** built with pure HTML, CSS, and vanilla JavaScript — no frameworks, no dependencies.

![Calculator Preview](./preview.png)

## ✨ Features

- **Glassmorphism UI** — animated background orbs, frosted glass cards, premium shadows
- **Dark mode by default** — Apple HIG-inspired `#0a0a0f` background, `SF Pro Display` font stack
- **Full keyboard support** — all digits, operators, Enter, Escape, Backspace, `%`, `h` (history toggle)
- **Chained operations** — `3 + 4 × 5` computes progressively in real-time
- **Calculation history** — slide-in history panel, click any result to recall it
- **Auto-sizing display** — font scales down automatically for long numbers
- **Error handling** — division by zero shows `Error` with shake animation, equals with no operand pulses
- **Accessible** — ARIA roles, live regions, keyboard navigation, focus-visible outlines

## 🚀 Usage

Just open `index.html` in any modern browser — zero build step required.

```bash
# Or serve locally with any static server
npx -y serve .
```

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `0–9` | Digit input |
| `.` or `,` | Decimal point |
| `+`, `-`, `*`, `/` | Operators |
| `Enter` or `=` | Calculate |
| `Escape` | Clear all (AC) |
| `Backspace` | Delete last digit |
| `%` | Percent |
| `h` | Toggle history panel |

## 🏗️ Tech Stack

- **HTML5** — semantic, fully accessible
- **CSS** — vanilla, custom properties, `backdrop-filter`, `@keyframes`
- **JavaScript** — ES2022, zero dependencies, strict mode

## 📁 Structure

```
calculator-app/
├── index.html   # Markup & semantic structure
├── style.css    # All styles (tokens, layout, animations)
├── app.js       # Calculator logic + state management
└── README.md
```

---

Made with ❤️ by Aditya Shirsatrao
