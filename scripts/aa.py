#!/usr/bin/env python3
"""Scrape the Artificial Analysis (AA) leaderboard and match local models to paid ones.

No API key: the model table is embedded in the page's Next.js RSC payload.

Usage:
  scripts/aa.py fetch                      # download + cache to .cache/aa_models.json, print summary
  scripts/aa.py show "Qwen3.8 27B" ...     # print scores for models whose name contains each string
  scripts/aa.py nearest "Qwen3.8 27B (Medium)"   # nearest paid models on TB 2.1 and General score
  scripts/aa.py fingerprint                # stable summary used by check-changes.sh

Scores are printed as AA shows them (0-100). "E" = intelligence index estimated by AA.
GS = General score: weighted mean of HLE, CritPt, an Omniscience penalty score and
AA-LCR (see GS_WEIGHTS); blank when any input is missing.
"""
import json
import os
import re
import sys
import urllib.request

URL = "https://artificialanalysis.ai/leaderboards/models"
METHODOLOGY = "https://artificialanalysis.ai/methodology/intelligence-benchmarking"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache", "aa_models.json")
PAID_CREATORS = {"OpenAI", "Anthropic", "Google", "SpaceXAI", "xAI"}


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "ignore")


def _rsc(url):
    html = _get(url)
    chunks = re.findall(r'self\.__next_f\.push\(\[1,(".*?")\]\)</script>', html, flags=re.S)
    if not chunks:
        sys.exit(f"AA page format changed: no self.__next_f chunks found in {url}. Update scripts/aa.py.")
    return "".join(json.loads(c) for c in chunks)


def _scored_array(txt, key, url):
    i = txt.find(f'"{key}":[{{')
    if i < 0:
        sys.exit(f'AA page format changed: no "{key}":[ array in {url}. Update scripts/aa.py.')
    arr, _ = json.JSONDecoder().raw_decode(txt[i + len(key) + 3:])
    arr = [m for m in arr if isinstance(m, dict)]  # a model page refers to itself by "$" reference
    if not (arr and "intelligenceIndex" in arr[0] and "terminalBench21" in arr[0]):
        sys.exit(f'AA page format changed: "{key}" array in {url} has no score fields. Update scripts/aa.py.')
    return arr


def fetch():
    # Since October 2026 the leaderboard embeds only current models ("initialModels").
    # Deprecated models are still scored on every model page's "models" array, which
    # names the creator in a "creator" object instead of "modelCreatorName".
    models = _scored_array(_rsc(URL), "initialModels", URL)
    page = f"https://artificialanalysis.ai/models/{models[0]['slug']}"
    known = {m["name"] for m in models}
    for m in _scored_array(_rsc(page), "models", page):
        if m["name"] in known:
            continue
        m.setdefault("modelCreatorName", (m.get("creator") or {}).get("name"))
        models.append(m)
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w") as f:
        json.dump(models, f)
    return models


def load():
    if os.path.exists(CACHE):
        with open(CACHE) as f:
            return json.load(f)
    return fetch()


def pct(x):
    return None if x is None else round(x * 100, 1)


# General score (GS): the Intelligence Index's non-agentic, non-coding evals (GDP.pdf is not
# in AA's leaderboard data), with two changes from the Index's weights:
# - Omniscience uses a penalty score instead of accuracy + non-hallucination. Non-hallucination
#   ignores correct answers, so a model that abstains on everything scores 100%. The penalty
#   score gives +1 per correct answer, 0 per abstention and -OMNI_PENALTY per wrong answer
#   (the -0.5 the AA-Omniscience paper suggests, arXiv 2511.13029 section 5), rescaled to 0-1.
# - CritPt weight 10 -> 5: small models score near 0 on its 70 problems, so it mostly adds noise.
OMNI_PENALTY = 0.5
GS_WEIGHTS = {"hle": 10, "critpt": 5, "omniPenalty": 15, "lcr": 5}


def omni_penalty(m):
    """Omniscience penalty score, 0-1. Wrong-answer share = accuracy - Omniscience Index/100."""
    c, oi = m.get("omniscienceAccuracy"), m.get("omniscience")
    if not isinstance(c, (int, float)) or not isinstance(oi, (int, float)):
        return None
    wrong = c - oi / 100
    return (c - OMNI_PENALTY * wrong + OMNI_PENALTY) / (1 + OMNI_PENALTY)


def general_score(m):
    vals = {k: (omni_penalty(m) if k == "omniPenalty" else m.get(k)) for k in GS_WEIGHTS}
    if any(not isinstance(v, (int, float)) for v in vals.values()):
        return None
    return round(100 * sum(vals[k] * w for k, w in GS_WEIGHTS.items()) / sum(GS_WEIGHTS.values()), 1)


def row(m):
    ii = m.get("intelligenceIndex")
    return {
        "name": m["name"],
        "creator": m.get("modelCreatorName"),
        "open": m.get("isOpenWeights"),
        "deprecated": m.get("deprecated"),
        "gs": general_score(m),
        "ii": None if ii is None else round(ii, 1),
        "ii_est": m.get("intelligenceIndexIsEstimated"),
        "tb21": pct(m.get("terminalBench21")),
        "tbh": pct(m.get("terminalbenchHard")),
        "gpqa": pct(m.get("gpqa")),
        "price": (m.get("price1mInputTokens"), m.get("price1mOutputTokens")),
    }


def fmt(r):
    def score(value):
        return "" if value is None else value

    ii = "" if r["ii"] is None else f'{r["ii"]}{"E" if r["ii_est"] else ""}'
    p = r["price"]
    price = "" if p[0] is None else f"${p[0]:g}/{p[1]:g}"
    dep = " (deprecated)" if r["deprecated"] else ""
    return (f'{r["name"][:52]:52} GS={score(r["gs"]):5} II={ii:6} TB2.1={score(r["tb21"]):5} '
            f'TBH={score(r["tbh"]):5} GPQA={score(r["gpqa"]):5} {price}{dep}')


def nearest_paid(models, key, score):
    """Paid models ordered as Equivalent paid models for a score ("gs" or "tb21")."""
    paid = [row(m) for m in models
            if not m.get("isOpenWeights") and m.get("modelCreatorName") in PAID_CREATORS]
    candidates = [p for p in paid if p[key] is not None]

    # Within 3 points: prefer current over deprecated, then closest.
    # Beyond 3 points: closest wins outright.
    def rank(p):
        d = abs(p[key] - score)
        if d <= 3:
            return (0, bool(p["deprecated"]), d)
        return (1, False, d)

    return sorted(candidates, key=rank)


def nearest(models, name, n=3):
    target = [row(m) for m in models if m["name"].lower() == name.lower()]
    if not target:
        sys.exit(f"No exact AA name match for {name!r}. Use `show` to find the exact name.")
    t = target[0]
    print(fmt(t))
    for key, label in (("tb21", "Agentic coding: Terminal-Bench 2.1"),
                       ("gs", "General use: General score")):
        if t[key] is None:
            print(f"  {label}: no score for this model")
            continue
        print(f"  {label} = {t[key]}; nearest paid:")
        for p in nearest_paid(models, key, t[key])[:n]:
            print("    " + fmt(p))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "fetch"
    if cmd == "fetch":
        models = fetch()
        print(f"{len(models)} models cached to {CACHE}")
    elif cmd == "show":
        models = load()
        for q in sys.argv[2:]:
            for m in models:
                if q.lower() in m["name"].lower():
                    print(fmt(row(m)))
    elif cmd == "nearest":
        models = load()
        for q in sys.argv[2:]:
            nearest(models, q)
    elif cmd == "fingerprint":
        models = fetch()
        method = _get(METHODOLOGY)
        v = re.search(r"(?:Intelligence Index|Version)[^0-9v]{0,40}v?(\d+\.\d+(?:\.\d+)?)", method)
        open_top = sorted((row(m) for m in models if m.get("isOpenWeights") and m.get("intelligenceIndex")),
                          key=lambda r: -r["ii"])[:15]
        print(json.dumps({
            "aa_index_version": v.group(1) if v else "unknown",
            "aa_model_count": len(models),
            "aa_open_names": sorted(r["name"] for r in (row(m) for m in models if m.get("isOpenWeights"))),
            "aa_top_open": [r["name"] for r in open_top],
        }))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
