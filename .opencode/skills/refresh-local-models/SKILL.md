---
name: refresh-local-models
description: Runbook for a Refresh of local-models-report.html, the Top local models per Hardware tier for OpenCode + Ollama. Use when the user asks to refresh/update/rerun the local models report, run the Change check, or add machines to the fleet.
---

# Refresh local models

Vocabulary: read `GLOSSARY.md` first (Machine, Hardware tier, Use case, Top model, Equivalent paid model, Stack, Report, Refresh, Diff, Change check, Estimated speed). Files: `machines.yaml` (fleet), `local-models-report.html` (the Report), `scripts/report-style.html` (its CSS), `scripts/`.

Facts come from primary sources with a URL; anything else is marked "unsourced" or "estimate". Never run or pull models: there are no smoke tests.

## Steps

1. **Change check.** Run `scripts/check-changes.sh`. If it prints `NO CHANGES` and the user did not ask to force a Refresh, tell the user and stop. Otherwise carry its list of reasons into the Diff.
   Done when: you have the list of reasons, or have stopped.

2. **Capture the previous state.** Read the hidden `<!-- STATE ... END STATE -->` block at the end of the current Report (refreshed date, source versions, picks) and keep it verbatim in context. It is the only record of the previous Refresh; the file is overwritten in step 10.
   Done when: the STATE block is in context.

3. **Stack.** Never count betas or release candidates.
   - OpenCode: the **2.x** line (`@opencode/cli`), declared stable by the user on 2026-10-05 even though GitHub still marks 1.x as "latest release". Version = `https://registry.npmjs.org/@opencode%2fcli/latest`. Config docs: `https://opencode.ai/v2/docs` (providers, models, config, compaction, agents, mcp-servers). If OpenCode later moves 2.x to GitHub releases or ships 3.x, ask the user which line counts before switching.
   - Ollama: GitHub "latest release", `https://api.github.com/repos/ollama/ollama/releases/latest`.
   Read the release notes since the previous versions for: context-length defaults, env vars, MLX/Vulkan changes, OpenCode provider/config changes. On a major-version change, rewrite the OpenCode config section from that version's docs.
   Done when: both versions recorded and every relevant release-note change listed.

4. **Fleet.** Apply each rule in `machines.yaml`:
   - Apple: open `https://support.apple.com/en-us/docs/mac`; for every MacBook Pro entry newer than those in `machines`, open its Tech Specs page and read Chip (GPU cores, memory bandwidth) and Memory (options). Add rows (`auto_add_new: true`).
   - Dell: for each `product_codes` and `next_generation_probe`, fetch `https://www.dell.com/support/product-details/en-us/product/<code>/overview` (an invalid code redirects to `IsInvalidSelection=True`). A new generation gets a row flagged `new: confirm in fleet`. Specs: owner's manual / setup-and-specifications PDF (dl.dell.com) or spec sheet PDF (delltechnologies.com); read Processor, Memory, GPU/Video Card.
   - NVIDIA laptop GPU bandwidth: `https://www.nvidia.com/en-us/products/workstations/professional-laptops/compare/`.
   - Place every new row in a tier per `tier_rules` in `machines.yaml`: Macs by memory, Windows by GPU/RAM class. A Machine whose bandwidth is far below the rest of its tier (like the base M1, ~67 GB/s vs 100+) gets its own tier, so it doesn't drag the tier's "one fast pick" down.
   Done when: every rule checked and every row in `machines` has a tier and a `source` URL.

5. **Candidates.** `scripts/ollama_library.py --tools` lists models with the `tools` badge. Keep: every model in the previous Picks, plus every model updated in the last 12 months. Drop cloud-only models (`scripts/ollama_library.py tags <model>` shows no local sizes). Rank GGUF tags only (`q4_K_M`, `-it-qat`, or 8-bit where no 4-bit exists); `-mlx`, `-nvfp4`, `-mxfp8`, `-int4`, `-int8` are Apple-only MLX formats and appear only as optional Mac swaps. Also check every model updated in the last 12 months that lacks the badge: Ollama still reports tool support when the registry config blob has no `renderer` and the GGUF `tokenizer.chat_template` handles tools (Ollama v0.40.1 `server/images.go`, `chatTemplateHasToolSupport`). Read the template with a ranged GET of the model blob's GGUF header. Such models are candidates; decision models (`decision` capability) never are. Note the rest under "Considered and left out". Record each candidate's tags, sizes, total/active params, license, origin (Ollama page, vendor model card on Hugging Face).
   Done when: every kept candidate has sizes and params.

6. **Scores.** `scripts/aa.py fetch`, then `scripts/aa.py show "<name>"`.
   - General: General score (GS), printed as `GS=` by `scripts/aa.py show` (`general_score` in `scripts/aa.py`). It's a weighted mean of the Intelligence Index's non-agentic, non-coding evals: HLE 10, CritPt 5, Omniscience penalty score 15, AA-LCR 5 (`GS_WEIGHTS`). The penalty score is +1 correct, 0 abstain, −0.5 wrong (`OMNI_PENALTY`; wrong share = `omniscienceAccuracy − omniscience/100`), rescaled to 0-1. Don't switch back to AA's accuracy + non-hallucination split: non-hallucination ignores correct answers, so heavy refusers top the small tiers. CritPt is halved because local models score near zero on it. A model missing any input has no GS and isn't ranked for General; there is no vendor fallback for GS. Note the Index version (`scripts/aa.py fingerprint`); if AA changes the Index's eval list, re-check `GS_WEIGHTS` against https://artificialanalysis.ai/methodology/intelligence-benchmarking and say so in the Diff. When a small-tier pick wins on few wrong answers rather than many right ones, say so in the tier notes.
   - Coding: the AA Terminal-Bench column with the best coverage of both candidates and paid models (currently `terminalBench21`). If it changes, say so in the Diff.
   - Effort row: use the row matching Ollama's default behaviour: `Medium` if AA has one, else `Reasoning`/`High`, else the single row.
   - No AA score: use the vendor's model card score on the same benchmark, flagged `(vendor)`.
   Done when: every candidate has a score or is marked "no score".

7. **Bugs.** For each candidate, search open issues by model name and by its parser name (Ranking rule 3): `https://api.github.com/search/issues?q=repo:ollama/ollama+<name>+in:title+state:open`. Also re-check every issue in the Report's Watched issues table (`https://api.github.com/repos/ollama/ollama/issues/<n>`).
   Done when: every candidate and watched issue checked.

8. **Fit, speed, rank.** Put every candidate (tag, size, active/total params, AA rows, family, vendor score) and every Machine from `machines.yaml` into a throwaway script in the temp directory, and compute fit, speed and rank there with **Fit rules**, **Speed estimate** and **Ranking rules**. Ranking by hand is how the first Refresh got 31 audit errors.
   Done when: the script prints 1-5 picks per tier × use case (or none), with speed ranges.

9. **Paid equivalents and config.** `scripts/aa.py nearest "<AA name>"` per pick. Re-verify each config claim against the pages in **Config sources**.
   Done when: every pick has an equivalent and every config row has a source.

10. **Write the Report.** Overwrite `local-models-report.html` keeping its section structure. Draft it as GitHub-flavoured markdown in the temp directory, then build the page:
    `pandoc -f gfm+attributes -t html5 -s --metadata pagetitle="Local Models Report" -H scripts/report-style.html <draft>.md -o local-models-report.html`
    - Copy tags, scores and speeds from script output, and generate each tier heading's machine list from `machines.yaml` with code; never retype them from memory.
    - Tiers have no codes: a tier heading is its descriptive name plus its machines on one line (Mac tiers list chip names only, e.g. `Mac 48-96 GB: M1 Max / M4 Pro`, since the name already gives the memory). Put a `---` rule between tiers.
    - Give every section and tier heading an explicit id (`### Mac 8 GB: M2 / M3 {#tier-mac-8}`) and keep the `<nav class="toc">` block at the top linking to each of them.
    - Citations are numbered links, `[\[3\]](#ref-3)`, numbered by first appearance; the Sources section is an `<ol class="refs">` whose `<li id="ref-N">` items hold the linked URLs. Ollama issue numbers link to their GitHub issue.
    - Each tier has a General use table and an Agentic coding table. Table separator rows use explicit left alignment (`|:---|`).
    - Prose bullets state no number that isn't in a table or a cited source.
    - Reader-facing content never mentions this project's files, scripts or process (no `machines.yaml`, `scripts/`, runbook, "Refresh", "update process"); cite public source URLs instead. No Diff in the file.
    - Plumbing goes only in the hidden STATE comment at the very end, in exactly this format (no `--` inside it):
      ```
      <!-- STATE (read by the update process; not shown on the page)
      refreshed: YYYY-MM-DD
      [source versions]
      opencode_stable: vX.Y.Z
      ...
      [picks]
      <tier name> | general|coding | <rank> | <tag> | <score>
      END STATE -->
      ```
    Done when: the page is built, `scripts/check-changes.sh` parses it, and every STATE pick matches the tier tables.

11. **Verify.** Dispatch a fresh subagent (it must not see your reasoning, only the files) with the **Audit brief** below. Fix every error it reports, then re-dispatch until it returns zero errors.
    Done when: an audit pass returns zero errors.

12. **Tell the user the Diff** in chat, plus the number of errors the audit caught and fixed: Stack versions, machines added, picks added/dropped/moved per tier and use case, score changes over 3 points, config changes, watched issues closed. Compare every old STATE pick with the new ones.
    Done when: every old and new STATE pick is accounted for.

## Audit brief

Paste this to the audit subagent, verbatim:

> Audit `local-models-report.html` in this directory (the rendered page, plus the hidden STATE comment at the end). Research only, edit nothing. Treat every factual claim as unverified until you check it against its source. Check every one:
> 1. Every tier heading's machine list against `machines.yaml`: each chip × memory pairing listed must exist there, and every `machines.yaml` row must appear in exactly one tier.
> 2. Every hardware fact (memory options, bandwidth, GPU, VRAM) against the source URL in `machines.yaml` or the report's Sources table.
> 3. Every Ollama tag: it exists on `https://ollama.com/library/<model>/tags`, and its size matches (`scripts/ollama_library.py tags <model>`).
> 4. Every score (GS, TB) against `scripts/aa.py show "<name>"`, including the "E" marker and the effort row.
> 5. Every Equivalent paid model against `scripts/aa.py nearest "<AA name>"`.
> 6. Every rank against the Ranking rules in `.opencode/skills/refresh-local-models/SKILL.md`.
> 7. Every Est. tok/s against the Speed estimate formula there.
> 8. Every issue number and its state against `https://api.github.com/repos/ollama/ollama/issues/<n>`.
> 9. Every config claim against the page cited for it.
> 10. The STATE `[picks]` lines match the tier tables row for row.
> 11. Every number written in prose (bullets) matches the tables or a cited source.
> 12. No reader-visible text mentions this project's files, scripts or process; all such content is inside the STATE comment.
> Write any throwaway files only inside a new subdirectory of the temp directory.
> Return a list: location in the report, the claim, what the source says, the source. Return "0 errors" only if every claim in the report was checked.

## Fit rules (estimates)

- Mac up to 36 GB: weights <= 60% of unified memory (macOS GPU cap + 64k context + OS).
- Mac 48 GB and up: weights + KV cache at 64k context <= RAM - 16 GB (macOS and apps); above macOS's default GPU cap (~2/3 of RAM below 64 GB, ~3/4 at 64 GB+) this needs `iogpu.wired_limit_mb` raised (Report config section 3). KV cache = f16 K+V for the attention layers only, computed from the GGUF header (`block_count`, `attention.head_count_kv` (array → per layer, 0 = no attention), `key_length`/`value_length`, `full_attention_interval`, `sliding_window` + pattern: sliding layers hold only the window). Check the advised `num_ctx` (Report config section 2) the same way.
- Windows discrete GPU, model in VRAM: weights <= VRAM - 3 GB. A model too big for that runs split with system RAM (next rule).
- Windows, MoE split GPU/system RAM or integrated GPU: weights <= RAM - 10 GB.
- Agentic coding needs 64k context (Ollama's OpenCode minimum: https://docs.ollama.com/integrations/opencode).
- Mac tags: rank GGUF tags; rank an MLX tag (for both use cases) only when its GGUF tag doesn't fit. ollama/ollama#18620 (MLX tool-call leak) was fixed in Ollama v0.40.4, so MLX tags are no longer barred from coding. Mac General tables carry an **MLX swap** column naming the `-nvfp4` tag of the same model (else `-mlx`; `—` if none; say "avoid" when an open bug hits only the MLX tag) (size = sum of the manifest's layer sizes). Since Ollama 0.40, short tags (e.g. `qwen3.5:9b`) can be manifest lists with an MLX and a GGUF child, and Apple silicon picks MLX; list explicit GGUF tags (check the manifest's `runner` with `Accept: application/vnd.ollama.manifest.list.v2+json`).

## Speed estimate

Est. tok/s = 0.6 × bandwidth (GB/s) ÷ GB read per token. GB read per token = tag size for dense models, tag size × active/total params for MoE. Bandwidth = Mac unified memory; Windows VRAM if the model fits in VRAM, else system RAM. Display the range from the lowest to the highest bandwidth figure across the tier's machines; ranking (rule 4) uses the lowest. Label it an estimate.

## Ranking rules

1. Filter: Ollama reports tool support (the `tools` badge, or a tool-handling GGUF chat template with no `renderer`, per step 5); fits **every** Machine in the tier (Fit rules); est. >= 15 tok/s on at least one Machine in the tier. Coding also needs a Terminal-Bench score >= 20.
2. Score: General = General score (GS); Coding = AA Terminal-Bench column (step 6). The Equivalent paid model is matched on the same score (`scripts/aa.py nearest`).
3. Tool-call flag (no score change): flag a model for coding when an open issue reports tool calls broken or dropped in normal use through the chat API (`/v1/chat/completions`, `/v1/messages` or `/api/chat`) by the model's Ollama tool-call **parser**. A model's parser is the `parser` field of its registry config blob: `https://registry.ollama.ai/v2/library/<model>/manifests/<tag>` → `config.digest` → `https://registry.ollama.ai/v2/library/<model>/blobs/<digest>`. Models sharing a parser share the flag; with no `parser` field, the flag covers only the model the issue names. Issues that need an unusual request (e.g. tools plus `response_format`), other endpoints, or hardware no fleet Machine has don't count; mention them in the Model reference. Exclude a model from coding only when such a bug is **confirmed**: an Ollama member or collaborator (GitHub `author_association` MEMBER/OWNER/COLLABORATOR) reproduces or acknowledges it, or a maintainer's fix PR is linked. Fix PRs from outside contributors don't count as confirmation. Check with `https://api.github.com/repos/ollama/ollama/issues/<n>/comments` and `/timeline`. Show the flag as ` ⚠` after the score in coding tables, and list the issue in the Model reference and Watched issues.
4. Sort by score. Then repeatedly swap neighbours within 3 points so the one with the higher est. tok/s on the tier's slowest Machine ranks first: pass from the top down, swapping each qualifying pair, and repeat passes until nothing changes. A Machine's speed uses the lowest bandwidth figure listed for it.
5. If none of the top 5 reaches 15 tok/s on every Machine in the tier, replace #5 with the best-ranked model that does; if none exists, say so in the tier notes.
6. Fewer than 5 picks is fine; never fill with models that fail the filter. If coding has no pick, or only picks that are slow on some Machines, write "use a cloud model" for those Machines.

Sampling: check each pick's Ollama default params (`ollama show <tag> --modelfile` or the registry) against its vendor card; list any mismatch as a Modelfile override in the config section.

Equivalent paid model: `scripts/aa.py nearest` (OpenAI, Anthropic, Google, xAI) on the score. Within 3 points it prefers measured, then current, then closest.

## Config sources

| Topic | Page |
|---|---|
| Context length defaults and setting it | https://docs.ollama.com/context-length |
| `/v1` ignores `num_ctx` | https://docs.ollama.com/api/openai-compatibility |
| Env vars (flash attention, KV cache, keep-alive, parallel) | https://docs.ollama.com/faq · https://raw.githubusercontent.com/ollama/ollama/main/envconfig/config.go |
| GPU / Vulkan / Windows drivers | https://docs.ollama.com/gpu · https://docs.ollama.com/windows |
| OpenCode integration | https://docs.ollama.com/integrations/opencode |
| OpenCode provider config (2.x) | https://opencode.ai/v2/docs/providers · https://opencode.ai/v2/docs/models · https://opencode.ai/v2/docs/config · https://opencode.ai/v2/docs/compaction |
| MLX / NVFP4 | https://ollama.com/blog (MLX posts) |
| Mac GPU memory limit | https://github.com/ml-explore/mlx-lm (README) |
