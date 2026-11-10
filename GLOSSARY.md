# Local Models

Choosing which open-weight models to run locally, through Ollama and OpenCode, on the company's fleet of Mac and Windows laptops.

## Language

### Hardware

**Machine**:
A specific laptop model and memory configuration in the fleet (e.g. MacBook Pro M3 Pro 36 GB, Dell Pro Max 16 32 GB).
_Avoid_: Device, box, computer

**Hardware tier**:
A group of Machines that can run the same set of models, defined by the memory usable for model weights plus context.
_Avoid_: Class, bucket, spec level

**Stack**:
The software every Top model is configured for: the stable OpenCode line (2.x since 2026-10-05, by the user's call) connected to the latest stable Ollama, pulling models from the Ollama library. Betas and release candidates never count.
_Avoid_: Toolchain, setup

### Use

**Use case**:
One of exactly two jobs a model is ranked for: General use or Agentic coding.
_Avoid_: Workload, scenario

**General use**:
Chat-style work: Q&A, writing, summarising, reasoning, without autonomous tool use.
_Avoid_: Generic, chat

**Agentic coding**:
Software development with the model in OpenCode: given a task, the model reads, edits and runs code through OpenCode's tools (multi-step, tool-calling work).
_Avoid_: Coding assistant, code completion

### Ranking

**Top model**:
One of the 5 highest-quality models for a Hardware tier and Use case that supports tool calling in Ollama, fits the tier's memory with 64k context, and has an Estimated speed of roughly 15+ tokens/sec on at least one Machine in the tier.
_Avoid_: Best model, recommended model

**General score (GS)**:
The score that ranks General use: a weighted mean of HLE 10 and AA-LCR 5, two non-agentic, non-coding evals of the AA Intelligence Index up to v4.3.2 (AA's legacy columns since v5.0). AA-Omniscience (since 2026-11-02) and CritPt (since 2026-11-04) are left out. LMArena ratings are shown beside it, not part of it.
_Avoid_: Intelligence Index (it is about half agentic and coding work), II

**Equivalent paid model**:
The paid, hosted model whose scores on the best public benchmarks for that Use case are closest to the local model's. Marked "low confidence" when the local model's score is vendor-reported rather than measured by AA.
_Avoid_: Comparable model, cloud equivalent

### Process

**Report**:
The single current HTML page listing Top models per Hardware tier and Use case; each Refresh replaces it.
_Avoid_: Snapshot, recommendation doc

**Refresh**:
One full re-run of the research and ranking that produces a new Report plus a Diff against the previous one.
_Avoid_: Update, rerun, regeneration

**Diff**:
The list of what changed between the previous Report and the new one (picks added, dropped or moved; Machines added; config changes), read from the previous Report just before it is replaced and told to the user at the end of a Refresh, never written into the Report.
_Avoid_: Changelog, delta

**Change check**:
A cheap test for whether anything upstream (models, benchmarks, Ollama, OpenCode, or Machines in the fleet) has changed enough to justify a Refresh.
_Avoid_: Monitor, watcher

**Runbook**:
The written procedure an agent follows to perform a Refresh.
_Avoid_: Playbook, process doc

**Estimated speed**:
Tokens/sec predicted from memory bandwidth divided by the size of the weights active per token; never measured on a real Machine.
_Avoid_: Benchmark speed, measured speed
