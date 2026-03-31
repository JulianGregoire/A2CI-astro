#!/usr/bin/env python3
"""Move breadcrumb nav from above hero to below hero on all formation pages."""

import re
import glob
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

files = glob.glob("formation-*.html")
print(f"Found {len(files)} formation files")

for filepath in sorted(files):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Extract the full breadcrumb block (nav + surrounding whitespace)
    breadcrumb_pattern = r'\n*<nav aria-label="Breadcrumb"[^>]*>.*?</nav>\s*'
    match = re.search(breadcrumb_pattern, content, re.DOTALL)
    if not match:
        print(f"  SKIP {filepath}: no breadcrumb found")
        continue

    breadcrumb_block = match.group(0).strip()

    # 2. Remove mt-[104px] from the breadcrumb (no longer directly after header)
    breadcrumb_block = breadcrumb_block.replace('mt-[104px] ', '')

    # 3. Remove the breadcrumb from its current position
    content = content[:match.start()] + "\n\n" + content[match.end():]

    # 4. Add mt-[104px] to the hero section
    content = content.replace(
        '<!-- Hero Section -->\n<section class="relative w-full overflow-hidden bg-black',
        '<!-- Hero Section -->\n<section class="mt-[104px] relative w-full overflow-hidden bg-black'
    )

    # 5. Insert the breadcrumb after the hero </section>, before Qualiopi
    content = content.replace(
        '</section>\n<!-- Qualiopi Certification Section -->',
        '</section>\n\n' + breadcrumb_block + '\n\n<!-- Qualiopi Certification Section -->'
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  OK {filepath}")

print("Done!")
