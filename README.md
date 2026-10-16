# Local models report

**[Read the current report](https://sbarber.github.io/local-models/)** — picks for
OpenCode + Ollama on the MacBook Pro and Dell laptop tiers in this fleet. The
report distinguishes General use from Agentic coding, explains its ranking
rules, and cites the underlying sources. Speeds are *estimates*, not benchmarks
measured on these machines. Coding scores marked **(vendor)** were supplied by
the model vendor; **⚠** marks an unresolved tool-call report.

## Refresh and publish

The [Refresh runbook](.opencode/skills/refresh-local-models/SKILL.md) describes
the research and independent audit. A Refresh requires human/agent review of
sources; it is deliberately **not** an unattended model-selection job.

Prerequisites: Python 3.14 (or a compatible recent Python 3), PyYAML, and
[pandoc 3.10.1](https://github.com/jgm/pandoc/releases/tag/3.10.1) to reproduce
the checked-in HTML. Never pull or run models to build the report.

```sh
python3 -m pip install -r requirements.txt
scripts/check-changes.sh                 # 0: no change, 10: refresh recommended, 1: incomplete/error
python3 scripts/aa.py fetch              # update the ignored AA cache when researching scores
# After checking upstream sources, update machines.yaml and candidates.json.
python3 scripts/ranking.py               # deterministic picks from the dated snapshot
# Edit report.md: tables, prose, sources and source versions; keep the previous STATE for the Diff.
python3 scripts/report.py --build         # generate STATE and local-models-report.html
python3 -m unittest discover -s tests -v
python3 scripts/report.py --check
scripts/verify_facts.py                  # live sources: tag sizes, KV cache, scores, paid equivalents, issues (~2 min)
# Then one audit of the changes (git diff origin/main), per the runbook.
```

`report.md` is the editable source; `local-models-report.html` is the generated
site. `candidates.json` is a dated snapshot of source-based scores, tag sizes,
KV-cache estimates and bug flags. **It does not update itself.** When the Change
check reports a new score, refresh the snapshot and review the rankings before
changing the report. The checked-in AA fixture is test data; `.cache/` is local
and ignored. This separation makes `--check` and the unit tests work offline.

After the research and audit, push to `main`. The
[report workflow](.github/workflows/report.yml) runs tests, builds the Pages
artifact (only the HTML, redirect, and `.nojekyll`), deploys it when tests pass,
and checks the live page. Pull requests run checks without deploying. A daily
[site check](.github/workflows/site-health.yml) catches an unavailable page.
The repository is public; access to GitHub Actions is needed for publishing.

## Public data review

This repository is public. **The HTML page is not the only public data**:
`machines.yaml` names the fleet and configurations; `candidates.json` records
research decisions; the runbook describes the ranking and review procedure;
`report.md` and the HTML contain public links and an HTML-comment STATE with
source versions, watched issue numbers and picks. The site artifact itself
contains only the report and redirect, but the full repository and its Git
history remain public.

No credentials are needed to build the report; `.cache/` and `__pycache__/` are
excluded. **Before adding machines or notes, check whether the details are
approved for public sharing.** If the fleet or process must be private, decide
with its owner what can be published, then move the working source to a private
repository and publish a reviewed, sanitized report separately. Removing a
file from a later commit does not remove it from Git history.
