#!/usr/bin/env python3
"""Generate a compact skill catalog from all SKILL.md files.
Output: skills_catalog.md (name | description | path format)
Also generates skills_catalog.json for programmatic access.

Usage:
  python3 generate_skill_catalog.py              # generate both
  python3 generate_skill_catalog.py --json-only   # json only
  python3 generate_skill_catalog.py --md-only     # markdown only
"""
import json
import os
import re
import sys
from pathlib import Path

MEMORY_ROOT = Path(os.environ.get("MEMORY_ROOT", os.path.expanduser("~/Desktop/Projects/MEMORY")))
SKILL_DIR = MEMORY_ROOT / ".agents" / "skills"
CATALOG_MD = MEMORY_ROOT / "memory" / "skills_catalog.md"
CATALOG_JSON = MEMORY_ROOT / "memory" / "skills_catalog.json"


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from SKILL.md."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            val = val.strip().strip('"').strip("'")
            if val:
                fm[key.strip()] = val
    return fm


def extract_description(content: str, frontmatter: dict) -> str:
    """Get description from frontmatter or first meaningful line."""
    if 'description' in frontmatter:
        desc = frontmatter['description']
        # Truncate if too long
        if len(desc) > 200:
            desc = desc[:197] + '...'
        return desc
    
    # Fallback: first non-heading, non-frontmatter line
    lines = content.split('\n')
    in_frontmatter = False
    for line in lines:
        stripped = line.strip()
        if stripped == '---':
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter or not stripped or stripped.startswith('#'):
            continue
        if len(stripped) > 10:
            return stripped[:200] + ('...' if len(stripped) > 200 else '')
    return '(no description)'


def extract_skills():
    """Extract name + description from all skills."""
    skills = []
    if not SKILL_DIR.exists():
        print(f"Skill dir not found: {SKILL_DIR}", file=sys.stderr)
        return skills
    
    for skill_path in sorted(SKILL_DIR.iterdir()):
        skill_file = skill_path / "SKILL.md"
        if not skill_file.exists():
            continue
        
        content = skill_file.read_text(errors='replace')
        fm = parse_frontmatter(content)
        name = fm.get('name', skill_path.name)
        desc = extract_description(content, fm)
        risk = fm.get('risk', 'unknown')
        
        skills.append({
            'name': name,
            'description': desc,
            'risk': risk,
            'path': str(skill_path.relative_to(MEMORY_ROOT)),
            'dir_name': skill_path.name,
        })
    
    return skills


def write_catalog_md(skills: list):
    """Write compact markdown catalog."""
    CATALOG_MD.parent.mkdir(parents=True, exist_ok=True)
    
    with open(CATALOG_MD, 'w') as f:
        f.write(f"# Skill Catalog ({len(skills)} skills)\n")
        f.write(f"Auto-generated. DO NOT EDIT.\n")
        f.write(f"Updated: {__import__('datetime').datetime.now().isoformat()}\n\n")
        f.write("| # | Skill | Description | Risk |\n")
        f.write("|---|-------|-------------|------|\n")
        for i, s in enumerate(skills, 1):
            desc = s['description'].replace('|', '\\|')
            f.write(f"| {i} | {s['name']} | {desc} | {s['risk']} |\n")
    
    print(f"  Wrote {CATALOG_MD} ({len(skills)} skills)")


def write_catalog_json(skills: list):
    """Write JSON catalog for programmatic access."""
    CATALOG_JSON.parent.mkdir(parents=True, exist_ok=True)
    
    with open(CATALOG_JSON, 'w') as f:
        json.dump({
            'count': len(skills),
            'generated': __import__('datetime').datetime.now().isoformat(),
            'skills': skills
        }, f, indent=2)
    
    print(f"  Wrote {CATALOG_JSON} ({len(skills)} skills)")


def main():
    md_only = '--md-only' in sys.argv
    json_only = '--json-only' in sys.argv
    
    print(f"Scanning {SKILL_DIR}...")
    skills = extract_skills()
    print(f"  Found {len(skills)} skills with SKILL.md")
    
    if not json_only:
        write_catalog_md(skills)
    if not md_only:
        write_catalog_json(skills)
    
    # Stats
    risks = {}
    for s in skills:
        r = s['risk']
        risks[r] = risks.get(r, 0) + 1
    print(f"  Risk breakdown: {risks}")
    print(f"  Total tokens (est): ~{len(skills) * 15}")


if __name__ == '__main__':
    main()
