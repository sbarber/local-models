#!/usr/bin/env python3
"""Check report facts against live sources, so the audit only covers what scripts can't.

Checks: picked tags exist and their sizes match the snapshot (tags page for GGUF,
registry manifest for MLX); 64k KV-cache sizes match each GGUF header; AA scores
match the snapshot; every Equivalent paid model matches the nearest-paid rule;
every linked Ollama issue's state matches what the report says about it.

Usage: scripts/verify_facts.py [--fetch]   # --fetch refreshes the AA cache first
Exit code: 0 = all checks pass, 1 = mismatches or a source could not be read.
"""
import argparse
import concurrent.futures
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import aa
import gguf_kv
import ollama_library
from change_detection import score_changes

ROOT = Path(__file__).resolve().parent.parent
ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*(GS|TB) ([\d.]+)[^|]*\|[^|]+\|\s*([^|]+?)\s*\|\s*$", re.M)
ISSUE = re.compile(r"github\.com/ollama/ollama/issues/(\d+)")
WATCHED = re.compile(r"(?m)^open_watched_issues:\s*(.*)$")


def table_rows(source):
    """(tag, kind, score, equivalent) for every row of the tier tables."""
    body = source.split("## Model reference", 1)[0]
    return [(tag, kind, float(score), equivalent) for _, tag, kind, score, equivalent in ROW.findall(body)]


def size_gb(text):
    """Tags-page size such as '17GB' or '366MB' in GB."""
    number, unit = re.fullmatch(r"([\d.]+)\s*([GMT]B)", text).groups()
    return float(number) * {"MB": 0.001, "GB": 1, "TB": 1000}[unit]


def equivalent_name(text):
    return re.sub(r",\s*low confidence$", "", text.strip()).lower()


def check_equivalents(rows, models):
    problems = []
    for tag, kind, score, equivalent in rows:
        key = "gs" if kind == "GS" else "tb21"
        expected = aa.nearest_paid(models, key, score)[0]["name"]
        if equivalent_name(equivalent) != expected.lower():
            problems.append(f"{tag} {kind} {score}: report says '{equivalent}', nearest paid is '{expected}'")
    return problems


def issue_line_problems(source, states):
    """A closed issue must be described as closed or fixed on its line; an open one mustn't."""
    problems = []
    watched = WATCHED.search(source)
    for number in (watched.group(1).split(",") if watched else []):
        number = number.strip()
        if number and states.get(number) != "open":
            problems.append(f"#{number} is in open_watched_issues but is {states.get(number)}")
    visible = source.split("<!-- STATE", 1)[0]
    for line in visible.splitlines():
        for number in set(ISSUE.findall(line)):
            closed_words = re.search(r"\b(closed|fixed)\b", line, re.I)
            if states.get(number) == "closed" and not closed_words:
                problems.append(f"#{number} is closed, but its line doesn't say so: {line[:100]}")
    return problems


def github_token():
    try:
        return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def issue_state(number, token):
    request = urllib.request.Request(f"https://api.github.com/repos/ollama/ollama/issues/{number}",
                                     headers={"Accept": "application/vnd.github+json",
                                              **({"Authorization": f"Bearer {token}"} if token else {})})
    with urllib.request.urlopen(request, timeout=60) as response:
        return number, json.loads(response.read())["state"]


def manifest_size_gb(tag):
    _, data = gguf_kv.manifest(tag)
    return round(sum(layer["size"] for layer in data["layers"]) / 1e9, 1)


def check_tags(rows, candidates, pool):
    snapshot = {tag: info for model in candidates for tag, info in model["tags"].items()}
    tags = sorted({tag for tag, *_ in rows})
    problems = [f"{tag}: not in candidates.json" for tag in tags if tag not in snapshot]
    tags = [tag for tag in tags if tag in snapshot]
    gguf_models = sorted({tag.split(":")[0] for tag in tags if snapshot[tag]["format"] == "gguf"})
    pages = dict(zip(gguf_models, pool.map(ollama_library.tags, gguf_models)))
    mlx = [tag for tag in tags if snapshot[tag]["format"] == "mlx"]
    mlx_sizes = dict(zip(mlx, pool.map(manifest_size_gb, mlx)))
    for tag in tags:
        info = snapshot[tag]
        model, name = tag.split(":")
        if info["format"] == "mlx":
            live = mlx_sizes[tag]
            if live != round(info["size_gb"], 1):
                problems.append(f"{tag}: manifest size {live} GB, snapshot {info['size_gb']} GB")
            continue
        listed = {row[0]: row[1] for row in pages[model]}
        if name not in listed:
            problems.append(f"{tag}: not on the tags page")
        elif listed[name] == "?":
            problems.append(f"{tag}: the tags page shows no size")
        elif abs(size_gb(listed[name]) - info["size_gb"]) > 0.0005:
            problems.append(f"{tag}: tags page says {listed[name]}, snapshot {info['size_gb']} GB")
    return problems


def check_kv(candidates, pool):
    tags = {}
    for model in candidates:
        gguf = [tag for tag, info in model["tags"].items() if info["format"] == "gguf"]
        if gguf:
            tags[gguf[0]] = model
    results = dict(zip(tags, pool.map(lambda tag: gguf_kv.kv_gb(gguf_kv.header(tag)), tags)))
    problems = []
    for tag, model in tags.items():
        for name, info in model["tags"].items():
            if abs(info["kv64k_gb"] - results[tag]) > 0.02:
                problems.append(f"{name}: 64k KV {info['kv64k_gb']} GB in snapshot, header gives {results[tag]:.2f} GB")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="refresh the AA cache before checking")
    args = parser.parse_args()
    source = (ROOT / "report.md").read_text()
    candidates = json.loads((ROOT / "candidates.json").read_text())["models"]
    models = aa.fetch() if args.fetch else aa.load()
    rows = table_rows(source)
    token = github_token()
    results = {}
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        checks = {
            "Tags and sizes": lambda: check_tags(rows, candidates, pool),
            "KV cache at 64k": lambda: check_kv(candidates, pool),
            "AA scores": lambda: score_changes(models, candidates),
            "Equivalent paid models": lambda: check_equivalents(rows, models),
            "Issue states": lambda: issue_line_problems(
                source, dict(pool.map(lambda n: issue_state(n, token), sorted(set(ISSUE.findall(source)))))),
        }
        for name, check in checks.items():
            try:
                results[name] = check()
            except Exception as exc:  # a source that can't be read is a failed check, not a pass
                results[name] = [f"could not check: {exc.__class__.__name__}: {exc}"]
    failed = False
    for name, problems in results.items():
        print(f"{'FAIL' if problems else 'OK  '} {name}")
        for problem in problems:
            print(f"     - {problem}")
        failed = failed or bool(problems)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
