#!/usr/bin/env python3
"""List Ollama library models with their capability badges (tools, thinking, vision, cloud, ...).

Usage:
  scripts/ollama_library.py                 # all models: name, badges, sizes, updated
  scripts/ollama_library.py --tools         # only models with the `tools` badge
  scripts/ollama_library.py --json          # JSON (used by check-changes.sh)
  scripts/ollama_library.py tags <model>    # tag list with size + context for one model

Source: https://ollama.com/library?sort=popular (whole library on one page).
"""
import html
import json
import re
import sys
import urllib.request


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "ignore")


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def library():
    page = get("https://ollama.com/library?sort=popular")
    out = []
    for block in re.findall(r"<li\b.*?</li>", page, flags=re.S):
        m = re.search(r'href="/library/([^"/?#]+)"', block)
        if not m:
            continue
        badges = [text(b) for b in re.findall(
            r'<span[^>]*class="[^"]*rounded-md[^"]*px-2[^"]*"[^>]*>(.*?)</span>', block, flags=re.S)]
        caps = sorted({b for b in badges if not re.match(r"^[\d.]+[a-zA-Z]*$|^e\d+b$", b)})
        sizes = [b for b in badges if b not in caps]
        upd = re.search(r'<span[^>]*title="([^"]+UTC)"', block)
        out.append({"name": m.group(1), "capabilities": caps, "sizes": sizes,
                    "updated": upd.group(1) if upd else None})
    if not out:
        sys.exit("Ollama library page format changed: no models parsed. Update scripts/ollama_library.py.")
    return out


def tags(model):
    page = get(f"https://ollama.com/library/{model}/tags")
    t = text(re.sub(r"<script.*?</script>", "", page, flags=re.S))
    rows = re.findall(re.escape(model) + r":([\w.\-]+) [0-9a-f]{12} • ([\d.]+\s?[GMT]B) • (\S+) context window", t)
    seen, out = set(), []
    for tag, size, ctx in rows:
        if tag not in seen:
            seen.add(tag)
            out.append((tag, size.replace(" ", ""), ctx))
    names = sorted(set(re.findall(r"/library/" + re.escape(model) + r":([\w.\-]+)", page)))
    for n in names:
        if n not in seen:
            out.append((n, "?", "?"))
    return out


def main():
    args = sys.argv[1:]
    if args[:1] == ["tags"]:
        for tag, size, ctx in tags(args[1]):
            print(f"{args[1]}:{tag:40} {size:>7} {ctx}")
        return
    models = library()
    if "--tools" in args:
        models = [m for m in models if "tools" in m["capabilities"]]
    if "--json" in args:
        print(json.dumps(models))
        return
    for m in models:
        print(f'{m["name"]:32} {",".join(m["capabilities"]):32} {" ".join(m["sizes"]):30} {m["updated"] or ""}')


if __name__ == "__main__":
    main()
