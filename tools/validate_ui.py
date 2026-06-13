#!/usr/bin/env python3
# Copyright (c) 2026 Aditya Shirsatrao. All rights reserved.
# Proprietary — see LICENSE file. No copying, cloning, or distribution.

from license import require_license
require_license()

import os
import sys
import re

# Banned basic colors that suggest low-effort vibe coding
BANNED_BASIC_COLORS = [
    r'(?:bg|text|border|ring|decoration)-(?:red|blue|green|yellow|purple|pink|indigo)-(?:500|600)',
]

# Approved font families
APPROVED_FONTS = [
    '-apple-system',
    'BlinkMacSystemFont',
    'SF Pro Display',
    'SFProDisplay',
    'Inter',
    'Outfit',
    'Roboto'
]

# Common placeholder patterns
PLACEHOLDERS = [
    r'\bTODO\b',
    r'\bLorem\s+Ipsum\b',
    r'\blorem\b',
    r'\bplaceholder\b',
    r'\btest\s+test\b',
    r'\basdf\b'
]

def check_file(file_path):
    errors = []
    warnings = []
    
    # Only scan web and code files
    ext = os.path.splitext(file_path)[1]
    if ext not in ['.tsx', '.jsx', '.ts', '.js', '.html', '.css', '.vue', '.svelte']:
        return errors, warnings

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return [f"Could not read file: {e}"], []

    for i, line in enumerate(lines, 1):
        # 1. Banned Basic Colors Check
        for pattern in BANNED_BASIC_COLORS:
            match = re.search(pattern, line)
            if match:
                warnings.append(f"Line {i}: Found basic/generic color class '{match.group(0)}'. Use custom HSL, slate, zinc, neutral, or stone for a premium look.")

        # 2. Placeholders Check
        for pattern in PLACEHOLDERS:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                errors.append(f"Line {i}: Found placeholder text/comment matching pattern '{pattern}'. Replace with real, high-quality content.")

        # 3. Check for raw border-style defaults (often look unpolished)
        if 'border ' in line and 'border-neutral' not in line and 'border-zinc' not in line and 'border-slate' not in line and 'border-gray' not in line:
            if 'border-style' not in line and not re.search(r'border-(?:[a-z]+)-\d+', line):
                warnings.append(f"Line {i}: Using raw 'border' without specifying a neutral/slate color. May result in harsh default borders.")

        # 4. Check for font families
        if 'font-family' in line:
            if not any(font in line for font in APPROVED_FONTS):
                warnings.append(f"Line {i}: custom font-family does not include Apple HIG / premium fonts (SF Pro Display, Inter, etc.).")

    return errors, warnings

def main():
    target_dirs = sys.argv[1:] if len(sys.argv) > 1 else ['.']
    total_errors = 0
    total_warnings = 0
    scanned_count = 0

    print("=== Apple HIG / UI Premium Validator ===")
    
    for target in target_dirs:
        if os.path.isfile(target):
            errors, warnings = check_file(target)
            scanned_count += 1
            if errors or warnings:
                print(f"\n📄 File: {target}")
                for err in errors:
                    print(f"  ❌ ERROR: {err}")
                    total_errors += 1
                for warn in warnings:
                    print(f"  ⚠️ WARN:  {warn}")
                    total_warnings += 1
        elif os.path.isdir(target):
            for root, dirs, files in os.walk(target):
                # Ignore dependencies, build artifacts, and templates
                if any(x in root for x in ['node_modules', '.next', 'dist', 'build', '.venv', 'venv', '.git', 'templates']):
                    continue
                for file in files:
                    full_path = os.path.join(root, file)
                    errors, warnings = check_file(full_path)
                    scanned_count += 1
                    if errors or warnings:
                        rel_path = os.path.relpath(full_path, target)
                        print(f"\n📄 File: {rel_path}")
                        for err in errors:
                            print(f"  ❌ ERROR: {err}")
                            total_errors += 1
                        for warn in warnings:
                            print(f"  ⚠️ WARN:  {warn}")
                            total_warnings += 1

    print(f"\n📊 Summary: Scanned {scanned_count} files.")
    print(f"  Errors:   {total_errors}")
    print(f"  Warnings: {total_warnings}")
    
    if total_errors > 0:
        print("\n❌ UI Validation failed. Please clean up placeholder values before committing.")
        sys.exit(1)
    else:
        print("\n✅ UI Validation passed! (Style warning checks completed)")
        sys.exit(0)

if __name__ == '__main__':
    main()
