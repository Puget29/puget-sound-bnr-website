#!/usr/bin/env python3
"""Inject the shared Google Tag Manager + Google Ads blocks into every staged HTML page.

Used by scripts/stage.mjs for the Netlify production build. The snippets come from
tools/tracking.py (which reads data/tracking.json), the same source the WordPress
pipeline uses, so there is exactly one tracking implementation.

    python tools/inject-tracking.py [stage-dir=build/stage]

Idempotent: a page that already contains the GTM snippet is left untouched, so running
the build twice never produces a duplicate container. The GTM <script> goes right after
the viewport meta; the <noscript> fallback goes right after <body>, matching the WordPress
live-page placement.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tracking import tracking_blocks


def main():
    stage = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("build") / "stage"
    head, noscript = tracking_blocks()
    if not head:
        print("inject-tracking: no tracking enabled in data/tracking.json, nothing to inject")
        return
    injected = 0
    for f in sorted(stage.rglob("*.html")):
        html = f.read_text(encoding="utf-8")
        if "googletagmanager" in html:
            continue  # already has tracking; never add a second container
        new, n = re.subn(r'(<meta name="viewport"[^>]*>)', lambda m: m.group(1) + "\n" + head, html, count=1)
        if n != 1:
            print(f"inject-tracking: WARNING no viewport meta in {f}, skipped")
            continue
        if noscript:
            new = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + "\n" + noscript, new, count=1)
        f.write_text(new, encoding="utf-8", newline="")
        injected += 1
    print(f"inject-tracking: injected into {injected} page(s)")


if __name__ == "__main__":
    main()
