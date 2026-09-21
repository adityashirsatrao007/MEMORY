---
created: 2026-08-26T10:27:18.376117
category: skills
tags: ["latex", "resume", "formatting", "overleaf", "ats"]
---

## LaTeX Resume Formatting Rules (Learned the Hard Way)

### Preamble (proven, copy-paste safe)
- `\documentclass[letterpaper,10pt]{article}` — use 10pt, NOT 11pt
- `\input{glyphtounicode}` — ATS PDF text extraction
- `\renewcommand{\rmdefault}{ptm}` + `\usepackage{mathptmx}` — Times New Roman
- Margins: `\addtolength{\oddsidemargin}{-0.5in}`, same for evenside, `\textwidth{+1in}`, `\topmargin{-.5in}`, `\textheight{1.0in}`, `\footskip}{5pt}`
- `\setlist{topsep=0pt,itemsep=0pt,parsep=0pt,partopsep=0pt}` — tight lists
- Section: `\titleformat{\section}{\vspace{-4pt}\scshape\raggedright\large}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]` — use `\color{black}`, NOT colored sections
- `\pdfgentounicode=1` — second ATS pass

### Custom Commands (standard sb2nov pattern)
- `\resumeItem{...}` — single bullet item
- `\resumeSubheading{Title}{Date}{Subtitle}{Location}` — experience/education entry
- `\resumeProjectHeading{Name | Tech | Link}{Date}` — project entry
- `\resumeSubHeadingListStart/End` — `itemize` with `leftmargin=0.15in, label={}`
- `\resumeItemListStart/End` — plain `itemize`, ends with `\vspace{-5pt}`

### Common Mistakes to Avoid
- NEVER use `\color{darkblue}` or colored section headers — use `\color{black}` only
- NEVER use 11pt — use 10pt for 1-page resumes
- NEVER skip `\footskip{5pt}` — fancyhdr warning
- NEVER forget `\input{glyphtounicode}` — ATS can't read PDF
- Overfull `\hbox` in skills section: use `\\` line breaks carefully, test with `\small`
- Compile TWICE to resolve cross-references

### File Locations
- Resumes dir: `/home/aditya/Documents/Default Project/internship-kit/resumes/`
- Compile: `pdflatex -interaction=nonstopmode filename.tex`
