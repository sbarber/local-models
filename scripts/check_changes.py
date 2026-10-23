#!/usr/bin/env python3
"""Compare live sources with the report STATE; exit 10 when a Refresh is due."""
import json, os, re, subprocess, sys, urllib.request
from pathlib import Path

from change_detection import content_hash, score_changes, updated_models

REPORT = "local-models-report.html"
if not os.path.exists(REPORT):
    print("CHANGED: no report yet\nREFRESH RECOMMENDED"); sys.exit(10)
report = open(REPORT).read()

# State lives in a hidden HTML comment at the end of the report:
#   <!-- STATE ...  refreshed: / [source versions] key: value / [picks] a | b | c  ... END STATE -->
m = re.search(r"<!-- STATE[^\n]*\n(.*?)\nEND STATE -->", report, flags=re.S)
if not m:
    sys.exit("Report has no <!-- STATE ... END STATE --> block; run a full Refresh.")
section, state, picks, refreshed = None, {}, [], None
for line in m.group(1).splitlines():
    line = line.strip()
    if line.startswith("[") and line.endswith("]"):
        section = line[1:-1]
    elif line.startswith("refreshed:"):
        refreshed = line.split(":", 1)[1].strip()
    elif section == "source versions" and ":" in line:
        k, v = line.split(":", 1); state[k.strip()] = v.strip()
    elif section == "picks" and line:
        picks.append([c.strip() for c in line.split("|")])

def get(url, accept="application/json"):
    headers = {"User-Agent": "Mozilla/5.0", "Accept": accept}
    if url.startswith("https://api.github.com/") and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"  # avoids the anonymous rate limit
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "ignore")

reasons, skipped = [], []

def check(name, fn):
    try:
        fn()
    except Exception as e:  # a broken source must not hide the others
        skipped.append(f"{name}: {e.__class__.__name__}: {e}")

# 1. Stack: latest stable GitHub releases
def stack():
    # OpenCode 2.x ships as the npm package @opencode/cli and isn't published as GitHub
    # releases; the user declared it the stable line on 2026-10-05.
    # Ollama: latest non-prerelease GitHub release.
    oc = "v" + json.loads(get("https://registry.npmjs.org/@opencode%2fcli/latest"))["version"]
    ol = json.loads(get("https://api.github.com/repos/ollama/ollama/releases/latest"))["tag_name"]
    for key, name, tag in (("opencode_stable", "@opencode/cli (npm latest)", oc), ("ollama_stable", "ollama/ollama", ol)):
        if tag != state.get(key):
            major = " (MAJOR VERSION: rewrite config section)" if tag.lstrip("v").split(".")[0] != state.get(key, "v0").lstrip("v").split(".")[0] else ""
            reasons.append(f"{name} stable {state.get(key)} -> {tag}{major}")
check("Stack versions", stack)

# 2. Artificial Analysis: index version, scores of all snapshot candidates,
#    and coding-column coverage (including models omitted from today's picks).
def aa():
    fp = json.loads(subprocess.check_output([sys.executable, "scripts/aa.py", "fingerprint"]))
    if fp["aa_index_version"] != state.get("aa_index_version"):
        reasons.append(f"AA Intelligence Index {state.get('aa_index_version')} -> {fp['aa_index_version']}")
    col = state.get("aa_coding_column", "terminalBench21")
    models = json.load(open(".cache/aa_models.json"))
    candidates = json.load(open("candidates.json"))["models"]
    reasons.extend(score_changes(models, candidates))
    open_models = [m for m in models if m.get("isOpenWeights") and not m.get("deprecated")]
    covered = sum(1 for m in open_models if m.get(col) is not None)
    if covered < 50:
        reasons.append(f"AA coding column '{col}' now covers only {covered} current open models; choose another column")
check("Artificial Analysis", aa)

# 3. Ollama library: even models without the tools badge can support tools.
def library():
    lib = json.loads(subprocess.check_output([sys.executable, "scripts/ollama_library.py", "--json"]))
    fresh = updated_models(lib, refreshed)
    if fresh:
        reasons.append("Ollama library models added/updated since " + refreshed + ": " + ", ".join(fresh))
check("Ollama library", library)

# 4. LMArena publish date
def arena():
    d = json.loads(get("https://datasets-server.huggingface.co/rows?dataset=lmarena-ai/leaderboard-dataset&config=text_style_control&split=latest&offset=0&length=1"))
    date = d["rows"][0]["row"]["leaderboard_publish_date"]
    if date != state.get("lmarena_publish_date"):
        reasons.append(f"LMArena leaderboard {state.get('lmarena_publish_date')} -> {date}")
check("LMArena", arena)

# 5. Watched Ollama issues
def issues():
    for n in state.get("open_watched_issues", "").split(","):
        n = n.strip()
        if not n:
            continue
        st = json.loads(get(f"https://api.github.com/repos/ollama/ollama/issues/{n}"))["state"]
        if st != "open":
            reasons.append(f"ollama/ollama#{n} is now {st}")
check("Watched issues", issues)

# 6. Hardware: Apple MacBook Pro list
def apple():
    page = get("https://support.apple.com/en-us/docs/mac", accept="text/html")  # JSON Accept returns 404
    names = re.findall(r">\s*(MacBook Pro \([^<]{3,60}\))\s*<", page)
    if not names:
        raise RuntimeError("no MacBook Pro entries parsed")
    if names[0] != state.get("macbook_pro_newest"):
        reasons.append(f"Apple: newest MacBook Pro is now '{names[0]}' (was '{state.get('macbook_pro_newest')}')")
check("Apple", apple)

# Dell blocks scripted requests (HTTP 403); the Refresh checks Dell via webfetch (Runbook step 4).
skipped.append("Dell: blocked for scripts (HTTP 403); checked by the agent during a Refresh")

# 7. Snapshot inputs: content hashes survive clones, touch and same-day edits.
for label, filename in (("fleet_sha256", "machines.yaml"), ("candidates_sha256", "candidates.json")):
    if state.get(label) != content_hash(Path(filename)):
        reasons.append(f"{filename} changed since the last Refresh")

for r in reasons:
    print("CHANGED:", r)
for s in skipped:
    print("SKIPPED:", s)
if reasons:
    print("REFRESH RECOMMENDED"); sys.exit(10)
if len(skipped) > 1:
    print("CHECK INCOMPLETE"); sys.exit(1)
print("NO CHANGES"); sys.exit(0)
