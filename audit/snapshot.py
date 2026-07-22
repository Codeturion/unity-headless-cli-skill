#!/usr/bin/env python3
"""Fetch the Unity CLI reference page and emit a normalized text snapshot.

Deterministic and stdlib only. Strips scripts/styles/nav/footer and all tags,
unescapes entities, and collapses whitespace so a plain `diff` against the
committed snapshot surfaces real content changes (renamed flags, new commands)
rather than markup churn.

Usage:
  python3 audit/snapshot.py [output_path]   # writes file, else prints to stdout
"""
import re
import sys
import html
import urllib.request

URL = "https://docs.unity.com/en-us/unity-cli/unity-cli-reference"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "unity-headless-cli docs-audit/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", "replace")


def normalize(doc: str) -> str:
    # drop comments
    doc = re.sub(r"<!--.*?-->", " ", doc, flags=re.S)
    # drop volatile / non-content blocks entirely
    for tag in ("script", "style", "svg", "noscript", "head", "nav", "footer", "header"):
        doc = re.sub(rf"<{tag}\b[^>]*>.*?</{tag}>", " ", doc, flags=re.S | re.I)
    # turn block-level boundaries into newlines so lines stay meaningful
    doc = re.sub(r"(?i)<(br|/p|/li|/h[1-6]|/tr|/div|/section)\b[^>]*>", "\n", doc)
    # strip all remaining tags
    doc = re.sub(r"<[^>]+>", " ", doc)
    doc = html.unescape(doc)
    # collapse whitespace per line, drop empties
    lines = []
    for raw in doc.splitlines():
        line = re.sub(r"[ \t ]+", " ", raw).strip()
        if line and not re.match(r"(?i)^(last updated .*ago|read time .*)$", line):
            lines.append(line)
    return "\n".join(lines) + "\n"


def main() -> int:
    text = normalize(fetch(URL))
    header = f"# Snapshot of {URL}\n# Normalized text only; regenerate with audit/snapshot.py\n\n"
    out = header + text
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
