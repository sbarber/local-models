# Local Models Report

**Updated:** 2026-11-04 · **Stack:** OpenCode 2.2.5 [\[1\]](#ref-1) + Ollama 0.40.13 [\[2\]](#ref-2)

<nav class="toc">
<strong>Contents</strong>
<ul>
<li><a href="#summary">Summary</a></li>
<li><a href="#how-to-read-this">How to read this</a></li>
<li><a href="#how-the-tiers-are-drawn">How the tiers are drawn</a></li>
<li><a href="#top-models-by-tier">Top models by tier</a>
<ul>
<li><a href="#tier-mac-m1-8">Mac M1, 8 GB</a></li>
<li><a href="#tier-mac-8">Mac 8 GB</a></li>
<li><a href="#tier-mac-m1-16">Mac M1, 16 GB</a></li>
<li><a href="#tier-mac-16-24">Mac 16-24 GB</a></li>
<li><a href="#tier-mac-32-36">Mac 32-36 GB</a></li>
<li><a href="#tier-mac-48-96">Mac 48-96 GB</a></li>
<li><a href="#tier-mac-128">Mac 128 GB</a></li>
<li><a href="#tier-latitude">Latitude 7350</a></li>
<li><a href="#tier-win-32">Windows 32 GB</a></li>
<li><a href="#tier-pm16p-8-16">Pro Max 16 Plus, 8-16 GB GPU</a></li>
<li><a href="#tier-pm16p-24">Pro Max 16 Plus, 24 GB GPU</a></li>
</ul></li>
<li><a href="#model-reference">Model reference</a></li>
<li><a href="#config-changes">Config changes</a>
<ul>
<li><a href="#config-server">1. Ollama server settings</a></li>
<li><a href="#config-context">2. Per-model context fix</a></li>
<li><a href="#config-gpu-limit">3. Mac GPU memory limit</a></li>
<li><a href="#config-tags">4. Tag choice</a></li>
<li><a href="#config-opencode">5. OpenCode 2.x</a></li>
</ul></li>
<li><a href="#watched-issues">Watched issues</a></li>
<li><a href="#sources">Sources</a></li>
</ul>
</nav>

## Summary

- **New this time: three changes to how models are scored.**
  - **General score (GS) = HLE 10 + AA-LCR 5.** CritPt is gone: most local models score 0 on it, so it barely moved any score. AA-Omniscience has been out since 2026-11-02, after Artificial Analysis replaced it with a version few of the models here have scores on yet [\[3\]](#ref-3)[\[4\]](#ref-4). GS values are on a new scale, so don't compare them with earlier versions of this report ([how to read this](#how-to-read-this)).
  - **A vendor's Terminal-Bench score counts only if it was run the way AA runs it,** with the Terminus 2 agent. Scores from Claude Code, OpenCode or an unnamed setup aren't comparable. Two coding picks drop out: `ornith-1.5:122b-nvfp4` (Mac 128 GB), whose card describes only a Claude Code run, and `nemotron-3.5-bolt:74b-a9b-iq2` (Pro Max 16 Plus), whose card doesn't name its setup [\[5\]](#ref-5)[\[6\]](#ref-6).
  - **General tables now show each model's LMArena rating** beside GS: people's votes on which of two answers they prefer, the main crowd-preference measure of writing and chat. It isn't part of GS, and many small models have no rating ([how to read this](#how-to-read-this)) [\[7\]](#ref-7).
- **What moved in General:** `qwen3:4b-thinking-2507-q4_K_M` now leads the base M1 Macs (GS 16.6), `gemma4:12b-nvfp4` rises to \#2 on 16-24 GB Macs, and `qwen3.5:122b-a10b-q4_K_M` passes `nemotron-3.5-super` on Mac 128 GB. `nemotron-3-nano:4b` joins the 8 GB Mac and Latitude tables, `minicpm-v4.6:q4_K_M` (a small model that also reads images) the base M1 tables, and `qwen3.5:9b-q4_K_M` the Pro Max 16 Plus 8-16 GB GPU table.
- **LFM3 from Liquid AI is new in Ollama, but it isn't ranked.** Ollama 0.40.12 added `lfm3` (1.7B), `lfm3-vl`, `lfm3-audio` and `lfm3-omni`, and 0.40.13 runs them on Windows and Linux too [\[2\]](#ref-2). AA hasn't scored any of them, so they get no General score. Liquid's own Terminal-Bench 2.1 score for LFM3-1.7B is 12.9, measured in OpenCode rather than AA's setup, and Liquid says it isn't recommended for agentic coding [\[8\]](#ref-8)[\[9\]](#ref-9). With a 1.1 GB 4-bit build and a 256k context window, it may still suit simple tool-calling agents on 8 GB machines; that's untested here.
- **Mac tables list the best build of each model, MLX or GGUF.** On Apple silicon Ollama runs two kinds of build: GGUF (through llama.cpp, the same files as on Windows) and MLX (Apple's machine-learning framework) [\[10\]](#ref-10)[\[11\]](#ref-11). Each Mac pick uses whichever build fits the tier and is estimated faster; when the two are within 10%, the MLX build is listed, because Ollama reports its NVFP4 builds about 20% faster than `q4_K_M` [\[12\]](#ref-12) ([tag choice](#config-tags)).
- **For coding, `ornith-1.5:35b` ranks \#1 on Macs with 32-96 GB and on the Pro Max 16 Plus, on its vendor's own score only** (TB 67.8) [\[13\]](#ref-13). Treat Ornith's scores as rough: on models AA also tests, Ornith's own Terminal-Bench numbers can differ from AA's, e.g. 52.5 for Qwen 3.6 35B-A3B against AA's 44.9 [\[13\]](#ref-13)[\[4\]](#ref-4). On Mac 128 GB, `qwen3.8-flash-next:125b-a6b-nvfp4` leads both use cases (GS 51.9, TB 86.1).
- **`nemotron-3.5-bolt:74b-a9b-iq2` is still ranked for General on the Pro Max 16 Plus** (\#3 on the 8-16 GB GPUs, GS 39.7). It's NVIDIA's own 2-bit release, trained for that precision, and runs on Windows only [\[6\]](#ref-6)[\[14\]](#ref-14); AA's GS is for the full-precision weights [\[15\]](#ref-15). `flint:40b-a2b-gguf-nvfp4` carries Recursive's TB 53.7 for its NVFP4 build [\[16\]](#ref-16).
- **Coding picks count the memory for 64k of context, OpenCode's minimum.** On Macs up to 36 GB they assume you raise macOS's GPU memory limit to about 80% of RAM ([section 3](#config-gpu-limit)). With that, the Ornith 35B MoE models fit the 32-36 GB coding table. On Windows 32 GB, `qwen3.5:35b-a3b` (General) and `ornith:35b` (coding) aren't listed: their context doesn't fit beside their weights. A few General picks on small machines need a context below 64k ([section 2](#config-context)).
- **Use Ollama 0.40.12 or later with OpenCode 2.** Before 0.40.12, `ollama launch opencode` passed a `--model` flag that OpenCode 2 rejects; 0.40.12 fixes that [\[2\]](#ref-2)[\[17\]](#ref-17). 0.40.9 brought Flint to Windows and its GGUF builds, and 0.40.4 fixed two MLX bugs that affected agent use [\[2\]](#ref-2)[\[18\]](#ref-18).
- **Below 32 GB, local agentic coding is weak.** The best picks score near Gemini 2.5 Pro or Claude 4.5 Haiku. On base M1 Macs (8 or 16 GB), no coding candidate passes the filters, so use a cloud model for coding there.
- **One config change matters more than model choice: context length.** Ollama defaults to 4k context below 24 GiB of GPU memory, OpenCode needs 64k or more, and Ollama's OpenAI-compatible `/v1` endpoint, which OpenCode uses, can't change it per request [\[19\]](#ref-19)[\[20\]](#ref-20)[\[21\]](#ref-21). Every pick below needs the [context fix](#config-context), MLX builds included.

------------------------------------------------------------------------

## How to read this

- **Hardware tier**: a group of machines that can run the same models. Each tier heading lists the machines in it.
- **Use cases**: **General use** is chat, writing and reasoning. **Agentic coding** is software development with the model in OpenCode: you give it a task, and the model reads, edits and runs code through OpenCode's tools to carry it out.
- **Scores** come from Artificial Analysis (AA) [\[4\]](#ref-4), which tests open and paid models with one harness:
  - General use: **General score (GS)**, built from AA's per-eval scores: the weighted mean of **HLE 10 and AA-LCR 5**. HLE is expert-level questions across many subjects; AA-LCR is reasoning over sets of long documents (about 100k tokens). Both were non-agentic, non-coding evals in AA's Intelligence Index up to v4.3.2; Index v5.0 (October 2026) moved them to AA's legacy evaluations, but AA still publishes them for almost every model [\[3\]](#ref-3)[\[4\]](#ref-4). A model missing either has no GS and isn't ranked for General. Paid equivalents use the same score.
  - **Left out:** AA-Omniscience, because v5.0 replaced v1 with v1.1, whose scores aren't comparable [\[3\]](#ref-3), AA's data no longer holds v1 results, and only a few of the models here have a v1.1 score yet [\[4\]](#ref-4). So GS has no factual-recall or hallucination component. CritPt (research-level physics), because most of the models here score 0 on it [\[4\]](#ref-4). GDP.pdf, because AA hasn't scored it for many of the models here [\[4\]](#ref-4).
  - Why not the full Index: v5.0 weights Knowledge Work, Coding, Science and General at 25% each, and most of it is agentic or coding evals [\[3\]](#ref-3), which the Agentic coding table already covers. GS is on a different scale from the Index, so don't compare the two numbers.
  - **LMArena** (General tables only, not part of GS): the model's rating on LMArena's text leaderboard with style control, which discounts long or heavily formatted answers. It comes from people's votes on which of two anonymous answers they prefer, so it's the closest measure of how good a model feels to chat and write with. The ± is half the width of LMArena's confidence interval. Higher is better; two models whose ranges overlap aren't clearly different. A dash means LMArena hasn't rated the model, which is true of most small models here. LMArena serves some models as their own quantized builds, e.g. NVIDIA's NVFP4 Nemotron models [\[7\]](#ref-7).
  - Agentic coding: **AA Terminal-Bench 2.1**. In AA's data, recent models such as Qwen3.8 have no Terminal-Bench Hard score, so 2.1 is the column that covers both sides [\[4\]](#ref-4). AA has since added Terminal-Bench 4.0 (10% of Index v5.0 [\[3\]](#ref-3)), and of the models here only `qwen3.8-flash-next` (25.3) and `qwen3.8:27b` (5.1) score above 5 on it; the rest score 0-5 or aren't scored, so it can't separate them [\[4\]](#ref-4).
  - Vendor-reported scores are used only when AA has none, and are flagged **(vendor)**. A vendor's Terminal-Bench 2.1 score counts only if the vendor says it used Terminus 2, the agent AA uses; scores run with another agent, such as Claude Code or OpenCode, or with an unnamed one, aren't used. The same model can score quite differently in different agents: Liquid's runs of Qwen 3.5 4B and 9B in OpenCode came out 11-12 points below AA's [\[8\]](#ref-8)[\[4\]](#ref-4).
  - **Effort rows:** where AA scores a model at several reasoning settings, the report uses the one Ollama runs by default: Medium for Qwen 3.8, and thinking on for Gemma 4 and the other thinking models [\[22\]](#ref-22).
- **Equivalent paid model**: a paid model whose score on the same benchmark is close. Among paid models within 3 points, current models come before deprecated ones, then the closest score.
- **Est. tok/s**: estimated output speed, computed as 0.6 × memory bandwidth ÷ GB of weights read per token. It's a rough estimate, **never measured** (unsourced). The range runs from the slowest to the fastest machine in the tier. MLX and GGUF builds use the same formula; Ollama's reported MLX speed-up isn't added.
- **Builds (Macs only):** each model is ranked once, as its best build for the tier. Its score belongs to the model, so the build only changes fit and speed. The build that fits and is estimated fastest is listed, but an MLX build within 10% of it is listed instead, unless that would cost the pick its 15 tok/s on any machine. Ranking uses the fastest build's speed, so the choice of build never moves a pick down. The Model reference lists the other build of each model.
- **Ranking rules:**
  - Every pick must support tool calls in Ollama, fit on every machine in the tier, and reach about 15 tok/s on at least one of them.
  - **Context memory:** coding picks must fit their weights plus 64k of context, OpenCode's minimum [\[20\]](#ref-20). General picks on Macs up to 36 GB and on the Dells are fit on their weights and must leave room for at least Ollama's default 4k context [\[19\]](#ref-19); where 64k won't fit, [section 2](#config-context) gives the largest context that does.
  - Tool support means Ollama reports it: either the model has the `tools` badge, or its model file carries a chat template that handles tools, which Ollama 0.40 also counts as tool support and runs through llama.cpp's own template code [\[23\]](#ref-23)[\[24\]](#ref-24). Ornith 1.5 and Granite 4.2 qualify the second way. MLX builds get tool support from their Ollama tool-call parser, the same one as their GGUF build [\[23\]](#ref-23)[\[18\]](#ref-18).
  - Coding picks need TB ≥ 20.
  - **⚠ marks a coding pick with an open tool-call bug report.** The report says tool calls break or go missing in normal use through Ollama's chat API, in the model's Ollama **parser** (the code that turns the model's output into tool calls). Every model that uses that parser gets the flag. A model without a parser is flagged only when a report names it. Reports that need an unusual request don't count.
  - The flag doesn't change the score or the rank. Before adopting a flagged pick, run a short OpenCode session that reads, edits and runs code, and watch for failed or missing tool calls.
  - A model is excluded from coding only when an Ollama maintainer confirms such a bug: they reproduce or acknowledge it, or link their own fix. As of 2026-11-02 no Ollama member or collaborator has confirmed any open report against a pick's parser. One Gemma 4 report was reproduced by an Ollama contributor (see the Mac 32-36 GB notes).
  - When two models are within 3 points, the one that's faster on the tier's slowest machine ranks higher.
  - Each tier keeps at least one pick that's fast on every machine in it, if one exists.

## How the tiers are drawn

Each tier heading below lists the machines it covers.

- **Macs use unified memory.** A model must fit the smallest machine in its tier.
  - **Up to 36 GB:** for General use, a model's weights should take no more than about 60% of RAM (estimate). For coding, the weights plus the memory for 64k of context must fit in 80% of RAM, which assumes you raise macOS's GPU memory limit to about that ([section 3](#config-gpu-limit)); the rest is left for macOS and apps (estimate).
  - **48 GB and up:** for both use cases, the weights plus the memory for 64k of context must fit in RAM minus 16 GB, which keeps 16 GB for macOS and apps (estimate). Context memory is computed from each model's file at Ollama's default precision; hybrid models that keep context in only some layers need much less. Models above macOS's default GPU memory cap need the cap raised ([section 3](#config-gpu-limit)).
- **18 GB and 24 GB Macs share a tier with 16 GB Macs.** Under the 60% fit rule, no better General model fits. For coding, `gemma4:26b-nvfp4` (TB 39.0) also fits 24 GB Macs with the raised GPU limit, but not the 16 and 18 GB ones; the tier lists only models that fit all of them.
- **Base M1 Macs (8 and 16 GB) have their own tiers.** Their bandwidth is so low that they get different picks from other Macs with the same memory.
- **The Latitude 7350, Pro 14 Premium and Pro Max 16 have no discrete GPU, or only a 6-8 GB one.** Their RAM bandwidth is about 90-137 GB/s, versus 150-614 on Pro/Max Macs.
  - Only **MoE models** reach usable speed on them. MoE (mixture of experts) means only a few billion parameters are read for each token.
  - Bandwidth figures: Apple specs [\[25\]](#ref-25); NVIDIA [\[26\]](#ref-26); Dell RAM speeds [\[27\]](#ref-27), with bandwidth computed as MT/s × 16 bytes, i.e. a 128-bit bus (estimate). Dell's manuals give the memory bus width as 64-bit; the report reads that as per channel, with two channels (unsourced). If the total bus is 64-bit, every Dell speed estimate that runs from system RAM halves. The base M1's ~67 GB/s isn't published by Apple; it's derived from Apple's "M2 has 50% more" (unsourced).
- **The Pro Max 16 Plus tiers depend on the GPU.**
  - A model runs entirely in VRAM if it's no bigger than VRAM minus 3 GB; for coding, its 64k context must also fit in VRAM. Only the 24 GB RTX PRO 5000 can hold a 27B dense model that way.
  - **Windows and Dell RAM:** a model run from system RAM must fit in RAM minus 10 GB (estimate); for coding, that includes 64k of context.
  - Otherwise Ollama splits the model between the GPU and system RAM, and RAM speed sets the pace.

------------------------------------------------------------------------

## Top models by tier

Each tier has one table per use case; ranks run 1-5 within each. Windows tables list GGUF builds. Mac tables list each model's best build for the tier, GGUF or MLX ([builds](#how-to-read-this), [tag choice](#config-tags)): MLX tags end in `-nvfp4` or `-int4`, except `flint:40b-a2b-gguf-nvfp4`, which is GGUF; every other tag is GGUF. Builds are 4-bit except `granite4:1b-h-q8_0` (8-bit; it has no 4-bit GGUF tag), and `nemotron-3.5-bolt:74b-a9b-iq2` (2-bit expert weights, the only Ollama build of it). ⚠ = open tool-call bug report ([ranking rules](#how-to-read-this)). General tables also show each model's LMArena rating, for reference only; a dash means LMArena hasn't rated it ([how to read this](#how-to-read-this)).

### MacBook Pro M1, 8 GB {#tier-mac-m1-8}

**Confidence:** General scores are from Artificial Analysis. Coding has no qualifying local pick. All speeds are estimates, not measurements on these machines.

**General use**

| \# | Model | Score | Est. tok/s | Equivalent paid model | LMArena |
|:---|:---|:---|:---|:---|:---|
| 1 | `qwen3:4b-thinking-2507-q4_K_M` | GS 16.6 | ~16 | GPT-6 Luna (Non-reasoning) | — |
| 2 | `granite4.2:3b-q4_K_M` | GS 12.5 | ~18 | GPT-5.4 nano (Non-reasoning) | 1290 ±12 |
| 3 | `granite4:1b-h-q8_0` | GS 5.7 | ~25 | GPT-5 nano (Minimal) | — |
| 4 | `minicpm-v4.6:q4_K_M` | GS 5.7 | ~25 | GPT-5 nano (Minimal) | — |
| 5 | `qwen3.5:2b-q4_K_M` | GS 8.7 | ~21 | GPT-5 nano (Minimal) | — |

**Agentic coding**

No pick.

- **Use a cloud model for agentic coding.** No coding candidate reaches the TB 20 floor and 15 tok/s on this chip.
- **`qwen3:4b-thinking-2507-q4_K_M` is \#1 for General** (GS 16.6), more than 3 points ahead of `granite4.2:3b-q4_K_M` (GS 12.5). Every pick here scores low (GS 5.7-16.6).
- **Stronger small models are too slow on this chip.** `qwen3.5:4b-q4_K_M` (GS 27.6 on other tiers) estimates about 12 tok/s here, under the 15 tok/s filter.
- **None of these picks has an LMArena rating**, except Granite 4.2 3B, which is near the bottom of the models here (1290 ±12) [\[7\]](#ref-7).
- **`granite4.2:3b-q4_K_M` has no `tools` badge in Ollama** but carries a tool-calling chat template in its model file, so Ollama supports tools with it [\[28\]](#ref-28)[\[23\]](#ref-23).
- **New: `minicpm-v4.6:q4_K_M` is General \#4** (GS 5.7). It's a 1.6 GB model that also reads images, built on Qwen3.5-0.8B [\[29\]](#ref-29). It has no `tools` badge, but its model file's chat template handles tools, so Ollama supports tools with it [\[23\]](#ref-23). It replaces `granite4:350m-h-q8_0`.

------------------------------------------------------------------------

### Mac 8 GB: M2 / M3 {#tier-mac-8}

**Confidence:** General scores are from Artificial Analysis. Coding scores are from Artificial Analysis. All speeds are estimates, not measurements on these machines. Picks marked ⚠ have unresolved tool-call reports.

**General use**

| \# | Model | Score | Est. tok/s | Equivalent paid model | LMArena |
|:---|:---|:---|:---|:---|:---|
| 1 | `qwen3.5:4b-q4_K_M` | GS 27.6 | ~18 | GPT-5.6 Terra (Non-reasoning) | — |
| 2 | `qwen3:4b-thinking-2507-q4_K_M` | GS 16.6 | ~24 | GPT-6 Luna (Non-reasoning) | — |
| 3 | `granite4.2:3b-q4_K_M` | GS 12.5 | ~27 | GPT-5.4 nano (Non-reasoning) | 1290 ±12 |
| 4 | `qwen3.5:2b-q4_K_M` | GS 8.7 | ~32 | GPT-5 nano (Minimal) | — |
| 5 | `nemotron-3-nano:4b-nvfp4` | GS 10.5 | ~21 | Grok 4 Fast (Non-reasoning) | — |

**Agentic coding**

| \# | Model | Score | Est. tok/s | Equivalent paid model |
|:---|:---|:---|:---|:---|
| 1 | `qwen3.5:4b-q4_K_M` | TB 25.8 ⚠ | ~18 | Gemini 2.5 Pro |

- **Agentic coding is weak here.** `qwen3.5:4b-q4_K_M` is the only model above the TB 20 floor (≈ Gemini 2.5 Pro). Consider a cloud model for serious coding work.
- **`qwen3.5:4b-q4_K_M` is \#1 for General** (GS 27.6), more than 10 points ahead of every other pick. Picks 2-5 score GS 8.7-16.6.
- **New: `nemotron-3-nano:4b-nvfp4` is General \#5** (GS 10.5), replacing `qwen3:4b-instruct-2507-q4_K_M`. It's NVIDIA's 4B hybrid Mamba-2 model; its MLX build (2.9 GB) is within 10% of the GGUF build `nemotron-3-nano:4b-q4_K_M` (2.8 GB), so the MLX build is listed. `qwen3.5:2b-q4_K_M` ranks above it because they're within 3 points and the 2B is faster.
- **The Qwen 3.5 4B and 2B picks are GGUF builds:** their MLX builds (`-nvfp4`, 4.0 and 2.5 GB) are more than 10% bigger, so slower.

------------------------------------------------------------------------

### MacBook Pro M1, 16 GB {#tier-mac-m1-16}

**Confidence:** General scores are from Artificial Analysis. Coding has no qualifying local pick. All speeds are estimates, not measurements on these machines.

**General use**

| \# | Model | Score | Est. tok/s | Equivalent paid model | LMArena |
|:---|:---|:---|:---|:---|:---|
| 1 | `qwen3:4b-thinking-2507-q4_K_M` | GS 16.6 | ~16 | GPT-6 Luna (Non-reasoning) | — |
| 2 | `granite4.2:3b-q4_K_M` | GS 12.5 | ~18 | GPT-5.4 nano (Non-reasoning) | 1290 ±12 |
| 3 | `granite4:1b-h-q8_0` | GS 5.7 | ~25 | GPT-5 nano (Minimal) | — |
| 4 | `minicpm-v4.6:q4_K_M` | GS 5.7 | ~25 | GPT-5 nano (Minimal) | — |
| 5 | `qwen3.5:2b-q4_K_M` | GS 8.7 | ~21 | GPT-5 nano (Minimal) | — |

**Agentic coding**

No pick.

- **Use a cloud model for agentic coding.** No coding candidate reaches both the TB 20 floor and 15 tok/s on this chip. The fastest one, `qwen3.5:4b-q4_K_M`, estimates about 12 tok/s.
- **This machine has its own tier because the base M1 is slow** (~67 GB/s, unsourced). Models that suit other 16 GB Macs, like `qwen3.5:4b-q4_K_M`, fail the speed filter here.
- **General picks are the same as on the M1 8 GB**; with 16 GB they have room for a 64k context ([section 2](#config-context)).

------------------------------------------------------------------------

### Mac 16-24 GB: M1 Pro / M2 / M2 Pro / M3 / M3 Pro / M4 / M4 Pro / M5 / M5 Pro {#tier-mac-16-24}

**Confidence:** General scores are from Artificial Analysis. Coding includes vendor-reported scores; see (vendor) in the table. All speeds are estimates, not measurements on these machines. Picks marked ⚠ have unresolved tool-call reports.

**General use**

| \# | Model | Score | Est. tok/s | Equivalent paid model | LMArena |
|:---|:---|:---|:---|:---|:---|
| 1 | `qwen3.5:9b-nvfp4` | GS 33.3 | 8-26 | GPT-5.4 nano (Medium) | — |
| 2 | `gemma4:12b-nvfp4` | GS 31.7 | 8-24 | Claude Sonnet 4.6 (Non-reasoning, High) | — |
| 3 | `qwen3.5:4b-q4_K_M` | GS 27.6 | 18-56 | GPT-5.6 Terra (Non-reasoning) | — |
| 4 | `granite4.2:8b-q4_K_M` | GS 21.5 | 11-35 | GPT-6 Luna (Non-reasoning) | 1290 ±11 |
| 5 | `qwen3:4b-thinking-2507-q4_K_M` | GS 16.6 | 24-74 | GPT-6 Luna (Non-reasoning) | — |

**Agentic coding**

| \# | Model | Score | Est. tok/s | Equivalent paid model |
|:---|:---|:---|:---|:---|
| 1 | `ornith-1.5:9b` | TB 46.2 (vendor) | 9-28 | Claude 4.5 Haiku (Reasoning), low confidence |
| 2 | `ornith:9b-q4_K_M` | TB 43.1 (vendor) ⚠ | 11-33 | GPT-5.6 Luna (Low), low confidence |
| 3 | `qwen3.5:9b-nvfp4` | TB 29.2 ⚠ | 8-26 | Gemini 2.5 Pro |
| 4 | `qwen3.5:4b-q4_K_M` | TB 25.8 ⚠ | 18-56 | Gemini 2.5 Pro |
| 5 | `gemma4:12b-nvfp4` | TB 27.3 ⚠ | 8-24 | Gemini 2.5 Pro |

- **`qwen3.5:9b-nvfp4` and `gemma4:12b-nvfp4` are MLX builds**, 7.2 and 7.7 GB against 6.6 and 7.2 GB for their GGUF builds (`qwen3.5:9b-q4_K_M`, `gemma4:12b-it-qat`). They're within 10%, so the MLX build is listed; the estimate is up to about 2 tok/s lower than the GGUF build's. One report says `gemma4:12b-mlx` (the same weights as `12b-nvfp4`) generates more slowly than the larger `gemma4:26b-mlx` ([\#17362](https://github.com/ollama/ollama/issues/17362), unconfirmed); if Gemma 12B is slow on your Mac, use `gemma4:12b-it-qat`.
- **`qwen3.5:9b-nvfp4` is \#1 for General** (GS 33.3), and `gemma4:12b-nvfp4` rises to \#2 (GS 31.7), now more than 3 points ahead of the faster `qwen3.5:4b-q4_K_M` (GS 27.6).
- **New: `qwen3:4b-thinking-2507-q4_K_M` is General \#5** (GS 16.6), replacing `granite4.2:3b-q4_K_M` (GS 12.5). `granite4.2:8b-q4_K_M` (\#4) has a tool-calling chat template but no `tools` badge [\[23\]](#ref-23).
- **On base M2/M3/M4 chips, the 8B, 9B and 12B models estimate 8-14 tok/s.** `qwen3.5:4b-q4_K_M` and `qwen3:4b-thinking-2507-q4_K_M` are fast on every machine in this tier.
- **LMArena rates only Granite 4.2 8B here** (1290 ±11) [\[7\]](#ref-7).
- **Both Ornith picks are ranked on vendor scores, not independent ones.** `ornith:9b-q4_K_M` is flagged because its parser has an open bug report on the 35B ([\#16992](https://github.com/ollama/ollama/issues/16992)).
- **`ornith-1.5:9b` isn't flagged, but may share a bug with its 35B sibling.** It has no Ollama parser, and the open bug ([\#17957](https://github.com/ollama/ollama/issues/17957)) names only `ornith-1.5:35b`. The proposed fix ([PR 17965](https://github.com/ollama/ollama/pull/17965)) says the cause covers `qwen35`-architecture models loaded without a renderer or parser; the 9B is one, though the PR doesn't name it. The bug shows only when a request sets both tools and a JSON response format.

------------------------------------------------------------------------

### Mac 32-36 GB: M1 Pro / M1 Max / M2 Pro / M2 Max / M3 Pro / M3 Max / M4 / M4 Max / M5 / M5 Max {#tier-mac-32-36}

**Confidence:** General scores are from Artificial Analysis. Coding includes vendor-reported scores; see (vendor) in the table. All speeds are estimates, not measurements on these machines. Picks marked ⚠ have unresolved tool-call reports.

**General use**

| \# | Model | Score | Est. tok/s | Equivalent paid model | LMArena |
|:---|:---|:---|:---|:---|:---|
| 1 | `qwen3.5:27b-int4` | GS 41.8 | 4-17 | Claude Haiku 5.5 (Low) | 1409 ±4 |
| 2 | `qwen3.6:27b-q4_K_M` | GS 41.2 | 4-16 | Claude Haiku 5.5 (Low) | — |
| 3 | `muse-glimmer:30b-nvfp4` | GS 42.4 | 4-16 | Claude Haiku 5.5 (Low) | 1425 ±10 |
| 4 | `gemma4:26b-nvfp4` | GS 34.8 | 29-111 | GPT-6.1 Terra (Non-reasoning) | 1438 ±7 |
| 5 | `qwen3.5:9b-nvfp4` | GS 33.3 | 10-38 | GPT-5.4 nano (Medium) | — |

**Agentic coding**

| \# | Model | Score | Est. tok/s | Equivalent paid model |
|:---|:---|:---|:---|:---|
| 1 | `ornith-1.5:35b` | TB 67.8 (vendor) | 37-140 | GPT-5.6 Luna (High), low confidence |
| 2 | `ornith:35b-q4_K_M` | TB 64.2 (vendor) ⚠ | 40-153 | GPT-5.5 (Low), low confidence |
| 3 | `qwen3.8:27b-nvfp4` | TB 65.2 ⚠ | 4-15 | GPT-5.5 (Low) |
| 4 | `qwen3.6:27b-q4_K_M` | TB 60.7 ⚠ | 4-16 | GPT-5.4 nano (Xhigh) |
| 5 | `flint:40b-a2b-qat-int4` | TB 54.9 (vendor) | 51-194 | Gemini 3.5 Flash-Lite, low confidence |

- **`qwen3.5:9b-nvfp4` is General \#5** (GS 33.3). It estimates 10-38 tok/s, faster than the dense 27B and 30B picks.
- **`flint:40b-a2b-qat-int4` (coding \#5) is a MoE model, so it's fast on every machine here**, unlike the dense coding picks.
- **Flint's score is its vendor's, for the full-precision model.** Recursive reports TB 54.9 for BF16 and 53.7 for its NVFP4 build [\[16\]](#ref-16); it publishes none for INT4, the format of Ollama's MLX build. Recursive's own MLX INT4 release is also about 22.6 GB [\[30\]](#ref-30); whether Ollama's tag holds the same weights isn't stated. Flint has no GGUF fallback on these Macs: its NVFP4 GGUF build is meant for NVIDIA GPUs [\[31\]](#ref-31), and llama.cpp's Metal backend, which Ollama 0.40.13 uses for GGUF on Macs, doesn't run NVFP4 weights [\[32\]](#ref-32); its `q4_1` build (26 GB) plus 64k of context doesn't fit 80% of a 32 GB Mac (estimate). Its weights plus 64k of context (24.5 GB, estimate) need the raised GPU memory limit ([section 3](#config-gpu-limit)).
- **Watch [\#19191](https://github.com/ollama/ollama/issues/19191) with Flint.** In the report, after one tool call with a whole-number argument (a timeout in milliseconds), later calls return that argument as a string, `"30000.0"`, and an agent that checks arguments against the tool's schema rejects every such call. The reporter traces it to Ollama's `flint` renderer, which writes earlier arguments back into the prompt as decimals. The ⚠ covers only tool-call parser bugs, so Flint isn't flagged, but the effect in an agent is the same. An Ollama collaborator has since opened a fix that says it fixes this report ([PR 19252](https://github.com/ollama/ollama/pull/19252), not merged as of 2026-11-02); an earlier fix from an outside contributor ([PR 19195](https://github.com/ollama/ollama/pull/19195)) is also open. Until a release ships the fix, test Flint in OpenCode before relying on it.
- **General: `qwen3.5:27b-int4` is \#1** (GS 41.8). This MLX build is 16 GB, smaller than the 17-18 GB of the other dense picks, so it's slightly faster, and it ranks above `qwen3.6:27b-q4_K_M` (GS 41.2) and `muse-glimmer:30b-nvfp4` (GS 42.4), which are within 3 points.
- **On LMArena, `gemma4:26b-nvfp4` rates as well as the top General picks** (1438 ±7; Muse 1425 ±10, close to it; `qwen3.5:27b` 1409 ±4, clearly lower), though its GS is lower [\[7\]](#ref-7). For writing and chat it's a strong choice, and it's the fast one.
- **`qwen3.6:27b` is listed as its GGUF build here.** Its MLX build `qwen3.6:27b-nvfp4` (19 GB) would estimate under 15 tok/s on every machine in this tier.
- **The dense 27B and 30B picks estimate 15+ tok/s only on the M5 Max, and `qwen3.5:27b-int4` also on the M4 Max.** Expect about 4-15 on the other chips.
- **Coding picks here assume the raised GPU memory limit** ([section 3](#config-gpu-limit)): each needs its weights plus 64k of context, 21-25 GB (estimate), within 80% of RAM. With that limit, the two Ornith 35B MoE models fit and lead coding on their vendor's scores [\[13\]](#ref-13). They and Flint are the fast options (37-194 tok/s).
- **Watch MLX builds on 32 GB Macs.** Two open reports, neither confirmed: [\#18131](https://github.com/ollama/ollama/issues/18131) (`qwen3.8:27b-mlx`, the same weights as `qwen3.8:27b-nvfp4`, swapping heavily during agent sessions because of MLX's prompt cache) and [\#18269](https://github.com/ollama/ollama/issues/18269) (`muse-glimmer:30b-mlx` getting stuck in "Stopping..." on a 32 GB Mac). If an MLX build swaps heavily or stalls, use the GGUF build of the same model instead: `qwen3.5:27b-q4_K_M`, `muse-glimmer:30b-q4_K_M`, `gemma4:26b-a4b-it-qat` or `qwen3.8:27b-q4_K_M`.
- **`gemma4:26b-nvfp4` is the fast option for General use** (29-111 tok/s), a MoE with 4B active.
- **`qwen3.8:27b-nvfp4` (GS 35.9, LMArena 1436 ±5) is \#6 for General**, within 3 points of `gemma4:26b-nvfp4` but much slower here.
- **Gemma 4 has at least fifteen open tool-call bug reports** ([\#18649](https://github.com/ollama/ollama/issues/18649), [\#18390](https://github.com/ollama/ollama/issues/18390), [\#18354](https://github.com/ollama/ollama/issues/18354), [\#17882](https://github.com/ollama/ollama/issues/17882), [\#18275](https://github.com/ollama/ollama/issues/18275), [\#15445](https://github.com/ollama/ollama/issues/15445), [\#15315](https://github.com/ollama/ollama/issues/15315), [\#18468](https://github.com/ollama/ollama/issues/18468), [\#15670](https://github.com/ollama/ollama/issues/15670), [\#17568](https://github.com/ollama/ollama/issues/17568), [\#18861](https://github.com/ollama/ollama/issues/18861), [\#15573](https://github.com/ollama/ollama/issues/15573), [\#15719](https://github.com/ollama/ollama/issues/15719), [\#19273](https://github.com/ollama/ollama/issues/19273), and [\#17562](https://github.com/ollama/ollama/issues/17562) in Cline). No Ollama member or collaborator has confirmed one. On [\#15315](https://github.com/ollama/ollama/issues/15315), an Ollama contributor reproduced it and their tool-call repair ([PR 15374](https://github.com/ollama/ollama/pull/15374)) was merged, but the issue is still open. Test Gemma 4 in OpenCode before relying on it.

------------------------------------------------------------------------

### Mac 48-96 GB: M1 Max / M2 Max / M3 Max / M4 Pro / M4 Max / M5 Pro / M5 Max {#tier-mac-48-96}

**Confidence:** General scores are from Artificial Analysis. Coding includes vendor-reported scores; see (vendor) in the table. All speeds are estimates, not measurements on these machines. Picks marked ⚠ have unresolved tool-call reports.

**General use**

| \# | Model | Score | Est. tok/s | Equivalent paid model | LMArena |
|:---|:---|:---|:---|:---|:---|
| 1 | `qwen3.5:27b-int4` | GS 41.8 | 10-23 | Claude Haiku 5.5 (Low) | 1409 ±4 |
| 2 | `qwen3.6:27b-nvfp4` | GS 41.2 | 9-20 | Claude Haiku 5.5 (Low) | — |
| 3 | `muse-glimmer:30b-nvfp4` | GS 42.4 | 9-21 | Claude Haiku 5.5 (Low) | 1425 ±10 |
| 4 | `qwen3.5:35b-a3b-nvfp4` | GS 38.0 | 87-196 | Gemini 3.5 Flash-Lite | 1394 ±4 |
| 5 | `qwen3.6:35b-a3b-nvfp4` | GS 38.7 | 83-186 | o3 | — |

**Agentic coding**

| \# | Model | Score | Est. tok/s | Equivalent paid model |
|:---|:---|:---|:---|:---|
| 1 | `ornith-1.5:35b` | TB 67.8 (vendor) | 83-187 | GPT-5.6 Luna (High), low confidence |
| 2 | `ornith:35b-q4_K_M` | TB 64.2 (vendor) ⚠ | 91-205 | GPT-5.5 (Low), low confidence |
| 3 | `qwen3.8:27b-nvfp4` | TB 65.2 ⚠ | 9-20 | GPT-5.5 (Low) |
| 4 | `qwen3.6:27b-nvfp4` | TB 60.7 ⚠ | 9-20 | GPT-5.4 nano (Xhigh) |
| 5 | `flint:40b-a2b-qat-int4` | TB 54.9 (vendor) | 115-260 | Gemini 3.5 Flash-Lite, low confidence |

- **Every Qwen, Muse and Flint pick here is an MLX build.** The Ornith 9B and 35B models have no MLX build.
- **`flint:40b-a2b-qat-int4` (coding \#5) is the fastest coding pick here.** Its score is the vendor's for the BF16 model; see the Mac 32-36 GB notes.
- **Use the extra memory for a 128k context window, not a bigger quantization.** A bigger quantization like `q8_0` or `mxfp8` is slower, and AA has no scores that show what it gains.
- **General: the dense 27B and 30B models lead** (GS 41.2-42.4), and the fast Qwen 35B MoE models are \#4 and \#5 (GS 38.0 and 38.7), more than 3 points below `muse-glimmer:30b-nvfp4`, so their speed doesn't lift them above it. `qwen3.5:27b-int4` (16 GB) is \#1 as the smallest dense build, within 3 points of the others.
- **`gemma4:31b-nvfp4` has the highest LMArena rating of any model in this report (1452 ±7) but is General \#6** (GS 39.0): within 3 points of the Qwen 35B models, which are much faster [\[7\]](#ref-7). If you mostly write or chat and can accept 8-19 tok/s, consider it.
- **`qwen3.6:27b-nvfp4` ranks above `muse-glimmer:30b-nvfp4` though its estimate is a little lower.** Ranking uses each model's fastest build, and Qwen's GGUF build (17 GB) is faster than both; within 10%, the MLX build is listed ([builds](#how-to-read-this)).
- **The MoE picks are the fast options:** the two Qwen 35B models for general use (83-196 tok/s), and the two Ornith 35B models and Flint for coding (83-260).
- **`nemotron-3.5-bolt:74b-a9b-iq2` isn't listed on Macs.** Ollama says the 74B doesn't run on Apple silicon yet [\[14\]](#ref-14); it's ranked on the Pro Max 16 Plus only ([summary](#summary)).
- **The two Ornith 35B models lead coding on their vendor's scores alone** [\[13\]](#ref-13). The vendor ran them on vLLM with an adjusted chat template, not on Ollama. `qwen3.8:27b-nvfp4` is the top pick with an independent score.
- **`ornith:35b-q4_K_M` ranks above `qwen3.8:27b-nvfp4`** because they're within 3 points and the MoE is much faster. It's flagged for [\#16992](https://github.com/ollama/ollama/issues/16992) (raw tool-call XML in Claude Code), which nobody at Ollama has confirmed.
- **`ornith-1.5:35b` isn't flagged.** Its open bug ([\#17957](https://github.com/ollama/ollama/issues/17957)) shows only when a request sets both tools and a JSON response format, which isn't normal agent use.
- **Two open reports concern `qwen3.6:35b-a3b` on MLX, neither confirmed:** [\#17426](https://github.com/ollama/ollama/issues/17426) (hangs while thinking on an M5 Pro, Ollama 0.32) and [\#15880](https://github.com/ollama/ollama/issues/15880) (thinking loop on an earlier build of `35b-a3b-nvfp4`; the tag has been rebuilt since, most recently on 2026-10-30, when it shrank to 23.1 GB [\[33\]](#ref-33)[\[18\]](#ref-18)). If it stalls, use `qwen3.6:35b-a3b-q4_K_M`.

------------------------------------------------------------------------

### Mac 128 GB: M3 Max / M4 Max / M5 Max {#tier-mac-128}

**Confidence:** General scores are from Artificial Analysis. Coding includes vendor-reported scores; see (vendor) in the table. All speeds are estimates, not measurements on these machines. Picks marked ⚠ have unresolved tool-call reports.

**General use**

| \# | Model | Score | Est. tok/s | Equivalent paid model | LMArena |
|:---|:---|:---|:---|:---|:---|
| 1 | `qwen3.8-flash-next:125b-a6b-nvfp4` | GS 51.9 | 67-103 | Claude Sonnet 5.5 (Medium, Default Fallback) | — |
| 2 | `qwen3.5:122b-a10b-q4_K_M` | GS 42.3 | 36-55 | Claude Haiku 5.5 (Low) | 1416 ±4 |
| 3 | `nemotron-3.5-super:120b-a12b-nvfp4` | GS 43.5 | 30-46 | GPT-6 Luna (Medium) | 1412 ±9 |
| 4 | `qwen3.5:27b-int4` | GS 41.8 | 15-23 | Claude Haiku 5.5 (Low) | 1409 ±4 |
| 5 | `qwen3.6:27b-nvfp4` | GS 41.2 | 13-20 | Claude Haiku 5.5 (Low) | — |

**Agentic coding**

| \# | Model | Score | Est. tok/s | Equivalent paid model |
|:---|:---|:---|:---|:---|
| 1 | `qwen3.8-flash-next:125b-a6b-nvfp4` | TB 86.1 ⚠ | 67-103 | Claude Fable 5.1 (Low, Default Fallback) |
| 2 | `ornith-1.5:35b` | TB 67.8 (vendor) | 122-187 | GPT-5.6 Luna (High), low confidence |
| 3 | `ornith:35b-q4_K_M` | TB 64.2 (vendor) ⚠ | 133-205 | GPT-5.5 (Low), low confidence |
| 4 | `nemotron-3.5-super:120b-a12b-q4_K_M` | TB 66.7 (vendor) | 27-41 | GPT-5.5 (Low), low confidence |
| 5 | `qwen3.8:27b-nvfp4` | TB 65.2 ⚠ | 13-20 | GPT-5.5 (Low) |

- **`qwen3.8-flash-next:125b-a6b-nvfp4` is \#1 for both use cases** (GS 51.9, TB 86.1) [\[4\]](#ref-4). LMArena hasn't rated it.
  - At 105 GB it fits under the 16 GB-reserve rule, but only after you raise the GPU memory limit ([section 3](#config-gpu-limit)).
  - It's an MLX build; its GGUF tag (120 GB) doesn't fit.
  - Watch [\#17778](https://github.com/ollama/ollama/issues/17778): `qwen3.8` models return HTTP 500 "no user query found in messages", mostly when the conversation overflows the context; some users also see it on tool-call turns. An Ollama collaborator points to Ollama's server-side message pruning and suggests a larger context as the workaround. A fix from an outside contributor ([PR 17894](https://github.com/ollama/ollama/pull/17894)) is open, and an Ollama collaborator has opened [PR 19058](https://github.com/ollama/ollama/pull/19058) to keep the last user message when Ollama trims a long conversation; it isn't linked to the issue.
- **`nemotron-3.5-super` uses a different build for each use case.**
  - General (\#3): the MLX build `120b-a12b-nvfp4` (80 GB) is smaller and faster than the GGUF build (90 GB); GS 43.5 is AA's score for the model [\[4\]](#ref-4). `qwen3.5:122b-a10b-q4_K_M` (GS 42.3) ranks above it because they're within 3 points and the Qwen model is faster. It ships no sampling settings; see [section 2](#config-context).
  - Coding: NVIDIA reports TB 60.8 for the NVFP4 build and 66.7 for the full BF16 model [\[34\]](#ref-34), run with Terminus 2, AA's agent [\[35\]](#ref-35). AA hasn't scored its Terminal-Bench. The 5.9-point gap is more than the 3 points that speed can make up, so coding lists `120b-a12b-q4_K_M` with NVIDIA's BF16 score. At 90 GB it's close to the default GPU memory cap ([section 3](#config-gpu-limit)), and it needs Ollama 0.40.5 or later [\[2\]](#ref-2).
- **`ornith-1.5:122b-nvfp4` is no longer ranked for coding.** Its card reports TB 81.2, but its footnote describes only a Claude Code run of Terminal-Bench 2.1, not Terminus 2, the agent AA uses [\[5\]](#ref-5). Ornith's own page shows the two agents giving different scores for the same model [\[13\]](#ref-13). It's a 122B MoE (73.4 GB as MLX), added to Ollama on 2026-10-20 [\[36\]](#ref-36), and it has no AA score. `qwen3.8:27b-nvfp4` (TB 65.2) takes coding \#5.
- **The two Ornith 35B models still rank high in coding on vendor scores only**; see the Mac 48-96 GB notes.
- **Other large models fit but don't make the top 5:** `qwen3.6:27b-nvfp4`, `flint`, `nemotron-3-super`, `gpt-oss:120b` and `qwen3.5:122b-a10b` in coding. In General, `muse-glimmer:30b-nvfp4` (GS 42.4) is \#6 and the fast Qwen 35B MoE models \#7 and \#8 (GS 38.0 and 38.7) [\[4\]](#ref-4). `mistral-medium-3.5` and `devstral-2` fit but estimate about 3-5 tok/s.

------------------------------------------------------------------------

### Dell Latitude 7350, 16 GB (Core Ultra U, Intel Graphics, no discrete GPU) {#tier-latitude}

**Confidence:** General scores are from Artificial Analysis. Coding scores are from Artificial Analysis. All speeds are estimates, not measurements on these machines. Picks marked ⚠ have unresolved tool-call reports.

**General use**

| \# | Model | Score | Est. tok/s | Equivalent paid model | LMArena |
|:---|:---|:---|:---|:---|:---|
| 1 | `qwen3.5:4b-q4_K_M` | GS 27.6 | ~19 | GPT-5.6 Terra (Non-reasoning) | — |
| 2 | `qwen3:4b-thinking-2507-q4_K_M` | GS 16.6 | ~24 | GPT-6 Luna (Non-reasoning) | — |
| 3 | `granite4.2:3b-q4_K_M` | GS 12.5 | ~28 | GPT-5.4 nano (Non-reasoning) | 1290 ±12 |
| 4 | `qwen3.5:2b-q4_K_M` | GS 8.7 | ~32 | GPT-5 nano (Minimal) | — |
| 5 | `nemotron-3-nano:4b-q4_K_M` | GS 10.5 | ~22 | Grok 4 Fast (Non-reasoning) | — |

**Agentic coding**

| \# | Model | Score | Est. tok/s | Equivalent paid model |
|:---|:---|:---|:---|:---|
| 1 | `qwen3.5:4b-q4_K_M` | TB 25.8 ⚠ | ~19 | Gemini 2.5 Pro |

- **Agentic coding is weak here.** `qwen3.5:4b-q4_K_M` is the only model that passes both the TB 20 floor and the speed filter (≈ Gemini 2.5 Pro). Consider a cloud model for serious coding work.
- **`qwen3.5:4b-q4_K_M` is \#1 for General** (GS 27.6), more than 10 points ahead of the rest. Picks 2-5 score GS 8.7-16.6.
- **New: `nemotron-3-nano:4b-q4_K_M` is General \#5** (GS 10.5), replacing `qwen3:4b-instruct-2507-q4_K_M`.
- Ollama runs the Intel iGPU through Vulkan, which is on by default when the backend is installed [\[37\]](#ref-37). Ollama's docs don't state Intel iGPU support on Windows (unverified).

------------------------------------------------------------------------

### Windows 32 GB: Dell Pro 14 Premium PA14250/PA14260 (no discrete GPU) · Dell Pro Max 16 MC16250 with RTX PRO 500 (6 GB), 1000 or 2000 (8 GB) · Dell Pro Precision 5 16 PW516261, integrated or RTX PRO 500/1000/2000 {#tier-win-32}

**Confidence:** General scores are from Artificial Analysis. Coding scores are from Artificial Analysis. All speeds are estimates, not measurements on these machines. Picks marked ⚠ have unresolved tool-call reports.

**General use**

| \# | Model | Score | Est. tok/s | Equivalent paid model | LMArena |
|:---|:---|:---|:---|:---|:---|
| 1 | `gemma4:26b-a4b-it-qat` | GS 34.8 | 22-33 | GPT-6.1 Terra (Non-reasoning) | 1438 ±7 |
| 2 | `qwen3:30b-a3b-thinking-2507-q4_K_M` | GS 27.3 | 28-43 | GPT-5.6 Terra (Non-reasoning) | — |
| 3 | `qwen3.5:4b-q4_K_M` | GS 27.6 | 16-70 | GPT-5.6 Terra (Non-reasoning) | — |
| 4 | `north-mini-code-1.0:q4_K_M` | GS 19.8 | 28-43 | GPT-6 Luna (Non-reasoning) | — |
| 5 | `gpt-oss:20b` | GS 18.9 | 22-34 | GPT-6 Luna (Non-reasoning) | 1317 ±6 |

**Agentic coding**

| \# | Model | Score | Est. tok/s | Equivalent paid model |
|:---|:---|:---|:---|:---|
| 1 | `gemma4:26b-a4b-it-qat` | TB 39.0 ⚠ | 22-33 | GPT-5.6 Luna (Non-reasoning) |
| 2 | `north-mini-code-1.0:q4_K_M` | TB 35.6 ⚠ | 28-43 | GPT-5.5 Instant (June 2026) |
| 3 | `qwen3.5:4b-q4_K_M` | TB 25.8 ⚠ | 16-70 | Gemini 2.5 Pro |

- **`gemma4:26b-a4b-it-qat` is \#1 for both use cases** (GS 34.8, TB 39.0), and it also rates highest of these picks on LMArena (1438 ±7) [\[7\]](#ref-7).
- **`north-mini-code-1.0:q4_K_M` (\#4) and `gpt-oss:20b` (\#5) are the other General picks**; the Granite 4.2 models are \#6 and \#8. `gpt-oss:20b` is OpenAI's 21B MoE with 3.6B active [\[38\]](#ref-38), in 4-bit MXFP4 (14 GB) [\[18\]](#ref-18); its open tool-call reports matter only for coding, where it scores below the TB 20 floor.
- **Larger MoE models don't leave room for context here.** `qwen3.5:35b-a3b-q4_K_M` (22 GB) and `ornith:35b-q4_K_M` (21 GB) fit only by their weights, with no room left for even Ollama's default 4k context (General) or OpenCode's 64k (coding) once 10 GB is kept for Windows and apps (estimate). `qwen3:30b-a3b-thinking-2507-q4_K_M` (19 GB) has room for a 16k context in General use ([section 2](#config-context)). `flint:40b-a2b-gguf-nvfp4` (23 GB) is over the 22 GB budget, so Flint isn't ranked here.
- **Dense 27B models estimate only 3-5 tok/s here.**
- **On the Pro Max 16 and Pro Precision 5 16, only `qwen3.5:4b-q4_K_M` fits in VRAM, and only on the 8 GB cards.** Every other pick runs from system RAM.
- **`gemma4:26b-a4b-it-qat` carries an unconfirmed report that it fails inside a coding agent** ([\#17562](https://github.com/ollama/ollama/issues/17562) in Cline).
- **The Dell Pro Precision 5 Series 16 (PW516261) is in this tier**, with 32 GB of LPDDR5x at 8533 MT/s and integrated graphics or an RTX PRO 500, 1000 or 2000 [\[39\]](#ref-39). Its faster memory (~137 GB/s, estimate assuming a 128-bit bus) gives it the top of each speed range, like the Pro 14 Premium. Whether it is the planned MC16260 isn't confirmed by Dell.
- **All three coding picks are flagged.** Test your choice in OpenCode before relying on it; `north-mini-code-1.0:q4_K_M` is a coding MoE model trained on OpenCode and three other agent harnesses [\[40\]](#ref-40).

------------------------------------------------------------------------

### Dell Pro Max 16 Plus MB16250, 64 GB, with RTX PRO 1000 or 2000 (8 GB), 3000 (12 GB) or 4000 (16 GB) {#tier-pm16p-8-16}

**Confidence:** General scores are from Artificial Analysis. Coding includes vendor-reported scores; see (vendor) in the table. All speeds are estimates, not measurements on these machines. Picks marked ⚠ have unresolved tool-call reports.

**General use**

| \# | Model | Score | Est. tok/s | Equivalent paid model | LMArena |
|:---|:---|:---|:---|:---|:---|
| 1 | `qwen3.5:35b-a3b-q4_K_M` | GS 38.0 | 32-37 | Gemini 3.5 Flash-Lite | 1394 ±4 |
| 2 | `qwen3.6:35b-a3b-q4_K_M` | GS 38.7 | 30-34 | o3 | — |
| 3 | `nemotron-3.5-bolt:74b-a9b-iq2` | GS 39.7 | 20-23 | o3 | — |
| 4 | `gemma4:26b-a4b-it-qat` | GS 34.8 | 25-28 | GPT-6.1 Terra (Non-reasoning) | 1438 ±7 |
| 5 | `qwen3.5:9b-q4_K_M` | GS 33.3 | 9-81 | GPT-5.4 nano (Medium) | — |

**Agentic coding**

| \# | Model | Score | Est. tok/s | Equivalent paid model |
|:---|:---|:---|:---|:---|
| 1 | `ornith-1.5:35b` | TB 67.8 (vendor) | 31-35 | GPT-5.6 Luna (High), low confidence |
| 2 | `ornith:35b-q4_K_M` | TB 64.2 (vendor) ⚠ | 34-38 | GPT-5.5 (Low), low confidence |
| 3 | `flint:40b-a2b-gguf-nvfp4` | TB 53.7 (vendor) | 42-48 | Gemini 3.5 Flash-Lite, low confidence |
| 4 | `qwen3.6:35b-a3b-q4_K_M` | TB 44.9 ⚠ | 30-34 | Claude 4.5 Haiku (Reasoning) |
| 5 | `ornith-1.5:9b` | TB 46.2 (vendor) | 9-81 | Claude 4.5 Haiku (Reasoning), low confidence |

- **General: `qwen3.5:35b-a3b-q4_K_M` is \#1** (GS 38.0), ahead of `qwen3.6:35b-a3b-q4_K_M` (GS 38.7) because they're within 3 points and it's slightly faster.
- **`nemotron-3.5-bolt:74b-a9b-iq2` is General \#3, and no longer ranked for coding.** It scores highest for General here (GS 39.7), but both Qwen 35B models are within 3 points and faster. Its GS is AA's score for the full-precision weights ([summary](#summary)). NVIDIA's TB 51.0 for this 2-bit build no longer counts: the card doesn't say which agent ran it [\[6\]](#ref-6), and AA hasn't scored Bolt's Terminal-Bench. At 25 GB it runs split between the GPU and system RAM on every GPU here; with 9B active it's the slowest General pick (estimate).
- **The 35B, 74B and 26B General picks run split between the GPU and system RAM**, so RAM bandwidth sets their speeds.
- **New: `qwen3.5:9b-q4_K_M` is General \#5** (GS 33.3), replacing `qwen3-next:80b-a3b-thinking-q4_K_M` (now \#6). It fits in VRAM on the 12 and 16 GB GPUs, where it's the fastest pick (up to 81 tok/s, estimate), but runs from RAM on the 8 GB GPUs (about 9 tok/s).
- **`flint:40b-a2b-gguf-nvfp4` is coding \#3** (TB 53.7, vendor) and the fastest coding pick on the 8 GB GPUs. It runs split between the GPU and system RAM on every GPU in this tier; as a MoE with about 2.5B active it still estimates 42-48 tok/s. See the Mac 32-36 GB notes for [\#19191](https://github.com/ollama/ollama/issues/19191).
- **`ornith-1.5:9b` returns as coding \#5**, replacing Bolt. It fits in VRAM on the 12 and 16 GB GPUs but runs from RAM on the 8 GB GPUs (about 9 tok/s, estimate). It ranks below `qwen3.6:35b-a3b-q4_K_M` (TB 44.9) because they're within 3 points and the Qwen MoE is faster on the slowest machine.
- **Four of the five coding picks are ranked on vendor scores** (the three Ornith models and Flint), all run with Terminus 2, AA's agent [\[13\]](#ref-13)[\[16\]](#ref-16). `qwen3.6:35b-a3b-q4_K_M` is the only one with an independent score.

------------------------------------------------------------------------

### Dell Pro Max 16 Plus MB16250, 64 GB, with RTX PRO 5000 (24 GB) {#tier-pm16p-24}

**Confidence:** General scores are from Artificial Analysis. Coding includes vendor-reported scores; see (vendor) in the table. All speeds are estimates, not measurements on these machines. Picks marked ⚠ have unresolved tool-call reports.

**General use**

| \# | Model | Score | Est. tok/s | Equivalent paid model | LMArena |
|:---|:---|:---|:---|:---|:---|
| 1 | `qwen3.5:27b-q4_K_M` | GS 41.8 | ~32 | Claude Haiku 5.5 (Low) | 1409 ±4 |
| 2 | `qwen3.6:27b-q4_K_M` | GS 41.2 | ~32 | Claude Haiku 5.5 (Low) | — |
| 3 | `muse-glimmer:30b-q4_K_M` | GS 42.4 | ~30 | Claude Haiku 5.5 (Low) | 1425 ±10 |
| 4 | `qwen3.5:35b-a3b-q4_K_M` | GS 38.0 | 32-37 | Gemini 3.5 Flash-Lite | 1394 ±4 |
| 5 | `qwen3.6:35b-a3b-q4_K_M` | GS 38.7 | 30-34 | o3 | — |

**Agentic coding**

| \# | Model | Score | Est. tok/s | Equivalent paid model |
|:---|:---|:---|:---|:---|
| 1 | `ornith-1.5:35b` | TB 67.8 (vendor) | 31-35 | GPT-5.6 Luna (High), low confidence |
| 2 | `ornith:35b-q4_K_M` | TB 64.2 (vendor) ⚠ | ~299 | GPT-5.5 (Low), low confidence |
| 3 | `qwen3.8:27b-q4_K_M` | TB 65.2 ⚠ | ~30 | GPT-5.5 (Low) |
| 4 | `qwen3.6:27b-q4_K_M` | TB 60.7 ⚠ | ~32 | GPT-5.4 nano (Xhigh) |
| 5 | `flint:40b-a2b-gguf-nvfp4` | TB 53.7 (vendor) | 42-48 | Gemini 3.5 Flash-Lite, low confidence |

- **This is the best Windows machine for local models.** Five of the nine models picked here fit in the 24 GB of VRAM, which runs at 896 GB/s [\[26\]](#ref-26). `qwen3.5:35b-a3b-q4_K_M` (22 GB), `qwen3.6:35b-a3b-q4_K_M` (24 GB), `ornith-1.5:35b` (23 GB) and `flint:40b-a2b-gguf-nvfp4` (23 GB) are over the VRAM-minus-3 GB limit, so they run split and are estimated from system RAM.
- **`nemotron-3.5-bolt:74b-a9b-iq2` is General \#7** (GS 39.7): within 3 points of the picks above it, which are faster. It's no longer ranked for coding (see the 8-16 GB GPU notes). `gemma4:31b-it-qat` (\#6, GS 39.0) has the highest LMArena rating of any model here (1452 ±7) [\[7\]](#ref-7).
- **`flint:40b-a2b-gguf-nvfp4` is coding \#5**, above `muse-glimmer:30b-q4_K_M` (TB 51.7). The two are within 3 points, and Flint is faster even running split.
- **General: `qwen3.5:27b-q4_K_M` is \#1** (GS 41.8). The three dense picks are within 3 points of each other and all fit in VRAM; the Qwen builds are slightly smaller than Muse's, so faster.
- **The two Ornith 35B models lead coding on vendor scores alone**; see the Mac 48-96 GB notes. `ornith:35b-q4_K_M` (21 GB) fits in VRAM here, hence ~299 tok/s. `qwen3.8:27b-q4_K_M` is the top pick with an independent score.
- **Watch [\#18840](https://github.com/ollama/ollama/issues/18840) on this machine.** It reports `qwen3.8:27b` on Windows with Ollama 0.40.0 returning HTTP 500 from `/api/chat` on a large request with tools. OpenCode uses `/v1` instead; whether that path is affected isn't reported.
- **Also watch [\#19439](https://github.com/ollama/ollama/issues/19439).** It reports Ollama 0.40.13's model process crashing with HTTP 500 during tool calls on Windows with an RTX 5090, with `muse-glimmer:30b` and `qwen3.5:27b`. It's unconfirmed: an Ollama collaborator asked for logs, which the reporter posted on 2026-11-01.

------------------------------------------------------------------------

## Model reference

GGUF tag sizes are from each model's tags page [\[33\]](#ref-33). MLX tag sizes are the sum of the layer sizes in the registry manifest, to one decimal [\[18\]](#ref-18); the tags page rounds them. MLX builds are marked (MLX); the tier tables show which build each tier uses. Issues marked "MLX" affect only the MLX build; every MLX build also shares the open MLX reports in [Watched issues](#watched-issues). Licenses are from the Hugging Face model cards [\[41\]](#ref-41) unless noted.

| Model (tags) | Params | Size | License · origin | Known Ollama issues |
|:---|:---|:---|:---|:---|
| `qwen3.8:27b-nvfp4` (MLX) · `qwen3.8:27b-q4_K_M` | 27B dense | 18.2 GB · 18 GB | Apache-2.0 · Alibaba [\[42\]](#ref-42) | Qwen parser note below; [\#17765](https://github.com/ollama/ollama/issues/17765) (image tag dropped with tools); [\#18840](https://github.com/ollama/ollama/issues/18840) (HTTP 500 on Windows, 0.40.0); [\#17778](https://github.com/ollama/ollama/issues/17778) (HTTP 500 "no user query found", mostly when the conversation overflows context); MLX: [\#18131](https://github.com/ollama/ollama/issues/18131) (heavy swap on a 32 GB Mac in agent sessions), [\#19353](https://github.com/ollama/ollama/issues/19353) (no `tool_calls` when the model writes text first, on `27b-mlx`; an Ollama collaborator's own run returned both, so not counted) |
| `qwen3.6:27b-nvfp4` (MLX) · `qwen3.6:27b-q4_K_M` | 27B dense | 18.8 GB · 17 GB | Apache-2.0 · Alibaba | Qwen parser note below |
| `qwen3.6:35b-a3b-nvfp4` (MLX) · `qwen3.6:35b-a3b-q4_K_M` | 35B MoE, 3B active | 23.1 GB · 24 GB | Apache-2.0 · Alibaba | Qwen parser note below; [\#17197](https://github.com/ollama/ollama/issues/17197) (default `presence_penalty` suits general use, not coding; see config); MLX: [\#17426](https://github.com/ollama/ollama/issues/17426) (hangs while thinking, M5 Pro, Ollama 0.32), [\#15880](https://github.com/ollama/ollama/issues/15880) (thinking loop on an earlier build). None confirmed |
| `qwen3.5:27b-int4` (MLX) · `qwen3.5:27b-q4_K_M` | 27B dense | 16.1 GB · 17 GB | Apache-2.0 · Alibaba | Qwen parser note below; [\#19439](https://github.com/ollama/ollama/issues/19439) (model process crashes with HTTP 500 during tool calls on Windows with an RTX 5090, Ollama 0.40.13; also reported with `muse-glimmer:30b`; unconfirmed) |
| `qwen3.5:35b-a3b-nvfp4` (MLX) · `qwen3.5:35b-a3b-q4_K_M` | 35B MoE, 3B active | 21.9 GB · 22 GB | Apache-2.0 · Alibaba | Qwen parser note below |
| `qwen3.5:9b-nvfp4` (MLX) · `qwen3.5:9b-q4_K_M` | 9B dense | 7.2 GB · 6.6 GB | Apache-2.0 · Alibaba | Qwen parser note below; [\#14986](https://github.com/ollama/ollama/issues/14986) (500 from `/api/generate` with tool-call XML in the prompt; not the tools API) |
| `qwen3.5:4b-q4_K_M` · `qwen3.5:4b-nvfp4` (MLX) | 4B dense | 3.3 GB · 4.0 GB | Apache-2.0 · Alibaba | Qwen parser note below |
| `qwen3.5:2b-q4_K_M` · `qwen3.5:2b-nvfp4` (MLX) | 2B dense | 1.9 GB · 2.5 GB | Apache-2.0 · Alibaba | Qwen parser note below |
| `muse-glimmer:30b-nvfp4` (MLX) · `muse-glimmer:30b-q4_K_M` | 30B dense [\[13\]](#ref-13) | 17.3 GB · 18 GB | Apache-2.0 · Meta (license from the Ollama page) | [\#17656](https://github.com/ollama/ollama/issues/17656) (wrong weights), [\#18269](https://github.com/ollama/ollama/issues/18269) (stuck "Stopping..." on a 32 GB Mac) are reported on the `30b-mlx` tag (19.1 GB), which holds the `30b-nvfp4` weights plus a draft model [\[18\]](#ref-18); whether they affect `30b-nvfp4` isn't reported. [\#19439](https://github.com/ollama/ollama/issues/19439) (HTTP 500 crash during tool calls on Windows, Ollama 0.40.13; unconfirmed) |
| `gemma4:26b-nvfp4` (MLX) · `gemma4:26b-a4b-it-qat` | 26B MoE, 4B active (25.2B total, 3.8B active on the same page) [\[43\]](#ref-43) | 16.1 GB · 16 GB | Apache-2.0 · Google | **Drops tool calls** ([\#18649](https://github.com/ollama/ollama/issues/18649), [\#18390](https://github.com/ollama/ollama/issues/18390), [\#18354](https://github.com/ollama/ollama/issues/18354), [\#17882](https://github.com/ollama/ollama/issues/17882), [\#19273](https://github.com/ollama/ollama/issues/19273)); [\#17562](https://github.com/ollama/ollama/issues/17562) (fails in Cline). None confirmed. MLX: [\#19268](https://github.com/ollama/ollama/issues/19268) (`stop` sequences ignored on `26b-nvfp4`; not tool calls) |
| `gemma4:12b-nvfp4` (MLX) · `gemma4:12b-it-qat` | 12B dense | 7.7 GB · 7.2 GB | Apache-2.0 · Google | Same `gemma4` parser bugs; [\#16562](https://github.com/ollama/ollama/issues/16562) (reported "basically unusable" on Apple silicon); MLX: [\#17362](https://github.com/ollama/ollama/issues/17362) (`12b-mlx`, the same weights, slower than `26b-mlx`; unconfirmed) |
| `north-mini-code-1.0:q4_K_M` · `north-mini-code-1.0:mlx-nvfp4` (MLX) | 30B MoE, 3B active | 19 GB · 19.7 GB | Apache-2.0 + Cohere use policy · Cohere [\[40\]](#ref-40) | Uses the `cohere` parser: [\#18053](https://github.com/ollama/ollama/issues/18053) (tool call returned as text on GGUF tags) |
| `qwen3:4b-thinking-2507-q4_K_M` | 4B dense | 2.5 GB | Apache-2.0 · Alibaba (license from the Ollama page) | [\#12561](https://github.com/ollama/ollama/issues/12561) (earlier thinking text left out of the prompt; not tool calls) |
| `ornith:9b-q4_K_M` | 9B dense | 5.6 GB | MIT · DeepReinforce [\[44\]](#ref-44) | [\#16992](https://github.com/ollama/ollama/issues/16992) (on `ornith:35b-q4_K_M`: parser leaks raw tool-call XML) |
| `ornith:35b-q4_K_M` | 35B MoE, 3B active [\[13\]](#ref-13) | 21 GB | MIT (license file in the Ollama tag [\[18\]](#ref-18)) · DeepReinforce | [\#16992](https://github.com/ollama/ollama/issues/16992) (parser leaks raw tool-call XML in Claude Code; unconfirmed) |
| `ornith-1.5:35b` | 35B MoE, 3B active; reads images [\[36\]](#ref-36) | 23 GB | License unsourced · Ornith Team [\[13\]](#ref-13) | No Ollama parser. [\#17957](https://github.com/ollama/ollama/issues/17957) (fails when a request sets both tools and a JSON response format; not normal agent use, so not flagged) |
| `ornith-1.5:9b` | 9B dense; reads images [\[36\]](#ref-36) | 6.6 GB | License unsourced · Ornith Team [\[13\]](#ref-13) | No Ollama parser. [\#17957](https://github.com/ollama/ollama/issues/17957) is reported on the 35B only; the fix ([PR 17965](https://github.com/ollama/ollama/pull/17965)) covers `qwen35`-architecture models without a parser, which includes the 9B |
| `flint:40b-a2b-qat-int4` (MLX) · `flint:40b-a2b-gguf-nvfp4` · `flint:40b-a2b-q4_1` | 39.8B MoE, about 2.5B active [\[16\]](#ref-16) | 22.6 GB · 23 GB · 26 GB | Apache-2.0 · Recursive [\[16\]](#ref-16) | Uses Ollama's `flint` parser. [\#19191](https://github.com/ollama/ollama/issues/19191) (integer tool-call arguments from earlier turns come back as strings such as `"30000.0"`, so clients that check arguments against the tool schema reject the call; reported on `/v1/chat/completions` with the MLX tag on 0.40.8; an Ollama collaborator's fix, [PR 19252](https://github.com/ollama/ollama/pull/19252), is open; in the `flint` renderer, which the GGUF tags also use [\[18\]](#ref-18), not the parser, so no flag). The GGUF tags need Ollama 0.40.9 [\[18\]](#ref-18); vendor TB 53.7 applies to `gguf-nvfp4` only [\[16\]](#ref-16), which is for NVIDIA GPUs, not Macs [\[31\]](#ref-31) |
| `granite4.2:3b-q4_K_M` | 3B dense | 2.2 GB | Apache-2.0 · IBM (license from the model file) [\[28\]](#ref-28) | [\#16505](https://github.com/ollama/ollama/issues/16505) (Granite speed regression since Ollama 0.30; not tool calls) |
| `qwen3.8-flash-next:125b-a6b-nvfp4` (MLX) · `125b-a6b-q4_K_M` | 125B MoE, 6B active, plus a 51B n-gram embedding table; speed is estimated over all 176B [\[45\]](#ref-45) | 104.9 GB · 120 GB | Qwen Community License 1.0 per the Ollama page [\[45\]](#ref-45); the `-nvfp4` tag's license file is Apache 2.0 and the `-q4_K_M` tag's is the Qwen Community License 1.0 [\[18\]](#ref-18) · Alibaba | Qwen parser note below; [\#17778](https://github.com/ollama/ollama/issues/17778) (HTTP 500 "no user query found", mostly when the conversation overflows context) |
| `granite4.2:8b-q4_K_M` | 8B dense | 5.3 GB | Apache-2.0 · IBM (license from the model file) [\[28\]](#ref-28) | [\#16505](https://github.com/ollama/ollama/issues/16505) (Granite speed regression since Ollama 0.30; not tool calls) |
| `minicpm-v4.6:q4_K_M` | About 1.2B: SigLIP2-400M vision encoder plus Qwen3.5-0.8B [\[29\]](#ref-29) | 1.6 GB | Apache-2.0 · OpenBMB [\[29\]](#ref-29) | No Ollama parser; tool calls go through its chat template [\[18\]](#ref-18). Not checked for tool-call bugs (general pick only) |
| `granite4:1b-h-q8_0` | 1B (from the tag name) | 1.6 GB | Apache-2.0 · IBM [\[46\]](#ref-46) | [\#12692](https://github.com/ollama/ollama/issues/12692) (wrong memory estimate for Granite 4 hybrid models), [\#16505](https://github.com/ollama/ollama/issues/16505) (Granite speed regression); neither is about tool calls |
| `nemotron-3-nano:4b-nvfp4` (MLX) · `nemotron-3-nano:4b-q4_K_M` | 4B; hybrid Mamba-2/Transformer (model config) [\[18\]](#ref-18) | 2.9 GB · 2.8 GB | NVIDIA Open Model License · NVIDIA (license from the model file) [\[18\]](#ref-18) | Uses the `nemotron-3-nano` parser; not checked for tool-call bugs (general pick only) |
| `gpt-oss:20b` | 21B MoE, 3.6B active [\[38\]](#ref-38); MXFP4 [\[18\]](#ref-18) | 14 GB | Apache-2.0 · OpenAI [\[38\]](#ref-38) | Open tool-call reports ([\#11991](https://github.com/ollama/ollama/issues/11991), [\#12203](https://github.com/ollama/ollama/issues/12203), [\#17638](https://github.com/ollama/ollama/issues/17638)); General pick only, so no flag |
| `qwen3:30b-a3b-thinking-2507-q4_K_M` | 30B MoE, 3B active (from the tag name) | 19 GB | Apache-2.0 · Alibaba (license from the model file) | Not checked for tool-call bugs (general pick only) |
| `qwen3.5:122b-a10b-q4_K_M` | 122B MoE, 10B active (from the tag name) | 81 GB | Apache-2.0 · Alibaba (license from the model file) | Qwen parser note below |
| `nemotron-3.5-bolt:74b-a9b-iq2` (Windows only) | 74B MoE, 9B active; hybrid Mamba-2/Transformer; reads images [\[14\]](#ref-14) | 25 GB | OpenMDW 1.1 · NVIDIA [\[6\]](#ref-6) | Uses the `nemotron-3-nano` parser, like `nemotron-3.5-super` [\[18\]](#ref-18). Not supported on Apple silicon [\[14\]](#ref-14); [\#19057](https://github.com/ollama/ollama/issues/19057) reports it crashing on Macs on any tool call; an open Ollama PR would add MLX support for it ([PR 19229](https://github.com/ollama/ollama/pull/19229)). The tag also carries a speculative-decoding draft model; the speed estimate can't model its gain [\[18\]](#ref-18). `74b-a9b` and `latest` are the same build |
| `nemotron-3.5-super:120b-a12b-nvfp4` (MLX, General) · `120b-a12b-q4_K_M` (coding) | 120B MoE, 12B active; hybrid Mamba-2/Transformer; reads images [\[47\]](#ref-47) | 79.6 GB · 90 GB | OpenMDW 1.1 · NVIDIA [\[47\]](#ref-47) | Uses the `nemotron-3-nano` parser; none open |

**Qwen parser note:** Qwen 3.5, 3.6 and 3.8 all use Ollama's `qwen3.5` tool-call parser [\[18\]](#ref-18). It has an open issue that breaks tool calls ([\#16383](https://github.com/ollama/ollama/issues/16383): strict parsing returns 500), so all three are flagged for coding.

**Considered and left out:**

| Model | Reason |
|:---|:---|
| `qwen3` (except `4b-thinking-2507`, `4b-instruct-2507` and `30b-a3b-thinking-2507`), `qwen3-vl`, `qwen3.5:0.8b`, `granite4` (except `1b-h`), `granite4.1`, `granite4.2:30b`, `glm-4.7-flash`, `qwen3-coder-next`, `devstral-small-2`, `ministral-3`, `olmo-3`, `olmo-3.1`, `nemotron-3-nano` (except `4b`), `nemotron-cascade-2`, `nemotron-3.5-lightning`, `lfm2.5:8b` | Evaluated; outranked in every tier |
| `lfm2`, `qwen3:0.6b`, `qwen3:1.7b`, `granite4:350m`, `gemma3n` | Context window below 64k (32k or 40k on their tags pages) [\[33\]](#ref-33) |
| `lfm2.5-thinking` | Sources conflict on context: its tags page lists 125k, but the model description on the same page says 32,768 tokens [\[48\]](#ref-48). Left out to be safe; it would rank \#6 or lower anyway |
| `laguna-xs.2`, `rnj-1` | No AA score; can't be ranked |
| `lfm3` (1.7B) | No AA score, so no General score. Liquid's Terminal-Bench 2.1 score is 12.9, below the TB 20 coding floor, and Liquid doesn't recommend it for agentic coding [\[8\]](#ref-8)[\[9\]](#ref-9). Needs Ollama 0.40.12 (Macs) or 0.40.13 (Windows) [\[2\]](#ref-2) |
| `lfm3-vl`, `lfm3-audio`, `lfm3-omni` (2B) | Image, speech and image-plus-audio versions of LFM3; no AA score and no vendor Terminal-Bench score. |
| `nemotron3:33b` | Nemotron 3 Nano Omni (TB 6.7); outranked |
| `gpt-oss-safeguard`, `granite4.1-guardian`, `functiongemma`, `glm-ocr`, `embeddinggemma-2`, `phonon` (speech) | Not general chat or coding models |
| `gemma3`, `medgemma`, `medgemma1.5`, `translategemma`, `deepseek-ocr` | No tool support in Ollama: no `tools` badge, and no tool handling in the model's chat template |
| `minicpm-v4.5` | Context window below 64k (40k in its model file) |
| `-mxfp8`, `-int8` and `-mlx-bf16` tags | 8-bit and 16-bit MLX builds. Every model here with an MLX build also has a 4-bit one, which is smaller and faster [\[18\]](#ref-18) |
| `-mlx` tags | Mostly the same weights as the `-nvfp4` tag. Where they differ, the `-mlx` build is bigger, so slower: 8-bit for `qwen3.5:0.8b-mlx` and `2b-mlx`; bigger 4-bit builds for `qwen3.5:9b-mlx` and `gemma4:26b-mlx` (both `gemma4:26b` tags carry a speculative-decoding draft model; the `-mlx` one is larger); and `muse-glimmer:30b-mlx` is the `30b-nvfp4` weights plus a draft model [\[18\]](#ref-18) |
| `-coding-` tags (Qwen 3.5, 3.6) | Builds with sampling settings tuned for coding [\[10\]](#ref-10). Not ranked separately; [section 2](#config-context) gives coding sampling settings for the plain tags |
| `-mtp-` tags (Qwen 3.5, 3.6, 3.8, Gemma 4) and `-dflash` tags (Muse Glimmer; `qwen3.8:27b-dflash2-nvfp4`, new with Ollama 0.40.12's DFlash2 support [\[2\]](#ref-2)) | Speculative-decoding builds. The speed estimate can't model their gain, so they're ranked as the plain tags [\[33\]](#ref-33) |
| `gemma4:31b-it-qat`, `gemma4:e2b-it-qat`, `gemma4:e4b-it-qat` | Ranked lower once speed is applied |
| `laguna-s-2.1`, `laguna-xs-2.1` | Open parser bug turns plain JSON into tool calls ([\#17602](https://github.com/ollama/ollama/issues/17602)); no AA score |
| `gpt-oss:20b` (coding) / `:120b` | 20b: TB 13.9, below the TB 20 floor for coding; it's a General pick on Windows 32 GB. 120b: TB 26.2, outranked on Mac 128 GB, the only tier it fits. Both have open tool-call reports ([\#11991](https://github.com/ollama/ollama/issues/11991), [\#12203](https://github.com/ollama/ollama/issues/12203), [\#17638](https://github.com/ollama/ollama/issues/17638)) |
| `nemotron-3-super` | Fits only Mac 128 GB; outranked there by its successor `nemotron-3.5-super` |
| `ornith-1.5:122b` (`122b-nvfp4`, `122b-q4_K_M`) | No AA score, and its vendor's Terminal-Bench 2.1 score (81.2) was run with Claude Code, not Terminus 2, AA's agent, so it doesn't count [\[5\]](#ref-5). It would fit Mac 128 GB. Its General use isn't ranked either: no AA HLE or AA-LCR score |
| `qwen3:4b-instruct-2507`, `qwen3-next:80b-a3b-thinking` | Evaluated; outranked in every tier (General picks in the previous version of this report) |
| `bonsai-2` | Only 2-bit ternary builds (`q2_0`) and no AA score; can't be ranked [\[33\]](#ref-33) |
| `nemotron-3.5-bolt:e4b` (8B, 4B effective, based on Gemma 4 E4B) | No AA score yet and no NVIDIA Terminal-Bench, HLE, AA-Omniscience or AA-LCR score; can't be ranked [\[14\]](#ref-14)[\[49\]](#ref-49). Needs Ollama 0.40.10 [\[2\]](#ref-2) |
| Kolibri 1 (Aleph Alpha, 78B MoE, 3.5B active) | Not in the Ollama library; only a community upload exists (`robit/kolibri-1`, 65 GB at 4-bit). No AA score; its vendor's Terminal-Bench 2.1 score (27.7) would be outranked on Mac 128 GB, the only tier it fits [\[50\]](#ref-50) |
| `lfm2.5:24b` | No AA score and no vendor Terminal-Bench score; can't be ranked |
| `mistral-medium-3.5`, `devstral-2` | Fit only Mac 128 GB, where they estimate about 3-5 tok/s; fail the speed filter |
| `ornith-1.5:397b`, `cogito-2.1` | Don't fit any tier |
| `glm-5.3`, `glm-5.3-flash`, `glm-5.2`, `kimi-k3`, `kimi-k2.6`, `kimi-k2.7-code`, `deepseek-v4-pro`, `deepseek-v4.1-flash`, `minimax-m3`, `minimax-m2.7`, `mistral-large-3`, `mistral-large-4`, `nemotron-3-ultra`, `muse-spark-open`, `beam`, `minimax-m3.1-flash` | Cloud-only in Ollama |
| `nimble`, `nimble-v3`, `tev1`, `clef`, `clef-flash`, `laya`, `kev`, `strands-decider`, `pplx-decider`, `d1`, `d1-omni`, `d3` | Decision models: they turn a state and typed questions into decisions (classification, routing, scoring). Not general chat or coding models [\[51\]](#ref-51) |

------------------------------------------------------------------------

## Config changes

### 1. Ollama server settings (all machines) {#config-server}

| Variable | Value | Why |
|:---|:---|:---|
| `OLLAMA_CONTEXT_LENGTH` | `65536` | Fallback for any model without a Modelfile. Default is 4k below 24 GiB of GPU memory [\[19\]](#ref-19). |
| `OLLAMA_FLASH_ATTENTION` | `1` | Already automatic on supported backends; setting it removes doubt [\[52\]](#ref-52) |
| `OLLAMA_KEEP_ALIVE` | `30m` | Default 5m unloads the model during pauses in an agent session [\[52\]](#ref-52) |
| `OLLAMA_NUM_PARALLEL` | `1` (default) | Each parallel slot multiplies KV-cache memory [\[52\]](#ref-52) |
| `OLLAMA_KV_CACHE_TYPE` | unset (`f16`), or `q8_0` if memory is tight | `q8_0` roughly halves context memory; per the FAQ, "this usually has no noticeable impact" [\[52\]](#ref-52). Open [\#17347](https://github.com/ollama/ollama/issues/17347) reports Qwen 3.5/3.6 stopping before tool calls with `q8_0` on AMD ROCm |

How to set these variables:

- **macOS:** run `launchctl setenv OLLAMA_CONTEXT_LENGTH 65536` (and likewise for the others), then restart the Ollama app [\[52\]](#ref-52). Also set the context length with the app's Settings slider [\[19\]](#ref-19).
- **Windows:**
  1.  Quit Ollama by clicking its icon in the taskbar.
  2.  Open Settings → "Edit environment variables for your account" and add the variables.
  3.  Start Ollama again [\[52\]](#ref-52).
- **Windows GPU extras:**
  - NVIDIA driver must be **551.61 or newer** [\[53\]](#ref-53).
  - If the Intel iGPU causes instability on a Pro Max, keep Vulkan on and set `GGML_VK_VISIBLE_DEVICES` to the NVIDIA GPU's index. `OLLAMA_VULKAN=0` turns Vulkan off completely and is the general fallback [\[37\]](#ref-37).

### 2. Per-model context fix (required) {#config-context}

OpenCode talks to Ollama's `/v1` endpoint, which can't set the context size per request. So bake the context size into a model of your own [\[21\]](#ref-21):

| Machines | `num_ctx` |
|:---|:---|
| Macs up to 36 GB; all Dells | `65536`, the minimum Ollama recommends for OpenCode [\[20\]](#ref-20). On the 24 GB GPU, the 27B models' context at 128k (about 8.6 GB, estimate) wouldn't fit in VRAM beside their weights |
| Macs 48 GB+ | `131072` |

**General picks with less room.** These General picks fit by their weights, but 64k of context wouldn't fit beside them (estimate, with the Mac GPU limit raised as in [section 3](#config-gpu-limit)). Use the largest context that fits:

| Model | Tier | `num_ctx` |
|:---|:---|:---|
| `granite4.2:3b-q4_K_M` | Mac M1 8 GB, Mac 8 GB, Latitude 7350 | `32768` |
| `qwen3:4b-thinking-2507-q4_K_M` | Mac M1 8 GB, Mac 8 GB, Latitude 7350 | `16384` |
| `granite4.2:8b-q4_K_M` | Mac 16-24 GB | `32768` |
| `qwen3:30b-a3b-thinking-2507-q4_K_M` | Windows 32 GB | `16384` |

These are too small for OpenCode, which needs 64k [\[20\]](#ref-20); none of these models is a coding pick in those tiers.

    # Modelfile (example: Mac 48-96 GB)
    FROM qwen3.8:27b-nvfp4
    PARAMETER num_ctx 131072

    ollama create oc-qwen3.8-27b -f Modelfile
    ollama ps        # CONTEXT should read 131072; PROCESSOR 100% GPU

**Use the full tag from the tables in `FROM`.** On a Mac, a short tag such as `FROM qwen3.8:27b` resolves to the MLX build, and on Windows to the GGUF build; the full tag tells you which one you get ([tag choice](#config-tags)).

**MLX builds take the same fix.** Ollama passes `num_ctx` to the MLX runner, which reports it as the model's context length [\[54\]](#ref-54). `qwen3.8-flash-next:125b-a6b-nvfp4` ships `num_ctx 262144` [\[18\]](#ref-18); the Modelfile value replaces it, and OpenCode's `limit.context` must match whichever applies ([section 5](#config-opencode)).

**Sampling settings:** most Ollama tags already carry the vendor's recommended values. For example, `qwen3.8` ships with temperature 1, top_p 0.95 and top_k 20, matching its model card [\[42\]](#ref-42).

**`qwen3.6:35b-a3b` for coding.** Both its builds (`-nvfp4` and `-q4_K_M`) ship `presence_penalty 1.5` [\[18\]](#ref-18), Qwen's value for general tasks in thinking mode, which it runs by default. For precise coding Qwen gives `presence_penalty 0.0` [\[55\]](#ref-55) ([\#17197](https://github.com/ollama/ollama/issues/17197)). Both `qwen3.6:27b` builds already ship `0`. Add this to the 35B's coding Modelfile:

    PARAMETER presence_penalty 0

**Ornith 1.5 9B and 35B ship no sampling settings,** so Ollama's defaults apply. The vendor ran most of its benchmarks at temperature 1.0 and top_p 0.95-1.0 (ClawEval at temperature 0.6), and Terminal-Bench at temperature 1.0 and top_p 1.0 [\[13\]](#ref-13); add those to the Modelfile to match.


**`flint:40b-a2b-qat-int4` ships temperature 1, top_k 20 and top_p 0.95,** the values Recursive recommends and used for its scores [\[18\]](#ref-18)[\[16\]](#ref-16). It needs only the `num_ctx` line. Recursive suggests an output budget of at least 32,768 tokens for hard problems, reasoning included [\[16\]](#ref-16).

**Ornith 1.0 tags (`ornith:9b-q4_K_M`, `ornith:35b-q4_K_M`) ship temperature 0.6, top_k 20 and top_p 0.95** [\[18\]](#ref-18), but the Terminal-Bench scores in the tables were run at temperature 1.0 and top_p 1.0 [\[13\]](#ref-13). To match them, add `PARAMETER temperature 1` and `PARAMETER top_p 1` to the Modelfile.

**`nemotron-3.5-super:120b-a12b-nvfp4` ships no sampling settings either,** while its GGUF build ships temperature 1 and top_p 0.95 [\[18\]](#ref-18). Add the same two lines to the MLX build's Modelfile:

    PARAMETER temperature 1
    PARAMETER top_p 0.95

For coding with either Qwen 3.6 pick, Qwen's thinking-mode value for precise coding is `PARAMETER temperature 0.6` [\[56\]](#ref-56).

**`qwen3.5:122b-a10b-q4_K_M` ships no `presence_penalty`,** so Ollama's default of 0 applies; Qwen gives `presence_penalty 1.5` for general tasks in thinking mode [\[57\]](#ref-57). For General use add `PARAMETER presence_penalty 1.5`.

**Qwen 3.5 coding picks** (`qwen3.5:4b-q4_K_M`, `qwen3.5:9b-nvfp4`) ship `temperature 1` and `presence_penalty 1.5`. Qwen's card gives `temperature 0.6` and `presence_penalty 0` for precise coding in thinking mode [\[58\]](#ref-58), so add both to their Modelfiles when used for coding.

### 3. Mac GPU memory limit {#config-gpu-limit}

macOS caps how much unified memory the GPU can use. The default cap isn't published by Apple; it's commonly reported as about 2/3 of RAM on Macs up to 36 GB and about 3/4 above that (unsourced). A model that doesn't fit under the cap still runs, but part of it runs on the CPU (unsourced). `ollama ps` shows that split [\[52\]](#ref-52), and Ollama advises avoiding CPU offload for best performance [\[19\]](#ref-19).

**Check first.** Load the model, then run `ollama ps`. If PROCESSOR reads **100% GPU**, the model is entirely on the GPU, so leave the cap alone. A split such as `48%/52% CPU/GPU` means part of it spilled [\[52\]](#ref-52).

| Tier | When to raise the cap | Example value |
|:---|:---|:---|
| Macs up to 36 GB | When a coding pick's weights plus 64k of context exceed the default cap: the coding fit estimates, and the General context sizes in [section 2](#config-context), allow up to about 80% of RAM | `6500` on 8 GB · `13000` on 16 GB · `14700` on 18 GB · `19600` on 24 GB · `26000` on 32 GB · `29000` on 36 GB |
| Mac 128 GB | Required for `qwen3.8-flash-next` (105 GB), the \#1 pick. Check `ollama ps` with the coding build `nemotron-3.5-super:120b-a12b-q4_K_M` (90 GB, close to the default cap); the General build `120b-a12b-nvfp4` (80 GB) fits under it (estimate) | `114000` |
| Mac 48-96 GB | Not needed for the picks in this report | — |

The value is in MB. It must be larger than the model and smaller than total RAM [\[59\]](#ref-59). The example values leave about 1.6-17 GB for macOS (estimate). On 8 and 16 GB Macs that's tight: close other apps while a model is loaded, and watch for swapping.

**Until the next reboot:**

    sudo sysctl -w iogpu.wired_limit_mb=26000

**Permanent:** add the same setting to `/etc/sysctl.conf`, which macOS applies at boot (unsourced):

    echo "iogpu.wired_limit_mb=26000" | sudo tee -a /etc/sysctl.conf

- **Risk:** setting it too high starves macOS of memory, which causes swapping or freezes (unsourced). Raise it in small steps and re-check `ollama ps`.
- **To undo:** set it to `0`, which is commonly reported to restore the macOS default (unsourced), and remove the line from `/etc/sysctl.conf`.

### 4. Tag choice {#config-tags}

- **Ollama 0.40 runs supported models on MLX by default on Apple silicon**, starting with Qwen 3.8, Qwen 3.6, Qwen 3.5 and Gemma 4 [\[11\]](#ref-11). MLX is Apple's machine-learning framework [\[10\]](#ref-10). MLX builds run only on Apple silicon; Windows uses GGUF.
- **How the Mac tables pick a build:** of the builds that fit the tier and pass the speed filter, the one with the highest estimate. An MLX build within 10% of that is listed instead, unless it would lose 15 tok/s on a machine where the faster build has it. Among MLX builds, `-nvfp4` comes first: Ollama says NVFP4 keeps model accuracy while cutting memory use [\[10\]](#ref-10). `-int4` is listed only when it's more than 10% faster, as for `qwen3.5:27b-int4`.
- **Why near-ties go to MLX:** Ollama reports NVFP4 generating about 20% faster than `q4_K_M` [\[12\]](#ref-12), and MLX is Ollama's default on Macs [\[11\]](#ref-11). The speed estimates don't include that gain, because it isn't measured on these machines.
- **Many short tags hold two builds.** For example, `qwen3.8:27b`, `qwen3.6:27b`, `qwen3.6:35b-a3b`, `qwen3.5:9b`, `gemma4:12b`, `gemma4:26b` and `nemotron-3.5-super:120b-a12b` each list an MLX build and a GGUF build [\[18\]](#ref-18). On Apple silicon Ollama picks MLX first; elsewhere it picks GGUF first [\[60\]](#ref-60). The tables always give the full tag.
- **`flint` and `flint:40b` also hold two builds:** the MLX `40b-a2b-qat-int4` and the GGUF `40b-a2b-gguf-nvfp4` [\[18\]](#ref-18). The GGUF build needs Ollama 0.40.9 [\[18\]](#ref-18), and it's NVFP4, which Macs can't run on the GPU; on a Mac use the full tag `flint:40b-a2b-qat-int4` [\[32\]](#ref-32).
- **To check which engine loaded,** run `ollama ps`: its RUNNER column reads `mlx` for the MLX build [\[61\]](#ref-61).
- **If an MLX build misbehaves, switch to the GGUF build of the same model** (listed beside it in the [Model reference](#model-reference)). It has the same score; the estimates differ by 10% or less, except for `nemotron-3.5-super` (the MLX build is 12% smaller) and `qwen3.8-flash-next` (no GGUF build fits). For `flint`, the Mac GGUF build is `40b-a2b-q4_1` (26 GB, about 13% slower; it fits Macs with 48 GB or more); `40b-a2b-gguf-nvfp4` is for NVIDIA GPUs and doesn't run on Apple's GPU [\[31\]](#ref-31)[\[32\]](#ref-32). Open MLX reports, none confirmed by Ollama:
  - [\#18754](https://github.com/ollama/ollama/issues/18754): the GPU only 50-70% busy on an M4 Pro (0.40). If MLX isn't faster on your Mac, use GGUF.
  - [\#16279](https://github.com/ollama/ollama/issues/16279): tool-call arguments arrive in one piece at the end instead of streaming, so a long file write can hit a client timeout. The report says non-MLX backends stream tool calls properly.
  - [\#18131](https://github.com/ollama/ollama/issues/18131): MLX's prompt cache pushing a 32 GB Mac into heavy swap during agent sessions.
- **Ollama 0.40.4 fixed two MLX bugs** [\[2\]](#ref-2): the per-tool-call memory leak ([\#18620](https://github.com/ollama/ollama/issues/18620), [PR 18955](https://github.com/ollama/ollama/pull/18955)) and the "Maximum threads" crash on `qwen3.6:35b-mlx` and `qwen3.8:27b-mlx` ([\#18846](https://github.com/ollama/ollama/issues/18846), [PR 18956](https://github.com/ollama/ollama/pull/18956)). Ollama 0.40.5 and 0.40.7 update MLX again [\[2\]](#ref-2). Use 0.40.9 or later: Flint's MLX build needs 0.40.8 and its GGUF builds 0.40.9 [\[18\]](#ref-18).
- **`ollama show <tag>` now reports the model's parser and renderer** (since 0.40.7) [\[2\]](#ref-2). Use it to see whether a model you pulled shares a parser with a ⚠ flag in this report.

### 5. OpenCode 2.x (`~/.config/opencode/opencode.jsonc`) {#config-opencode}

**Ollama is discovered automatically.** OpenCode 2 probes `http://127.0.0.1:11434`, lists every Ollama model that can chat, and reads context, vision and tool-use capabilities from Ollama, with no provider config needed [\[62\]](#ref-62). Select a model as `ollama/<tag>`.

**Still override the context limit.** Discovery reads each model's maximum context from Ollama, not your `num_ctx` [\[63\]](#ref-63), and requests go through Ollama's `/v1` endpoint, which has no way to set the context size [\[64\]](#ref-64)[\[21\]](#ref-21). So keep the Modelfile fix from section 2, and tell OpenCode the same limit. A `limit` set in config overrides the discovered value [\[65\]](#ref-65). Example for a Mac with 48-96 GB, matching the Modelfile above [\[64\]](#ref-64)[\[62\]](#ref-62):

    {
      "$schema": "https://opencode.ai/config.json",
      "model": "ollama/oc-qwen3.8-27b",
      "providers": {
        "ollama": {
          "models": {
            "oc-qwen3.8-27b": {
              "name": "Qwen3.8 27B (local, 128k)",
              "capabilities": { "tools": true, "input": ["text", "image"], "output": ["text"] },
              "limit": { "context": 131072, "output": 16384 },
            },
          },
        },
      },
      "compaction": { "auto": true },
    }

- **`limit.context` must equal the model's `num_ctx`.** It tells OpenCode when to compact; it doesn't change Ollama. Automatic compaction is on by default and, since OpenCode 2.1.0, keeps 15% of the limit free (up from 10%), at least 16k tokens [\[66\]](#ref-66)[\[67\]](#ref-67). Below a limit of about 107k the 16k minimum applies, so at 64k nothing changes; at 128k about 19.7k is kept free instead of 16k. Since 2.2.5, `compaction.buffer` also takes a percentage, such as `"20%"`, as well as a token count [\[1\]](#ref-1).
- **OpenCode 2.1 can't be downgraded cleanly.** Sessions compacted by 2.1 can't be loaded by 2.0 [\[68\]](#ref-68).
- **Malformed tool calls fail visibly (since 2.0.25).** OpenCode no longer repairs bad tool-call JSON; it sends the model a tool error so it can retry [\[69\]](#ref-69). With the parser bugs above, expect the odd retried tool call rather than a silent fix.
- **Key names changed from 1.x:** 2.x uses `providers`, `package`, `settings` and `capabilities.tools` [\[64\]](#ref-64)[\[62\]](#ref-62), where 1.x used `provider`, `npm`, `options` and `tool_call` [\[70\]](#ref-70). `small_model` isn't in the 2.x docs; title and summary work is done by hidden built-in agents [\[71\]](#ref-71).
- **The config schema describes 2.x.** The schema at `opencode.ai/config.json` has the `providers` key and marks 1.x keys such as `provider` and `small_model` as deprecated [\[70\]](#ref-70).
- **Remote Ollama:** set `providers.ollama.settings.baseURL` to its `/v1` URL [\[62\]](#ref-62).
- **Keep MCP servers to a minimum.** MCP tools consume model context [\[72\]](#ref-72), on top of OpenCode's own system prompt and tools.
- **Prefer the config above to `ollama launch opencode`.** Ollama's OpenCode page shows only 1.x setup (the Windows install is the 1.x package `opencode-ai`; the manual config uses `provider` and `npm`) [\[20\]](#ref-20). Before Ollama 0.40.12, `ollama launch opencode` failed with OpenCode 2, which rejects its `--model` flag; 0.40.12 launches OpenCode 2 with `--standalone` instead, but an agent's own model setting in OpenCode 2 can still override the model it picks [\[17\]](#ref-17). Before Ollama 0.40.11, `ollama launch opencode` gave OpenCode the model's maximum context rather than the context Ollama actually loaded, so compaction started too late; 0.40.11 reads the loaded context and passes that instead ([\#19172](https://github.com/ollama/ollama/issues/19172), fixed by [PR 19193](https://github.com/ollama/ollama/pull/19193), which is in 0.40.11).

------------------------------------------------------------------------

## Watched issues

When one of these closes, the affected pick or flag may change. A parser's ⚠ flag lifts only when **every** open tool-call bug in that parser is closed. Other open bugs in the same parser that aren't listed here (e.g. [\#16686](https://github.com/ollama/ollama/issues/16686), [\#12751](https://github.com/ollama/ollama/issues/12751), [\#18421](https://github.com/ollama/ollama/issues/18421) for `qwen3-coder`; [\#18275](https://github.com/ollama/ollama/issues/18275), [\#15445](https://github.com/ollama/ollama/issues/15445), [\#15315](https://github.com/ollama/ollama/issues/15315) for `gemma4`; [\#18658](https://github.com/ollama/ollama/issues/18658), [\#18659](https://github.com/ollama/ollama/issues/18659) for `glm-4.7`) still count. If an Ollama maintainer confirms one of these bugs, the affected models drop out of coding.

| Issue | Affects | Effect when closed |
|:---|:---|:---|
| [\#18754](https://github.com/ollama/ollama/issues/18754) MLX runner underuses the GPU (0.40) | Mac MLX builds | Removes the "if MLX isn't faster" caution |
| [\#16279](https://github.com/ollama/ollama/issues/16279) MLX doesn't stream tool-call arguments | Mac MLX builds (coding) | Removes the timeout caution |
| [\#18131](https://github.com/ollama/ollama/issues/18131) MLX prompt cache causes heavy swap on 32 GB | MLX builds on Mac 32-36 GB | Removes the swap caution |
| [\#17426](https://github.com/ollama/ollama/issues/17426), [\#15880](https://github.com/ollama/ollama/issues/15880) `qwen3.6:35b-a3b` hangs or loops on MLX | `qwen3.6:35b-a3b-nvfp4` | Removes the caution |
| [\#17362](https://github.com/ollama/ollama/issues/17362) `gemma4:12b` MLX slower than expected | `gemma4:12b-nvfp4` | Removes the caution |
| [\#18840](https://github.com/ollama/ollama/issues/18840) `qwen3.8:27b` HTTP 500 on Windows (0.40) | Pro Max 16 Plus, 24 GB GPU | Removes the warning |
| [\#19439](https://github.com/ollama/ollama/issues/19439) HTTP 500 crash during tool calls on Windows (0.40.13) | `qwen3.5:27b-q4_K_M`, `muse-glimmer:30b-q4_K_M` on the Pro Max 16 Plus | Removes the caution |
| [\#17778](https://github.com/ollama/ollama/issues/17778) `qwen3.8` HTTP 500 "no user query found" | `qwen3.8:27b`, `qwen3.8-flash-next` | Removes the Mac 128 GB warning |
| [\#18649](https://github.com/ollama/ollama/issues/18649), [\#18390](https://github.com/ollama/ollama/issues/18390), [\#18354](https://github.com/ollama/ollama/issues/18354) Gemma 4 drops tool calls | `gemma4` | Part of the Gemma flag |
| [\#16383](https://github.com/ollama/ollama/issues/16383) Qwen 3.6 template drift; `qwen3.5` parser returns 500 | `qwen3.5` parser (Qwen 3.5/3.6/3.8) | Removes the flag |
| [\#18053](https://github.com/ollama/ollama/issues/18053) `cohere` parser misses end of turn | `north-mini-code-1.0:q4_K_M` | Removes the flag |
| [\#18530](https://github.com/ollama/ollama/issues/18530) `qwen3-coder` parser loses tool calls | `qwen3-coder-next` | Part of the `qwen3-coder` flag |
| [\#17882](https://github.com/ollama/ollama/issues/17882) More Gemma 4 tool-call bugs | `gemma4` | Part of the Gemma flag |
| [\#19273](https://github.com/ollama/ollama/issues/19273) Gemma 4 drops a tool call with an unclosed list | `gemma4` parser (Gemma 4, `nemotron-3.5-bolt:e4b`) | Part of the Gemma flag |
| [\#19268](https://github.com/ollama/ollama/issues/19268) MLX ignores `stop` | Mac MLX builds (reported on `gemma4:26b-nvfp4`) | Removes the caution |
| [\#17197](https://github.com/ollama/ollama/issues/17197) `qwen3.6` default presence_penalty | `qwen3.6` | Re-check the coding Modelfile override |
| [\#16992](https://github.com/ollama/ollama/issues/16992) Ornith parser leaks raw tool-call XML | `ornith` parser | Removes the flag on `ornith:9b-q4_K_M` and `ornith:35b-q4_K_M` |
| [\#19191](https://github.com/ollama/ollama/issues/19191) Flint re-sends integer tool arguments as strings | `flint` (all builds use the `flint` renderer) | Removes the caution |
| [\#17957](https://github.com/ollama/ollama/issues/17957) `ornith-1.5:35b` fails with tools plus a JSON response format | `ornith-1.5:35b` (and likely `:9b`) | No ranking change (not normal agent use). Fix pending in [PR 17965](https://github.com/ollama/ollama/pull/17965) |
| [\#13820](https://github.com/ollama/ollama/issues/13820) GLM-4.7-Flash tool-call parse failures | `glm-4.7-flash` | Part of the `glm-4.7` flag |
| [\#17602](https://github.com/ollama/ollama/issues/17602) Laguna parser turns JSON into tool calls | `laguna-*` | Laguna becomes eligible |
| [\#17638](https://github.com/ollama/ollama/issues/17638), [\#11991](https://github.com/ollama/ollama/issues/11991), [\#12203](https://github.com/ollama/ollama/issues/12203) gpt-oss tool-call failures | `gpt-oss` | Removes the flag |
| [\#17562](https://github.com/ollama/ollama/issues/17562) Gemma 4 A4B drops tool calls in Cline | `gemma4:26b-a4b-it-qat` | Part of the Gemma flag |
| [\#17656](https://github.com/ollama/ollama/issues/17656), [\#18269](https://github.com/ollama/ollama/issues/18269) Muse Glimmer `30b-mlx` tag | `muse-glimmer:30b-mlx`, which holds the `30b-nvfp4` weights | Removes the caution on `30b-nvfp4` |

------------------------------------------------------------------------

## Sources {#sources}

<ol class="refs">
<li id="ref-1">OpenCode 2.x release (npm <code>@opencode/cli</code> 2.2.5, published 2026-10-30): <a href="https://registry.npmjs.org/@opencode/cli/latest">https://registry.npmjs.org/@opencode/cli/latest</a>; release notes: <a href="https://github.com/anomalyco/opencode/releases/tag/v2.2.5">https://github.com/anomalyco/opencode/releases/tag/v2.2.5</a></li>
<li id="ref-2">Ollama release notes: v0.40.13 (published 2026-10-28; LFM3 on Linux and Windows): <a href="https://github.com/ollama/ollama/releases/tag/v0.40.13">https://github.com/ollama/ollama/releases/tag/v0.40.13</a>; v0.40.12 (published 2026-10-27; LFM3 on Apple silicon, DFlash2 speculative decoding on MLX, &ldquo;<code>ollama launch</code> now works with OpenCode v2&rdquo;): <a href="https://github.com/ollama/ollama/releases/tag/v0.40.12">https://github.com/ollama/ollama/releases/tag/v0.40.12</a>; v0.40.11 (published 2026-10-24; speech, d3 decision models): <a href="https://github.com/ollama/ollama/releases/tag/v0.40.11">https://github.com/ollama/ollama/releases/tag/v0.40.11</a>; v0.40.10 (published 2026-10-23; Nemotron 3.5 Bolt E4B): <a href="https://github.com/ollama/ollama/releases/tag/v0.40.10">https://github.com/ollama/ollama/releases/tag/v0.40.10</a>; v0.40.9 (published 2026-10-22; &ldquo;Flint on Linux and Windows&rdquo;): <a href="https://github.com/ollama/ollama/releases/tag/v0.40.9">https://github.com/ollama/ollama/releases/tag/v0.40.9</a>; v0.40.8 (published 2026-10-21; Flint, &ldquo;supported on MacOS&rdquo;, other GPUs in a later release): <a href="https://github.com/ollama/ollama/releases/tag/v0.40.8">https://github.com/ollama/ollama/releases/tag/v0.40.8</a>; v0.40.7 (published 2026-10-18; <code>ollama show</code> reports renderer and parser; llama.cpp and MLX update): <a href="https://github.com/ollama/ollama/releases/tag/v0.40.7">https://github.com/ollama/ollama/releases/tag/v0.40.7</a>; v0.40.5 (published 2026-10-14; Nemotron 3.5 support in llama.cpp, MLX update): <a href="https://github.com/ollama/ollama/releases/tag/v0.40.5">https://github.com/ollama/ollama/releases/tag/v0.40.5</a>; v0.40.4 (published 2026-10-12; MLX fixes in PRs 18955 and 18956): <a href="https://github.com/ollama/ollama/releases/tag/v0.40.4">https://github.com/ollama/ollama/releases/tag/v0.40.4</a></li>
<li id="ref-3">Artificial Analysis, Intelligence Index methodology (v5.0 evals and weights; legacy evaluations: HLE, AA-LCR and CritPt removed or replaced in v5.0; AA-Omniscience v1.1 &ldquo;not directly comparable with v1&rdquo;; version history): <a href="https://artificialanalysis.ai/methodology/intelligence-benchmarking">https://artificialanalysis.ai/methodology/intelligence-benchmarking</a></li>
<li id="ref-4">Artificial Analysis leaderboard (per-eval scores (HLE, CritPt, AA-LCR, AA-Omniscience v1.1) and Terminal-Bench 2.1, read 2026-11-02; deprecated models&rsquo; scores from the same data on AA&rsquo;s model pages, e.g. <a href="https://artificialanalysis.ai/models/qwen3-5-27b">https://artificialanalysis.ai/models/qwen3-5-27b</a>): <a href="https://artificialanalysis.ai/leaderboards/models">https://artificialanalysis.ai/leaderboards/models</a></li>
<li id="ref-5">Ornith Team, Ornith-1.5-122B model card (Terminal-Bench 2.1 81.2; evaluation settings; sampling settings; MIT license; config): <a href="https://huggingface.co/ornith-ai/Ornith-1.5-122B">https://huggingface.co/ornith-ai/Ornith-1.5-122B</a></li>
<li id="ref-6">NVIDIA, Nemotron 3.5 Bolt 74B-A9B 24GB GGUF model card (74B total, 9B active; Terminal-Bench 2.1 50.98 for the IQ2 build; OpenMDW 1.1): <a href="https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-24GB-GGUF">https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-24GB-GGUF</a></li>
<li id="ref-7">LMArena text leaderboard with style control, overall category, published 2026-10-28 (dataset config <code>text_style_control</code>, split <code>latest</code>; ratings with lower and upper bounds): <a href="https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset">https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset</a>; leaderboard: <a href="https://lmarena.ai/leaderboard/text">https://lmarena.ai/leaderboard/text</a></li>
<li id="ref-8">Liquid AI, LFM3-1.7B model card (benchmark table: Terminal-Bench 2.1 (OpenCode) 12.92; LFM Open License v1.0): <a href="https://huggingface.co/LiquidAI/LFM3-1.7B">https://huggingface.co/LiquidAI/LFM3-1.7B</a></li>
<li id="ref-9">Ollama library, lfm3 (&ldquo;not recommended for agentic coding or complex multi-step reasoning due to its small size&rdquo;; 256K context): <a href="https://ollama.com/library/lfm3">https://ollama.com/library/lfm3</a></li>
<li id="ref-10">Ollama blog, MLX on Apple silicon: <a href="https://ollama.com/blog/mlx">https://ollama.com/blog/mlx</a></li>
<li id="ref-11">Ollama v0.40.0 release notes, &ldquo;Models run on MLX on Apple Silicon by default&rdquo;: <a href="https://github.com/ollama/ollama/releases/tag/v0.40.0">https://github.com/ollama/ollama/releases/tag/v0.40.0</a></li>
<li id="ref-12">Ollama blog, MLX performance: <a href="https://ollama.com/blog/mlx-performance">https://ollama.com/blog/mlx-performance</a></li>
<li id="ref-13">Ornith Team, Ornith-1.5 announcement and benchmark tables: <a href="https://ornith.ai/ornith_1_5.html">https://ornith.ai/ornith_1_5.html</a></li>
<li id="ref-14">Ollama library, nemotron-3.5-bolt (IQ2_XXS expert weights by quantization-aware distillation; &ldquo;Apple Silicon / Metal is not currently supported for 74B-A9B&rdquo;): <a href="https://ollama.com/library/nemotron-3.5-bolt">https://ollama.com/library/nemotron-3.5-bolt</a></li>
<li id="ref-15">Artificial Analysis, Nemotron 3.5 Bolt 74B-A9B model page (weights source: the BF16 release): <a href="https://artificialanalysis.ai/models/nemotron-3-5-bolt-74b-a9b">https://artificialanalysis.ai/models/nemotron-3-5-bolt-74b-a9b</a></li>
<li id="ref-16">Recursive, Flint model card (39.8B total, ~2.5B active; Terminal-Bench 2.1 54.9 BF16 and 53.7 NVFP4 in the evaluation chart; sampling settings; Apache 2.0): <a href="https://huggingface.co/RecursiveSI/flint">https://huggingface.co/RecursiveSI/flint</a></li>
<li id="ref-17">Ollama PR 19310, &ldquo;cmd/launch: fix OpenCode v2 launch and config parsing&rdquo; (&ldquo;OpenCode v2 rejects <code>--model</code> on the bare command&rdquo;), in v0.40.12: <a href="https://github.com/ollama/ollama/pull/19310">https://github.com/ollama/ollama/pull/19310</a></li>
<li id="ref-18">Ollama registry manifests and config blobs (<code>runner</code>, <code>format</code> and <code>parser</code> fields), e.g. <a href="https://registry.ollama.ai/v2/library/qwen3.5/manifests/9b">https://registry.ollama.ai/v2/library/qwen3.5/manifests/9b</a></li>
<li id="ref-19">Ollama docs, Context length: <a href="https://docs.ollama.com/context-length">https://docs.ollama.com/context-length</a></li>
<li id="ref-20">Ollama docs, OpenCode integration: <a href="https://docs.ollama.com/integrations/opencode">https://docs.ollama.com/integrations/opencode</a></li>
<li id="ref-21">Ollama docs, OpenAI compatibility: <a href="https://docs.ollama.com/api/openai-compatibility">https://docs.ollama.com/api/openai-compatibility</a></li>
<li id="ref-22">Ollama v0.40.5 source, default thinking per model (local models default thinking on; Qwen 3.8 defaults to "medium"), applied to chat requests that don't set it: <a href="https://github.com/ollama/ollama/blob/v0.40.5/server/model_thinking.go">https://github.com/ollama/ollama/blob/v0.40.5/server/model_thinking.go</a> · <a href="https://github.com/ollama/ollama/blob/v0.40.5/model/renderers/thinking.go">https://github.com/ollama/ollama/blob/v0.40.5/model/renderers/thinking.go</a></li>
<li id="ref-23">Ollama source, tool support read from the model's chat template (<code>chatTemplateHasToolSupport</code>, v0.40.1) or from its built-in tool-call parser (<code>parserCapabilities</code>, v0.40.5): <a href="https://github.com/ollama/ollama/blob/v0.40.1/server/images.go">https://github.com/ollama/ollama/blob/v0.40.1/server/images.go</a> · <a href="https://github.com/ollama/ollama/blob/v0.40.5/server/images.go">https://github.com/ollama/ollama/blob/v0.40.5/server/images.go</a></li>
<li id="ref-24">Ollama v0.40.5 source, llama.cpp's Jinja chat template used unless Ollama renders the chat itself (<code>DisableJinja: usesOllamaRenderedChat(m)</code>): <a href="https://github.com/ollama/ollama/blob/v0.40.5/server/routes.go">https://github.com/ollama/ollama/blob/v0.40.5/server/routes.go</a></li>
<li id="ref-25">Apple MacBook Pro tech specs: <a href="https://support.apple.com/en-us/111893">111893</a> · <a href="https://support.apple.com/en-us/111902">111902</a> · <a href="https://support.apple.com/en-us/111901">111901</a> · <a href="https://support.apple.com/en-us/111869">111869</a> · <a href="https://support.apple.com/en-us/111340">111340</a> · <a href="https://support.apple.com/en-us/111838">111838</a> · <a href="https://support.apple.com/en-us/117735">117735</a> · <a href="https://support.apple.com/en-us/117736">117736</a> · <a href="https://support.apple.com/en-us/117737">117737</a> · <a href="https://support.apple.com/en-us/121552">121552</a> · <a href="https://support.apple.com/en-us/121553">121553</a> · <a href="https://support.apple.com/en-us/121554">121554</a> · <a href="https://support.apple.com/en-us/125405">125405</a> · <a href="https://support.apple.com/en-us/126318">126318</a> · <a href="https://support.apple.com/en-us/126319">126319</a></li>
<li id="ref-26">NVIDIA professional laptop GPU comparison: <a href="https://www.nvidia.com/en-us/products/workstations/professional-laptops/compare/">https://www.nvidia.com/en-us/products/workstations/professional-laptops/compare/</a></li>
<li id="ref-27">Dell specs: Latitude 7350 <a href="https://dl.dell.com/content/manual34075453-latitude-7350-owner-s-manual.pdf">owner's manual</a> · Pro 14 Premium PA14250 <a href="https://dl.dell.com/content/manual2592419-dell-pro-14-premium-pa14250-owner-s-manual.pdf">owner's manual</a> · PA14260 <a href="https://dl.dell.com/content/manual19413430-dell-pro-14-premium-pa14260-setup-and-specifications.pdf">setup and specifications</a> · Pro Max 16 <a href="https://www.delltechnologies.com/asset/en-us/products/workstations/technical-support/dell-pro-max-16-laptop-spec-sheet.pdf">spec sheet</a> · Pro Max 16 Plus <a href="https://www.delltechnologies.com/asset/en-us/products/workstations/technical-support/dell-pro-max-16-plus-laptop-spec-sheet.pdf">spec sheet</a></li>
<li id="ref-28">Ollama library, granite4.2: <a href="https://ollama.com/library/granite4.2">https://ollama.com/library/granite4.2</a></li>
<li id="ref-29">OpenBMB, MiniCPM-V 4.6 model card (built on SigLIP2-400M and Qwen3.5-0.8B; Apache 2.0): <a href="https://huggingface.co/openbmb/MiniCPM-V-4.6">https://huggingface.co/openbmb/MiniCPM-V-4.6</a></li>
<li id="ref-30">Recursive, Flint INT4 (MLX) model card (group-64 affine INT4, about 22.6 GB): <a href="https://huggingface.co/RecursiveSI/flint-int4">https://huggingface.co/RecursiveSI/flint-int4</a></li>
<li id="ref-31">Recursive, Flint NVFP4 GGUF model card (&ldquo;primarily intended for NVIDIA GPUs using llama.cpp with CUDA&rdquo;): <a href="https://huggingface.co/RecursiveSI/flint-nvfp4-gguf">https://huggingface.co/RecursiveSI/flint-nvfp4-gguf</a></li>
<li id="ref-32">llama.cpp b11963 (the build in Ollama 0.40.13; unchanged here since b11803 in 0.40.9), Metal backend declines NVFP4 matrix operations: <a href="https://github.com/ggml-org/llama.cpp/blob/b11963/ggml/src/ggml-metal/ggml-metal-device.m">ggml-metal-device.m</a>; Ollama&rsquo;s pinned version: <a href="https://github.com/ollama/ollama/blob/v0.40.13/LLAMA_CPP_VERSION">LLAMA_CPP_VERSION</a></li>
<li id="ref-33">Ollama library tags pages, e.g. <a href="https://ollama.com/library/qwen3.5/tags">https://ollama.com/library/qwen3.5/tags</a></li>
<li id="ref-34">NVIDIA, Nemotron 3.5 Super VL 120B-A12B model card (API catalog copy; BF16 and NVFP4 benchmark table): <a href="https://build.nvidia.com/nvidia/nemotron-3.5-super-vl-120b-a12b.md">https://build.nvidia.com/nvidia/nemotron-3.5-super-vl-120b-a12b.md</a></li>
<li id="ref-35">NVIDIA NeMo Gym, Nemotron 3.5 Super Terminal-Bench 2.1 recipe (&ldquo;The Terminus-2 agent works in a tmux session inside each task&rsquo;s container&rdquo;): <a href="https://github.com/NVIDIA-NeMo/Gym/blob/main/nemotron_recipes/super-3.5/terminal-bench-2.1.yaml">https://github.com/NVIDIA-NeMo/Gym/blob/main/nemotron_recipes/super-3.5/terminal-bench-2.1.yaml</a></li>
<li id="ref-36">Ollama library, ornith-1.5: <a href="https://ollama.com/library/ornith-1.5">https://ollama.com/library/ornith-1.5</a></li>
<li id="ref-37">Ollama docs, Hardware support (GPU, Vulkan): <a href="https://docs.ollama.com/gpu">https://docs.ollama.com/gpu</a></li>
<li id="ref-38">OpenAI, gpt-oss-20b model card (21B parameters, 3.6B active; Apache 2.0): <a href="https://huggingface.co/openai/gpt-oss-20b">https://huggingface.co/openai/gpt-oss-20b</a></li>
<li id="ref-39">Dell, Dell Pro Precision 5 Series 16 (PW516261) brochure: <a href="https://www.delltechnologies.com/asset/en-us/products/workstations/briefs-summaries/dell-pro-precision-5-series-16-laptop-pw516261-brochure.pdf">https://www.delltechnologies.com/asset/en-us/products/workstations/briefs-summaries/dell-pro-precision-5-series-16-laptop-pw516261-brochure.pdf</a>; Dell support page: <a href="https://www.dell.com/support/product-details/en-us/product/dell-pro-precision-pw516261-laptop/overview">https://www.dell.com/support/product-details/en-us/product/dell-pro-precision-pw516261-laptop/overview</a></li>
<li id="ref-40">Ollama library, north-mini-code-1.0: <a href="https://ollama.com/library/north-mini-code-1.0">https://ollama.com/library/north-mini-code-1.0</a></li>
<li id="ref-41">Hugging Face model cards: <a href="https://huggingface.co/Qwen">Qwen</a> · <a href="https://huggingface.co/google/gemma-4-12B-it">Gemma 4 12B</a></li>
<li id="ref-42">Qwen3.8-27B model card: <a href="https://huggingface.co/Qwen/Qwen3.8-27B">https://huggingface.co/Qwen/Qwen3.8-27B</a></li>
<li id="ref-43">Ollama library, gemma4 (26B A4B: total and active parameters): <a href="https://ollama.com/library/gemma4">https://ollama.com/library/gemma4</a></li>
<li id="ref-44">Ornith-1.0-9B model card: <a href="https://huggingface.co/ornith-ai/Ornith-1.0-9B-GGUF">https://huggingface.co/ornith-ai/Ornith-1.0-9B-GGUF</a></li>
<li id="ref-45">Ollama library, qwen3.8-flash-next (parameters and license): <a href="https://ollama.com/library/qwen3.8-flash-next">https://ollama.com/library/qwen3.8-flash-next</a></li>
<li id="ref-46">Ollama library, granite4 (sizes and license): <a href="https://ollama.com/library/granite4">https://ollama.com/library/granite4</a></li>
<li id="ref-47">Ollama library, nemotron-3.5-super: <a href="https://ollama.com/library/nemotron-3.5-super">https://ollama.com/library/nemotron-3.5-super</a></li>
<li id="ref-48">Ollama library, lfm2.5-thinking: <a href="https://ollama.com/library/lfm2.5-thinking">https://ollama.com/library/lfm2.5-thinking</a></li>
<li id="ref-49">NVIDIA, Nemotron 3.5 Bolt E4B 4GB model card (benchmark table): <a href="https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB">https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB</a></li>
<li id="ref-50">Aleph Alpha, Kolibri-1 model card (78B total, 3.46B active; TerminalBench 2.1 27.7; Apache 2.0): <a href="https://huggingface.co/Aleph-Alpha/Kolibri-1">https://huggingface.co/Aleph-Alpha/Kolibri-1</a>; community upload: <a href="https://ollama.com/robit/kolibri-1/tags">https://ollama.com/robit/kolibri-1/tags</a></li>
<li id="ref-51">Ollama model library: <a href="https://ollama.com/library?sort=popular">https://ollama.com/library?sort=popular</a></li>
<li id="ref-52">Ollama docs, FAQ: <a href="https://docs.ollama.com/faq">https://docs.ollama.com/faq</a></li>
<li id="ref-53">Ollama docs, Windows: <a href="https://docs.ollama.com/windows">https://docs.ollama.com/windows</a></li>
<li id="ref-54">Ollama v0.40.5 source, <code>num_ctx</code> passed to the MLX runner (<code>mlxrunner.NewClient</code>) and reported as its context length: <a href="https://github.com/ollama/ollama/blob/v0.40.5/server/sched.go">https://github.com/ollama/ollama/blob/v0.40.5/server/sched.go</a> · <a href="https://github.com/ollama/ollama/blob/v0.40.5/mlxrunner/client.go">https://github.com/ollama/ollama/blob/v0.40.5/mlxrunner/client.go</a></li>
<li id="ref-55">Qwen3.6-35B-A3B model card (sampling parameters): <a href="https://huggingface.co/Qwen/Qwen3.6-35B-A3B">https://huggingface.co/Qwen/Qwen3.6-35B-A3B</a></li>
<li id="ref-56">Qwen3.6-27B model card: <a href="https://huggingface.co/Qwen/Qwen3.6-27B">https://huggingface.co/Qwen/Qwen3.6-27B</a></li>
<li id="ref-57">Qwen3.5-122B-A10B model card (sampling parameters): <a href="https://huggingface.co/Qwen/Qwen3.5-122B-A10B">https://huggingface.co/Qwen/Qwen3.5-122B-A10B</a></li>
<li id="ref-58">Qwen3.5-9B model card: <a href="https://huggingface.co/Qwen/Qwen3.5-9B">https://huggingface.co/Qwen/Qwen3.5-9B</a></li>
<li id="ref-59">mlx-lm README (<code>iogpu.wired_limit_mb</code>): <a href="https://github.com/ml-explore/mlx-lm">https://github.com/ml-explore/mlx-lm</a></li>
<li id="ref-60">Ollama v0.40.1 source, runner preference for manifest lists (<code>runnerPreferences</code>): <a href="https://github.com/ollama/ollama/blob/v0.40.1/manifest/manifest.go">https://github.com/ollama/ollama/blob/v0.40.1/manifest/manifest.go</a></li>
<li id="ref-61">Ollama v0.40.1 source, <code>ollama ps</code> columns: <a href="https://github.com/ollama/ollama/blob/v0.40.1/cmd/cmd.go">https://github.com/ollama/ollama/blob/v0.40.1/cmd/cmd.go</a></li>
<li id="ref-62">OpenCode 2 docs, Models: <a href="https://opencode.ai/v2/docs/models">https://opencode.ai/v2/docs/models</a></li>
<li id="ref-63">OpenCode PR #53438, shared local provider discovery (in 2.0.24+): <a href="https://github.com/anomalyco/opencode/pull/53438">https://github.com/anomalyco/opencode/pull/53438</a></li>
<li id="ref-64">OpenCode 2 docs, Providers: <a href="https://opencode.ai/v2/docs/providers">https://opencode.ai/v2/docs/providers</a></li>
<li id="ref-65">OpenCode source, config model overrides applied after provider discovery (<code>packages/core/src/config/plugin/provider.ts</code>, production branch), and PR #55778 (in 2.0.31), configured limits seeded before model transforms: <a href="https://github.com/anomalyco/opencode/blob/production/packages/core/src/config/plugin/provider.ts">https://github.com/anomalyco/opencode/blob/production/packages/core/src/config/plugin/provider.ts</a> · <a href="https://github.com/anomalyco/opencode/pull/55778">https://github.com/anomalyco/opencode/pull/55778</a></li>
<li id="ref-66">OpenCode 2 docs, Compaction: <a href="https://opencode.ai/v2/docs/compaction">https://opencode.ai/v2/docs/compaction</a></li>
<li id="ref-67">OpenCode PR #57091, summarize the whole conversation during compaction (in 2.1.0; reserve 15%, at least 16k): <a href="https://github.com/anomalyco/opencode/pull/57091">https://github.com/anomalyco/opencode/pull/57091</a></li>
<li id="ref-68">OpenCode PR #57260, v2.1 minor breaking changes (&ldquo;Versions before v2.1 can&rsquo;t load a session that has a compaction created by v2.1&rdquo;): <a href="https://github.com/anomalyco/opencode/pull/57260">https://github.com/anomalyco/opencode/pull/57260</a></li>
<li id="ref-69">OpenCode PR #53685, reject malformed tool arguments (in 2.0.25): <a href="https://github.com/anomalyco/opencode/pull/53685">https://github.com/anomalyco/opencode/pull/53685</a></li>
<li id="ref-70">OpenCode config schema: <a href="https://opencode.ai/config.json">https://opencode.ai/config.json</a></li>
<li id="ref-71">OpenCode 2 docs, Agents: <a href="https://opencode.ai/v2/docs/agents">https://opencode.ai/v2/docs/agents</a></li>
<li id="ref-72">OpenCode 2 docs, MCP servers: <a href="https://opencode.ai/v2/docs/mcp-servers">https://opencode.ai/v2/docs/mcp-servers</a></li>
</ol>

<!-- STATE (read by the update process; not shown on the page)
refreshed: 2026-11-04
[source versions]
library_checked: 2026-11-02 18:00 UTC
opencode_stable: v2.2.5
ollama_stable: v0.40.13
aa_index_version: 5.0
aa_coding_column: terminalBench21
aa_coding_note: AA added terminalBench40 in 2026-10 (10% of Index v5.0); local candidates score near 0 on it, so terminalBench21 stays
aa_data: leaderboard initialModels (current models; scores nested in a scores object with kebab-case eval slugs since 2026-10-26, mapped in SCORE_SLUGS) plus a model page's models array (deprecated models; flat fields)
aa_general_score: GS = hle 10, lcr 5 (both required; legacy columns after Index v5.0). Omniscience penalty dropped 2026-11-02 (v5.0 replaced v1 with v1.1, v1 data removed); CritPt dropped 2026-11-04 (27 of 50 candidates score 0); both user decisions
vendor_tb_rule: vendor Terminal-Bench 2.1 counts only with the Terminus 2 harness (tb_harness in candidates.json; user decision 2026-11-04); ornith-1.5:122b (Claude Code) and nemotron-3.5-bolt:74b (harness unstated) dropped from coding
lmarena_column: General tables show LMArena text style-control rating (overall), not part of GS (user decision 2026-11-04); ratings from publish date in lmarena_publish_date
benchmarks_research: docs/research/benchmarks.md (2026-11-04)
lmarena_publish_date: 2026-10-28
macbook_pro_newest: MacBook Pro (14-inch, M5 Pro or M5 Max)
dell_next_gen_found: Dell Pro Precision 5 Series 16 PW516261 (added to Windows 32 GB tier 2026-10-15 at user request; link to MC16260 unconfirmed). 2026-11-02: probes pa14270, mc16260, mb16260, pw716261, pw516262 invalid; Dell Pro Precision 7 16 PW716260 exists but tops out at RTX PRO 3000 12 GB, so not an MB16250 successor (not added); Dell Pro Precision 5 16S PW516260 exists, integrated graphics only (not added)
flint_gguf: flint GGUF tags require Ollama 0.40.9 (stable 2026-10-22); 40b-a2b-gguf-nvfp4 carries vendor TB 53.7; llama.cpp b11963 (Ollama 0.40.13) still declines NVFP4 on Metal
two_bit_rule: 2-bit tags rankable only as the vendor's own quantization-aware release with no 4/8-bit tag (nemotron-3.5-bolt:74b-a9b-iq2); user decision 2026-10-26
mac_tag_choice: best build per model per tier, GGUF or MLX (MLX within 10% wins); user decision 2026-10-15
lfm3: lfm3 (vendor TB 12.9) and lfm3-vl/-audio/-omni have no AA score; recorded in candidates.json, not ranked
open_watched_issues: 19439,19273,19268,19191,18754,16279,18131,17426,15880,17362,18840,17778,18649,18390,18354,16383,18053,18530,17882,17562,11991,12203,17197,16992,17957,13820,17602,17638,17656,18269
fleet_sha256: 0334ec9a6f365048d565a176537d8ae5666ca27c985075a1167528b6a2c04742
candidates_sha256: f787f113931aa1cd7baec11800b6d3cd68a2da270e309c46a1d70dd2ebcbda22
[picks]
Mac M1 8 GB | general | 1 | qwen3:4b-thinking-2507-q4_K_M | GS 16.6
Mac M1 8 GB | general | 2 | granite4.2:3b-q4_K_M | GS 12.5
Mac M1 8 GB | general | 3 | granite4:1b-h-q8_0 | GS 5.7
Mac M1 8 GB | general | 4 | minicpm-v4.6:q4_K_M | GS 5.7
Mac M1 8 GB | general | 5 | qwen3.5:2b-q4_K_M | GS 8.7
Mac 8 GB | general | 1 | qwen3.5:4b-q4_K_M | GS 27.6
Mac 8 GB | general | 2 | qwen3:4b-thinking-2507-q4_K_M | GS 16.6
Mac 8 GB | general | 3 | granite4.2:3b-q4_K_M | GS 12.5
Mac 8 GB | general | 4 | qwen3.5:2b-q4_K_M | GS 8.7
Mac 8 GB | general | 5 | nemotron-3-nano:4b-nvfp4 | GS 10.5
Mac 8 GB | coding | 1 | qwen3.5:4b-q4_K_M | TB 25.8 flag
Mac M1 16 GB | general | 1 | qwen3:4b-thinking-2507-q4_K_M | GS 16.6
Mac M1 16 GB | general | 2 | granite4.2:3b-q4_K_M | GS 12.5
Mac M1 16 GB | general | 3 | granite4:1b-h-q8_0 | GS 5.7
Mac M1 16 GB | general | 4 | minicpm-v4.6:q4_K_M | GS 5.7
Mac M1 16 GB | general | 5 | qwen3.5:2b-q4_K_M | GS 8.7
Mac 16-24 GB | general | 1 | qwen3.5:9b-nvfp4 | GS 33.3
Mac 16-24 GB | general | 2 | gemma4:12b-nvfp4 | GS 31.7
Mac 16-24 GB | general | 3 | qwen3.5:4b-q4_K_M | GS 27.6
Mac 16-24 GB | general | 4 | granite4.2:8b-q4_K_M | GS 21.5
Mac 16-24 GB | general | 5 | qwen3:4b-thinking-2507-q4_K_M | GS 16.6
Mac 16-24 GB | coding | 1 | ornith-1.5:9b | TB 46.2 vendor
Mac 16-24 GB | coding | 2 | ornith:9b-q4_K_M | TB 43.1 vendor flag
Mac 16-24 GB | coding | 3 | qwen3.5:9b-nvfp4 | TB 29.2 flag
Mac 16-24 GB | coding | 4 | qwen3.5:4b-q4_K_M | TB 25.8 flag
Mac 16-24 GB | coding | 5 | gemma4:12b-nvfp4 | TB 27.3 flag
Mac 32-36 GB | general | 1 | qwen3.5:27b-int4 | GS 41.8
Mac 32-36 GB | general | 2 | qwen3.6:27b-q4_K_M | GS 41.2
Mac 32-36 GB | general | 3 | muse-glimmer:30b-nvfp4 | GS 42.4
Mac 32-36 GB | general | 4 | gemma4:26b-nvfp4 | GS 34.8
Mac 32-36 GB | general | 5 | qwen3.5:9b-nvfp4 | GS 33.3
Mac 32-36 GB | coding | 1 | ornith-1.5:35b | TB 67.8 vendor
Mac 32-36 GB | coding | 2 | ornith:35b-q4_K_M | TB 64.2 vendor flag
Mac 32-36 GB | coding | 3 | qwen3.8:27b-nvfp4 | TB 65.2 flag
Mac 32-36 GB | coding | 4 | qwen3.6:27b-q4_K_M | TB 60.7 flag
Mac 32-36 GB | coding | 5 | flint:40b-a2b-qat-int4 | TB 54.9 vendor
Mac 48-96 GB | general | 1 | qwen3.5:27b-int4 | GS 41.8
Mac 48-96 GB | general | 2 | qwen3.6:27b-nvfp4 | GS 41.2
Mac 48-96 GB | general | 3 | muse-glimmer:30b-nvfp4 | GS 42.4
Mac 48-96 GB | general | 4 | qwen3.5:35b-a3b-nvfp4 | GS 38.0
Mac 48-96 GB | general | 5 | qwen3.6:35b-a3b-nvfp4 | GS 38.7
Mac 48-96 GB | coding | 1 | ornith-1.5:35b | TB 67.8 vendor
Mac 48-96 GB | coding | 2 | ornith:35b-q4_K_M | TB 64.2 vendor flag
Mac 48-96 GB | coding | 3 | qwen3.8:27b-nvfp4 | TB 65.2 flag
Mac 48-96 GB | coding | 4 | qwen3.6:27b-nvfp4 | TB 60.7 flag
Mac 48-96 GB | coding | 5 | flint:40b-a2b-qat-int4 | TB 54.9 vendor
Mac 128 GB | general | 1 | qwen3.8-flash-next:125b-a6b-nvfp4 | GS 51.9
Mac 128 GB | general | 2 | qwen3.5:122b-a10b-q4_K_M | GS 42.3
Mac 128 GB | general | 3 | nemotron-3.5-super:120b-a12b-nvfp4 | GS 43.5
Mac 128 GB | general | 4 | qwen3.5:27b-int4 | GS 41.8
Mac 128 GB | general | 5 | qwen3.6:27b-nvfp4 | GS 41.2
Mac 128 GB | coding | 1 | qwen3.8-flash-next:125b-a6b-nvfp4 | TB 86.1 flag
Mac 128 GB | coding | 2 | ornith-1.5:35b | TB 67.8 vendor
Mac 128 GB | coding | 3 | ornith:35b-q4_K_M | TB 64.2 vendor flag
Mac 128 GB | coding | 4 | nemotron-3.5-super:120b-a12b-q4_K_M | TB 66.7 vendor
Mac 128 GB | coding | 5 | qwen3.8:27b-nvfp4 | TB 65.2 flag
Latitude 7350 | general | 1 | qwen3.5:4b-q4_K_M | GS 27.6
Latitude 7350 | general | 2 | qwen3:4b-thinking-2507-q4_K_M | GS 16.6
Latitude 7350 | general | 3 | granite4.2:3b-q4_K_M | GS 12.5
Latitude 7350 | general | 4 | qwen3.5:2b-q4_K_M | GS 8.7
Latitude 7350 | general | 5 | nemotron-3-nano:4b-q4_K_M | GS 10.5
Latitude 7350 | coding | 1 | qwen3.5:4b-q4_K_M | TB 25.8 flag
Windows 32 GB | general | 1 | gemma4:26b-a4b-it-qat | GS 34.8
Windows 32 GB | general | 2 | qwen3:30b-a3b-thinking-2507-q4_K_M | GS 27.3
Windows 32 GB | general | 3 | qwen3.5:4b-q4_K_M | GS 27.6
Windows 32 GB | general | 4 | north-mini-code-1.0:q4_K_M | GS 19.8
Windows 32 GB | general | 5 | gpt-oss:20b | GS 18.9
Windows 32 GB | coding | 1 | gemma4:26b-a4b-it-qat | TB 39.0 flag
Windows 32 GB | coding | 2 | north-mini-code-1.0:q4_K_M | TB 35.6 flag
Windows 32 GB | coding | 3 | qwen3.5:4b-q4_K_M | TB 25.8 flag
Pro Max 16 Plus, 8-16 GB GPU | general | 1 | qwen3.5:35b-a3b-q4_K_M | GS 38.0
Pro Max 16 Plus, 8-16 GB GPU | general | 2 | qwen3.6:35b-a3b-q4_K_M | GS 38.7
Pro Max 16 Plus, 8-16 GB GPU | general | 3 | nemotron-3.5-bolt:74b-a9b-iq2 | GS 39.7
Pro Max 16 Plus, 8-16 GB GPU | general | 4 | gemma4:26b-a4b-it-qat | GS 34.8
Pro Max 16 Plus, 8-16 GB GPU | general | 5 | qwen3.5:9b-q4_K_M | GS 33.3
Pro Max 16 Plus, 8-16 GB GPU | coding | 1 | ornith-1.5:35b | TB 67.8 vendor
Pro Max 16 Plus, 8-16 GB GPU | coding | 2 | ornith:35b-q4_K_M | TB 64.2 vendor flag
Pro Max 16 Plus, 8-16 GB GPU | coding | 3 | flint:40b-a2b-gguf-nvfp4 | TB 53.7 vendor
Pro Max 16 Plus, 8-16 GB GPU | coding | 4 | qwen3.6:35b-a3b-q4_K_M | TB 44.9 flag
Pro Max 16 Plus, 8-16 GB GPU | coding | 5 | ornith-1.5:9b | TB 46.2 vendor
Pro Max 16 Plus, 24 GB GPU | general | 1 | qwen3.5:27b-q4_K_M | GS 41.8
Pro Max 16 Plus, 24 GB GPU | general | 2 | qwen3.6:27b-q4_K_M | GS 41.2
Pro Max 16 Plus, 24 GB GPU | general | 3 | muse-glimmer:30b-q4_K_M | GS 42.4
Pro Max 16 Plus, 24 GB GPU | general | 4 | qwen3.5:35b-a3b-q4_K_M | GS 38.0
Pro Max 16 Plus, 24 GB GPU | general | 5 | qwen3.6:35b-a3b-q4_K_M | GS 38.7
Pro Max 16 Plus, 24 GB GPU | coding | 1 | ornith-1.5:35b | TB 67.8 vendor
Pro Max 16 Plus, 24 GB GPU | coding | 2 | ornith:35b-q4_K_M | TB 64.2 vendor flag
Pro Max 16 Plus, 24 GB GPU | coding | 3 | qwen3.8:27b-q4_K_M | TB 65.2 flag
Pro Max 16 Plus, 24 GB GPU | coding | 4 | qwen3.6:27b-q4_K_M | TB 60.7 flag
Pro Max 16 Plus, 24 GB GPU | coding | 5 | flint:40b-a2b-gguf-nvfp4 | TB 53.7 vendor
END STATE -->
