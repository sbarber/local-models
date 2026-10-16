#!/usr/bin/env python3
"""Build the report from report.md; verify tables, STATE, citations and ranks.

Usage: python3 scripts/report.py --check   # read-only; fails on stale/inconsistent output
       python3 scripts/report.py --build   # update STATE and regenerate HTML
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

import ranking
from change_detection import content_hash

ROOT = Path(__file__).resolve().parent.parent
STATE = re.compile(r"<!-- STATE[^\n]*\n.*?\nEND STATE -->", re.S)
SOURCES = re.compile(r'<li id="ref-(\d+)">')
CITATIONS = re.compile(r"\[\\\[(\d+)\\\]\]\(#ref-(\d+)\)")
TIER = re.compile(r"(?m)^### .*\{#(tier-[\w-]+)\}\n")
ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*(GS|TB) ([\d.]+)(.*?)\|\s*([^|]+)\|", re.M)


NAMED_CITATION = re.compile(r"\[\\\[(@?\w+)\\\]\]\(#ref-(@?\w+)\)")
NAMED_SOURCE = re.compile(r'<li id="ref-(@?\w+)">.*?</li>', re.S)


def renumber(source):
    """Number sources by first citation; new ones may use ref-@name placeholders."""
    split = "## Sources {#sources}"
    body, refs = source.split(split, 1)
    items = {m.group(1): m.group(0) for m in NAMED_SOURCE.finditer(refs)}
    order = []
    for label, target in NAMED_CITATION.findall(body):
        if label != target:
            raise ValueError(f"Citation label {label} links to ref-{target}")
        if target not in items:
            raise ValueError(f"Citation {target} has no source")
        if target not in order:
            order.append(target)
    unused = [key for key in items if key not in order]
    if unused:
        raise ValueError(f"Uncited sources: {unused}")
    number = {key: str(i) for i, key in enumerate(order, 1)}
    body = NAMED_CITATION.sub(lambda m: f"[\\[{number[m.group(1)]}\\]](#ref-{number[m.group(2)]})", body)
    start, end = refs.index('<ol class="refs">'), refs.index("</ol>") + len("</ol>")
    listing = '<ol class="refs">\n' + "\n".join(
        items[key].replace(f'id="ref-{key}"', f'id="ref-{number[key]}"', 1) for key in order
    ) + "\n</ol>"
    return body + split + refs[:start] + listing + refs[end:]


def tables(source):
    """Read rank/score/speed rows from the human-authored Markdown tables."""
    sections = {}
    for heading in TIER.finditer(source):
        end = source.find("\n---", heading.end())
        text = source[heading.end():end if end >= 0 else len(source)]
        sections[heading.group(1)] = {}
        for use, title in (("general", "**General use**"), ("coding", "**Agentic coding**")):
            if title not in text:
                raise ValueError(f"Missing {use} table in {heading.group(1)}")
            table = text.split(title, 1)[1].split("\n\n", 2)[1]
            sections[heading.group(1)][use] = [
                (int(n), tag, kind, float(score), "vendor" in rest, "⚠" in rest, speed.strip())
                for n, tag, kind, score, rest, speed in ROW.findall(table)
            ]
    return sections


def validate(source):
    match = STATE.search(source)
    if match is None or not source.rstrip().endswith(match.group(0)):
        raise ValueError("The STATE comment must appear at the end of report.md")
    refs = [int(n) for n in SOURCES.findall(source)]
    if refs != list(range(1, len(refs) + 1)):
        raise ValueError("Sources must be consecutively numbered from 1")
    body = source[:source.index('## Sources {#sources}')]
    seen = []
    for label, target in CITATIONS.findall(body):
        if label != target or int(label) not in refs:
            raise ValueError(f"Broken citation [{label}](#ref-{target})")
        if int(target) not in seen:
            seen.append(int(target))
    if seen != refs:
        raise ValueError("Sources must appear in citation order and all be cited")

    fleet, candidates = ranking.load_data()
    headings = tables(body)
    if len(headings) != len(fleet["tiers"]):
        raise ValueError("Number of tier headings differs from machines.yaml")
    lines = []
    for tier in fleet["tiers"]:
        section = next((section for key, section in headings.items() if key.endswith(tier_id(tier))), None)
        if section is None:
            raise ValueError(f"Missing tier heading for {tier}")
        for use in ("general", "coding"):
            expected = ranking.rank(fleet, candidates, tier, use)
            actual = section[use]
            if len(actual) != len(expected):
                raise ValueError(f"{tier} {use}: expected {len(expected)} picks, found {len(actual)}")
            for i, (row, pick) in enumerate(zip(actual, expected), 1):
                n, tag, kind, score, vendor, flag, display_speed = row
                if (n, tag, kind, score, vendor, flag, display_speed) != (
                    i, pick["tag"], "GS" if use == "general" else "TB", pick["score"],
                    pick["vendor"], pick["flag"], ranking.formatted_speed(pick)
                ):
                    raise ValueError(f"{tier} {use} #{i}: table differs from ranking; got {row}, expected {pick}")
                suffix = (" vendor" if vendor else "") + (" flag" if flag else "")
                lines.append(f"{tier} | {use} | {i} | {tag} | {kind} {score:.1f}{suffix}")
    prefix, existing = match.group(0).split("[picks]\n", 1)
    for label, path in (("fleet_sha256", "machines.yaml"), ("candidates_sha256", "candidates.json")):
        entry = f"{label}: {content_hash(ROOT / path)}"
        if re.search(rf"(?m)^{label}: .*?$", prefix):
            prefix = re.sub(rf"(?m)^{label}: .*?$", entry, prefix)
        else:
            prefix += entry + "\n"
    state = prefix + "[picks]\n" + "\n".join(lines) + "\nEND STATE -->"
    if "--" in state[4:-4]:
        raise ValueError("STATE cannot contain -- inside the HTML comment")
    return source[:match.start()] + state + source[match.end():]


def tier_id(tier):
    # Explicit names are human-readable; the id-to-tier mapping lives here, not in report.md.
    return {
        "Mac M1 8 GB": "mac-m1-8", "Mac 8 GB": "mac-8",
        "Mac M1 16 GB": "mac-m1-16", "Mac 16-24 GB": "mac-16-24",
        "Mac 32-36 GB": "mac-32-36", "Mac 48-96 GB": "mac-48-96",
        "Mac 128 GB": "mac-128", "Latitude 7350": "latitude",
        "Windows 32 GB": "win-32", "Pro Max 16 Plus, 8-16 GB GPU": "pm16p-8-16",
        "Pro Max 16 Plus, 24 GB GPU": "pm16p-24",
    }[tier]


def render(source):
    return subprocess.run(
        ["pandoc", "-f", "gfm+attributes", "-t", "html5", "-s", "--metadata",
         "pagetitle=Local Models Report", "-H", str(ROOT / "scripts/report-style.html")],
        input=source, text=True, capture_output=True, check=True,
    ).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--build", action="store_true")
    args = parser.parse_args()
    path = ROOT / "report.md"
    source = path.read_text()
    corrected = validate(renumber(source))
    rendered = render(corrected)
    output = ROOT / "local-models-report.html"
    if args.check:
        if source != corrected:
            raise ValueError("STATE does not match tables; run --build")
        if not output.exists() or output.read_text() != rendered:
            raise ValueError("HTML differs from report.md; run --build")
        print("Report, rankings, STATE and citations match")
    else:
        path.write_text(corrected)
        output.write_text(rendered)
        print(f"Built {output}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, subprocess.CalledProcessError) as exc:
        sys.exit(str(exc))
