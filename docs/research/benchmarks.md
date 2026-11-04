# Benchmarks for ranking local models: what to keep, add or watch

Research note, 2026-11-04. AA figures are from the cache used for the 2026-11-02 Refresh (`.cache/aa_models.json`, `/tmp/opencode/aa_raw.json`, AA Index v5.0.1); everything else was read on 2026-11-04 unless a row says otherwise. "Candidates" means the 57 models in `candidates.json` (50 mapped to an AA name; Ornith ×4, Ornith 1.5 122B, Flint and LFM3 aren't on AA). "Paid" means OpenAI, Anthropic, Google and xAI models, counted as *current / including deprecated* where AA marks deprecation. Anything not checked against a primary source is marked **(unverified)**.

## Summary: recommendations

**Agentic coding**

- **Keep AA Terminal-Bench 2.1 as the coding score.** It's still the only independent, one-harness benchmark that scores most of our candidates (36/57, spread 0-86.1) and current paid models (16 current, 79 including deprecated) [1][2]. AA has removed it from the Index but still runs it on new models (Qwen3.8 and GPT-6 Astra both have rows) [2].
- **Add a harness rule for vendor fallbacks: accept only Terminal-Bench 2.1 rows run with Terminus 2.** That's AA's harness [2]. Vendor cards report scores from different harnesses (Terminus 2, Claude Code, OpenCode) [4][5][6]. Ornith publishes both a Terminus 2 and a Claude Code number [4].
- **Widen the uncertainty on Ornith's scores (about ±8 points).** Ornith's own table puts competitors 8 points off AA: Qwen3.6-35B-A3B at 52.5 vs AA's 44.9, and Qwen3.5-9B at 21.3 vs AA's 29.2 [4][1]. NVIDIA's Bolt card matches AA within 2 points on three shared models [6][1], so NVIDIA's vendor scores look comparable to AA's.
- **Don't switch to Terminal-Bench 4.0, FrontierCode 2.0 or the AA Coding Agent Index.** They're too hard for local models, or don't score them. On AA's TB 4.0, 25 of the 29 scored candidates get 0-0.5. FrontierCode 2.0 covers 7 candidates (0-11.5). The tbench.ai 4.0 board and the AA Coding Agent Index score none of our candidates [1][3][7].
- **Watch SWE-rebench.** It's independent and decontaminated, but its current window scores only 3 candidates and it hasn't been updated since 2026-07-01 [8].
- **Watch LMArena's Agent arena.** It scores 4 candidates (Qwen3.8 27B, Qwen3.8-Flash-Next, Mistral Medium 3.5, Nemotron 3.5 Super VL) against 57 models, most of them paid [9]. Its harness is (unverified).
- **Don't use SWE-bench Verified, Aider Polyglot, LiveCodeBench or BFCL for ranking.** Their official boards are stale (newest entry Feb 2026 / Oct 2025 / Apr 2026) and score 0-3 candidates [10][11][12]. SWE-bench Verified is also saturated at the top: 97% on Vals' run [13].

**General use**

- **Keep GS = HLE 10 + AA-LCR 5 + CritPt 5 for now.** These are the only AA general evals that score all 50 AA-mapped candidates and 54-56 current paid models. HLE runs from 1.1 to 38.0 and AA-LCR from 0 to 83.3 across the candidates [1].
- **Consider dropping CritPt (low impact either way).** 27 of 50 candidates score 0, and only Qwen3.8-Flash-Next (11.1) and Nemotron 3.5 Super (10.6) score above 4.3. At weight 5 it adds at most 2.8 GS points [1].
- **Watch HLE-Diamond (likely successor to HLE) and AA-Omniscience v1.1.** AA's Index v5 uses both [2]. They cover 22/50 and 11/50 candidates today, against 54 and 52 current paid models [1]. HLE-Diamond is also compressed for local models: 2.8-16.3, and 9.1 or less for all but Qwen3.8-Flash-Next [1].
- **Don't add IFBench or GPQA Diamond.** IFBench separates candidates well (17.6-80.4), but AA hasn't run it on the 9 newest candidates (Qwen3.8, Nemotron 3.5, Granite 4.2, Muse Glimmer), and only 3 current paid models have it [1][2]. GPQA is saturated: most candidates of 4B and up score 75-92 [1].
- **Optionally show LMArena text (style control) beside GS, but don't use it in the score.** It's the only human-preference signal for writing and chat. It covers 19/57 candidates (Elo 1290-1452) and 124 paid entries, but misses every Qwen3.5 model below 27B, Qwen3.6, Gemma 4 E2B/E4B/12B, Ornith, Flint and LFM [9].

**Quantization and Ollama**

- **No independent leaderboard scores 4-bit GGUF, MLX or NVFP4 builds.** The best evidence is one independent study [14]: on Qwen3.8 27B, the Q4_K_M build matched BF16 on Terminal-Bench 2.1, GPQA and IFBench, 2-bit lost some, and 1-bit collapsed. That supports the report's "the score belongs to the model" rule down to 4-bit. Keep flagging 2-bit picks.
- **No benchmark measures tool calling through Ollama or llama.cpp at a level we could rank on.** There are only small community harnesses [15][16][17]. **Recommendation:** add a Refresh step that runs a short Terminal-Bench 2.1 subset with the OpenCode agent against Ollama, one machine per new pick. Harbor runs OpenCode, per [18].

## Agentic coding: benchmark comparison

Coverage counts come from AA data (AA rows), page data embedded in each leaderboard (SWE-bench, SWE-rebench, tbench.ai 4.0, BFCL CSV, LMArena parquet) or Epoch's export (TB 2.0).

| Benchmark | Owner / runner | What it measures | Independent? | Candidates covered (/57) | Paid covered | Spread among candidates | URL |
|---|---|---|---|---|---|---|---|
| **Terminal-Bench 2.1 (AA)**, current score | AA runs it on the Stanford/Laude task set; Terminus 2 harness, 250 episodes, 3 repeats [2] | 89 terminal tasks: SWE, sysadmin, data, security | Yes, one harness | **36** (AA) + 9 vendor-only, e.g. Ornith ×5, Flint, LFM3, Nemotron 3.5 Super/Bolt | 16 current / 79 | **0-86.1** (median 26) | [1][2] |
| Terminal-Bench 2.1 (tbench.ai board) | Laude/Stanford; open submissions, mixed agents | Same tasks | Mixed submitter-run | **(unverified)**: the board renders client-side; one secondary source counts 18 entries, frontier only [19] | Yes | n/a | tbench.ai/leaderboard/terminal-bench/2.1 |
| Terminal-Bench 2.0 (tbench.ai, via Epoch mirror) | Laude/Stanford; open submissions | Older task set | Mixed | 4: Qwen3.6-35B-A3B 24.6 and Qwen3.5-9B 9.2 (both "little-coder" agent), gpt-oss-120b 18.7, gpt-oss-20b 3.1 | 167 rows | 3-25 | [20] |
| Terminal-Bench 4.0 (AA) | AA; mini-swe-agent [2] | 66 harder terminal tasks | Yes | 29, but 25 score 0-0.5 | 54 current | 0-25.3 (Qwen3.8-Flash-Next) | [1][2] |
| Terminal-Bench 4.0 (tbench.ai) | Laude/Stanford | Same | Submitter-run, mostly vendor harnesses (Claude Code, Codex) | **0** of 35 rows | 31 rows | n/a | [3] |
| FrontierCode 2.0 (AA) | Cognition tasks, AA runs them in its Stirrup harness [2] | Mergeable changes to real repos | Yes | 7 | 52 current | 0-11.5 | [1][2] |
| AA Coding Agent Index (FrontierCode 1.1 + TB 4.0 + SWE-Atlas-QnA) | AA | Agent+model pairs (Claude Code, Codex, OpenCode…) | Yes | **0**; OpenCode appears only with GLM-5.3 | ~30 agent variants | n/a | [7] |
| SWE-bench Verified (official, incl. bash-only view) | Princeton/SWE-bench team; mini-swe-agent for bash-only | 500 Python GitHub issues | Mixed; bash-only rows are run by the team | 3: Devstral Small 2 56.4, Devstral 2 53.8, gpt-oss-120b 26.0. Newest entry 2026-02-26 | Many, older models only | 26-56 | [10] |
| SWE-bench Verified (Vals) | Vals AI, mini-swe-agent | Same | Yes | 3: Devstral 2 62.8, Mistral Medium 3.5 66.4, Nemotron 3.5 Lightning 52.8. Archived 2026-09-01 as saturated | Yes | 53-66 | [13] |
| SWE-bench Verified / Multilingual (vendor cards) | Each vendor | Same | **Vendor**; harness varies: OpenHands (Ornith), mini-swe-agent (Flint), internal scaffold (Qwen), **OpenCode (Liquid)** | Most new models | n/a | n/a | [4][5][21] |
| SWE-bench Pro (Scale) | Scale AI | 1,865 harder long-horizon tasks | Yes for board rows | 0 small candidates seen on the board (unverified count) | Yes | n/a | labs.scale.com/leaderboard/swe_bench_pro |
| SWE-rebench | Nebius; own ReAct "tools" scaffold | Fresh, decontaminated GitHub tasks, monthly windows | Yes | **3** in current window (15 May-1 Jul 2026, 111 tasks): Qwen3.6-27B 31.2, Qwen3.6-35B-A3B 24.7, Qwen3.5-35B-A3B 17.1. About 12 across earlier windows: gpt-oss ×2, Gemma 4 31B, Qwen3.5-27B, Qwen3-Coder-Next, GLM-4.7-Flash, Devstral ×2, … | 6 models in current window (plus Claude Code and Codex as agents) | 17-31 | [8] |
| LMArena Agent arena | LMArena | Human-judged agent sessions (harness unverified) | Yes (crowd) | 4 (above) | Most of 57 | Narrow score scale (−0.2 to 0.2) | [9] |
| LiveCodeBench (AA legacy) | AA | Single-shot competitive coding (not agentic) | Yes | 18, none newer than Qwen3.5 | 1 current / 93 | 1.9-87.8 | [1] |
| Aider Polyglot | Aider | Diff-editing exercises | Yes | 1 (gpt-oss-120b); newest entry 2025-10-03 | Old models | n/a | [11] |
| τ²-Bench Telecom (AA legacy) | Sierra tasks, AA run | Multi-turn tool use with a simulated user | Yes | 41; missing the 9 newest candidates | 3 current / 114 | 12.6-98.8 | [1] |
| τ³-Banking (AA legacy) | Sierra tasks, AA run | Tool use and knowledge retrieval | Yes | 28 | 16 current / 80 | 3.7-47.4 | [1] |
| BFCL v4 (official) | UC Berkeley Gorilla | Function-call accuracy: single, parallel, multi-turn, web, memory | Yes | 1-2: Qwen3-4B-Instruct-2507 35.7, Granite-4.0-350m 19.0 (non-H variant). Last updated 2026-04-12 | 32 rows | n/a | [12] |
| MCP-Atlas | Scale AI | Multi-step tool use over 36 real MCP servers | Official board updated 2026-04-08; newer rows on aggregators are vendor-reported | (unverified) Aggregators list Qwen3.5-27B 68.4, Muse Glimmer 75.5, Qwen3.6-35B-A3B 62.8, Gemma 4 31B 57.2 [22] | Yes | 57-76 | labs.scale.com/leaderboard/mcp_atlas |
| ITBench-AA | IBM tasks, AA run | Kubernetes root-cause diagnosis | Yes | 6 | 6 current | 1.1-37.3 | [1][2] |

### Harness: does AA's Terminus 2 stand in for OpenCode?

- **Same model, different harness, small difference for strong models.**
  - Scale/Reflection ran GLM-5.3, Kimi K3 and Inkling through mini-swe-agent, Pi and OpenCode on SWE-Bench Pro v2, and found "on-par performance" for the strongest models [23] (read from a search excerpt).
  - Harness-Bench ranks OpenCode first of 7 harnesses: 66.3 mean, with every harness between 59.7 and 66.3. Its backends include Gemma-4-31B and Qwen3.8-27B served locally [24].
  - Strands' 94k-trial study found OpenCode had the highest accuracy on open-weight models (42.93%) [18] (read from a search excerpt).
- **Small models may be more harness-sensitive.**
  - Liquid ran Terminal-Bench 2.1 with the OpenCode agent, capped at 100 turns. Qwen3.5-4B scored 13.48 and Qwen3.5-9B 17.98, against AA's Terminus 2 scores of 25.8 and 29.2 [5][1].
  - The same card reports SWE-bench Verified (OpenCode) of 43.4 for LFM3-1.7B, 41.2 for Qwen3.5-4B and 51.2 for Qwen3.5-9B [5].
  - The cause of the TB gap (harness, turn cap or sampling) isn't established (unverified).
- **Vendor-card calibration against AA Terminal-Bench 2.1:**

| Source of score | Model | Vendor's number | AA | Difference |
|---|---|---|---|---|
| NVIDIA Bolt card [6] | Qwen3.6-35B-A3B / Gemma 4 26B-A4B / Nemotron 3.5 Lightning | 44.4 / 37.2 / 23.5 | 44.9 / 39.0 / 24.3 | −0.5 / −1.8 / −0.8 |
| Ornith 1.5 page, Terminus 2 [4] | Qwen3.6-35B-A3B / Qwen3.5-9B / Gemma 4 31B | 52.5 / 21.3 / 42.1 | 44.9 / 29.2 / 43.4 | +7.6 / −7.9 / −1.3 |
| Liquid LFM3 card, OpenCode [5] | Qwen3.5-4B / Qwen3.5-9B | 13.5 / 18.0 | 25.8 / 29.2 | −12.3 / −11.2 |

Ornith's `ornith-1.5:35b` (67.8) and `ornith-1.5:9b` (46.2) are the Terminus 2 rows [4], which is the right column to compare with AA. Flint's 54.9 is also Terminus 2 [21].

## General use: benchmark comparison

| Benchmark | Owner / runner | What it measures | Independent? | Candidates covered (/57) | Paid covered | Spread among candidates | URL |
|---|---|---|---|---|---|---|---|
| **HLE** (AA legacy), in GS | CAIS/Scale questions, AA run | Expert reasoning and knowledge | Yes | **50** | 54 current / 229 | **1.1-38.0** | [1][2] |
| **AA-LCR** (AA legacy), in GS | AA | Reasoning over ~100k-token document sets | Yes | **50** | 55 / 198 | **0-83.3** | [1][2] |
| **CritPt** (AA legacy), in GS | CritPt authors, AA run | Research-level physics | Yes | 50 | 56 / 200 | 0-11.1; 27 score 0 | [1] |
| HLE-Diamond (Index v5) | CAIS/Scale; AA run | Cleaned 1,000-question HLE | Yes | 22 | 54 / 63 | 2.8-16.3 (compressed) | [1][2] |
| AA-Omniscience v1.1 (Index v5) | AA | Factual recall with a hallucination penalty | Yes | 11 | 52 / 58 | Accuracy 9.2-28.0 | [1][2] |
| GDP.pdf (Index v5) | AA | Answers grounded in long PDFs (rubric all-pass) | Yes | 29 | 54 / 112 | 0-15.6 | [1][2] |
| IFBench (AA standalone) | AI2 dataset, AA run | Precise instruction following | Yes | 41; missing 9 newest | 3 / 116 | 17.6-80.4 | [1][2] |
| GPQA Diamond (AA legacy) | NYU dataset, AA run | Graduate science MCQ | Yes | 48 | 18 / 187 | 11.1-92.3; most ≥4B models score 75-92 | [1] |
| GPQA Diamond (Epoch run) | Epoch AI | Same | Yes | ~25, incl. Qwen3.5/3.6, Gemma 4 (minimal effort), gpt-oss | 170 rows | 11-86 | [20] |
| SimpleQA Verified (Epoch) | Epoch AI | Short factual QA | Yes | 1 (Gemma 4 31B, 10.4) | 62 rows | n/a | [20] |
| MLCR-AA (medical long context) | AA | Long medical-record reasoning | Yes | 15 | 47 / 104 | 0-20.6 | [1] |
| LMArena text, style control | LMArena (arena.ai) | Crowd preference in open chat; style control discounts length and formatting | Yes (crowd); some open models are served as NVFP4 builds | **19**: Gemma 4 31B 1452, 26B 1438, Qwen3.8-27B 1436, Mistral Medium 3.5 1426, Muse Glimmer 1425, Qwen3.5-122B/27B/35B, Nemotron 3.5 Super/Lightning, Granite 4.2 ×3 (1290-1340), gpt-oss ×2, … | 124 rows | 1290-1452 (CI about ±7) | [9] |
| RULER 128K, MRCR | Vendor cards only | Long-context retrieval | Vendor | n/a | n/a | n/a | e.g. [5] |
| MMLU-Pro | AA legacy (no longer in AA's leaderboard data) | Knowledge MCQ | n/a | not checked | n/a | n/a | [2] |

## Quantization: is there a benchmark of 4-bit builds?

No maintained, independent leaderboard scores quantized local builds across models. What exists:

| Source | Kind | Finding |
|---|---|---|
| Quesma, "Benchmarking Qwen3.8 27B quantizations" (2026-08-26) [14] | Independent blog, llama.cpp, Unsloth GGUFs | Q4_K_M matched BF16 on Terminal-Bench 2.1 (89 tasks), GPQA Diamond and IFBench, and BF16 reproduced Qwen's reported scores. UD-Q2_K_XL showed a "noticeable fall" on Terminal-Bench, and 1-bit collapsed to chance on GPQA. Only one model was tested, and some files have since been replaced upstream. |
| NVIDIA Nemotron 3.5 Bolt 74B-A9B card [6] | Vendor | Terminal-Bench 2.1 50.98 was measured on the IQ2 build itself. |
| Recursive Flint card [21] | Vendor | Terminal-Bench 2.1: 54.9 BF16, 53.7 NVFP4. |
| NVIDIA Nemotron 3.5 Super VL card (https://build.nvidia.com/nvidia/nemotron-3.5-super-vl-120b-a12b.md) | Vendor | BF16 and NVFP4 benchmark table, per `report.md` ref 32 (not re-read today). |
| LMArena text [9] | Independent | Nemotron 3.5 Super and Lightning are rated as "(NVFP4)" deployments, i.e. a quantized build. |
| Kaitchup, Qwen3.8 Flash Next GGUF Q4→Q1 (2026-09-30) | Independent newsletter, paywalled | Its free intro says every standard quant cleared 95% accuracy recovery (unverified beyond the intro). |
| yrougy/llm-quant-bench (GitHub) | Community | GGUF quant ladders for Gemma 4 and Qwen 3.x on BigCodeBench, MUSR and BFCL, with q4_0 KV cache (unverified results). |

Takeaway: 4-bit K-quants and NVFP4 lose little on agentic and reasoning tasks, based on one independent study and two vendor cards. 2-bit loses measurably unless the vendor trained for it (Bolt). We have no evidence for MLX 4-bit or for quantized KV cache.

## Tool calling through Ollama or llama.cpp

No leaderboard tests models served through Ollama with tool calls at our coverage or quality bar. The closest:

- **MikeVeerman/tool-calling-benchmark** [15]: 21 small models on Ollama and llama.cpp, CPU only, 12 single-turn prompts × 20 runs, Feb 2026.
  - It notes that "Ollama's native tool API returns only the first tool call" at that time.
  - None of our current picks are tested.
- **guofeng201507/local-llm-ollama-benchmark** [16]: BFCL subsets through Ollama `/api/chat`, July 2026.
  - Results: Qwen3.5 9B 16/20 and Gemma 4 E4B 15/20 on simple_python.
  - Every model scored 0/5 on strict multi-turn tasks. The samples are tiny.
- **adatoo/quail ADR-0063** [17]: runs BFCL against Ollama, llama-server and MLX engines on the same files. It found engine-side parser failures (Gemma 4 tool calls not parsed), which shows the serving layer matters as much as the model.
- AA, tbench.ai, SWE-bench, BFCL and Scale all run models through vendor APIs or vLLM/SGLang, not Ollama [2][10][12].

Recommendation: keep the ⚠ parser flag, and add a measured smoke test to each Refresh. ClawProBench shows the OpenCode CLI driving Terminal-Bench 2.1 [19], and Strands ran OpenCode on Harbor [18].

## Sources

1. Artificial Analysis leaderboard data (per-eval `scores` slugs; deprecated models from model pages), cached 2026-11-02: https://artificialanalysis.ai/leaderboards/models
2. AA, Intelligence Benchmarking methodology, v5.0.1 (eval list, harnesses, legacy status, version history): https://artificialanalysis.ai/methodology/intelligence-benchmarking
3. Terminal-Bench 4.0 leaderboard (35 rows parsed from page data): https://www.tbench.ai/
4. Ornith-1.5 announcement and full tables (Terminus 2 and Claude Code columns; SWE-bench via OpenHands): https://ornith.ai/ornith_1_5.html
5. Liquid AI, LFM3-1.7B card ("SWE-bench Verified (OpenCode)", "Terminal-Bench 2.1 (OpenCode)", 100-turn cap, BF16 on vLLM): https://huggingface.co/LiquidAI/LFM3-1.7B
6. NVIDIA, Nemotron 3.5 Bolt 74B-A9B 24GB GGUF card: https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-24GB-GGUF
7. AA Coding Agent benchmarks (Coding Agent Index v2.0): https://artificialanalysis.ai/agents/coding
8. SWE-rebench leaderboard (window 15/05/2026-01/07/2026; news log): https://swe-rebench.com/
9. LMArena leaderboard dataset, `text_style_control` (published 2026-10-28) and `agent` (2026-11-02) latest splits: https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset; board: https://lmarena.ai/leaderboard/text
10. SWE-bench leaderboards (embedded `leaderboard-data`): https://www.swebench.com/
11. Aider Polyglot leaderboard data: https://github.com/Aider-AI/aider/blob/main/aider/website/_data/polyglot_leaderboard.yml
12. BFCL v4 leaderboard and CSV: https://gorilla.cs.berkeley.edu/leaderboard.html, https://gorilla.cs.berkeley.edu/data_overall.csv
13. Vals AI SWE-bench Verified (archived 2026-09-01) and Terminal-Bench 2.0: https://www.vals.ai/benchmarks/swebench, https://www.vals.ai/benchmarks/terminal-bench-2
14. Quesma, Qwen3.8 27B quantizations: https://quesma.com/blog/qwen38-27b-quantizations-benchmarked
15. https://github.com/MikeVeerman/tool-calling-benchmark
16. https://github.com/guofeng201507/local-llm-ollama-benchmark/blob/main/2026-07-26-bfcl-tool-calling-summary.md
17. https://github.com/adatoo/quail/blob/main/docs/adr/0063-benchmark-comparison-method.md
18. Strands Agents, "We ran 94,000 trials to measure the cost of harness choice" (2026-10-13): https://strandsagents.com/blog/we-ran-94000-trials-to-measure-the-cost-of-harness-choice/
19. ClawProBench Terminal-Bench 2.1 (OpenCode agent): https://suyoumo.github.io/terminal-bench; TB 2.1 board entry count (secondary): https://capitalandcompute.net/blog/opencode-vs-claude-code-vs-openclaude
20. Epoch AI benchmarking data export (`terminalbench_external.csv` mirrors tbench.ai TB 2.0; `gpqa_diamond.csv`, `simpleqa_verified.csv`): https://epoch.ai/data/benchmark_data.zip
21. Recursive, Flint card (Terminus 2 for Terminal-Bench, mini-swe-agent for SWE-bench): https://huggingface.co/RecursiveSI/flint
22. MCP-Atlas official board: https://labs.scale.com/leaderboard/mcp_atlas; aggregator listing (unverified): https://vectorwire.ai/benchmarks/mcp-atlas
23. Scale Labs, SWE-Bench Pro V2 (harness study by Reflection): https://labs.scale.com/blog/swe-bench-pro-v2
24. Harness-Bench leaderboard: https://www.harness-bench.ai/leaderboard.html
