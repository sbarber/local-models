#!/usr/bin/env python3
"""Rank snapshot candidates against the fleet without downloading or running models.

Update candidates.json from primary sources during a Refresh, then run this
script and copy its output to the report. Sizes/scores are dated estimates,
not live benchmarks. PyYAML is the only non-stdlib dependency.
"""

import argparse
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_data(root=ROOT):
    fleet = yaml.safe_load((root / "machines.yaml").read_text())
    candidates = json.loads((root / "candidates.json").read_text())["models"]
    return fleet, candidates


def machines_for_tier(fleet, tier):
    return [
        (machine, memory)
        for machine in fleet["machines"]
        for memory in machine["memory_gb"]
        if machine["tiers"].get(memory) == tier
    ]


CONTEXT = 65536  # OpenCode's minimum, per Ollama's OpenCode integration docs
MIN_GENERAL_CONTEXT = 4096  # Ollama's default context below 24 GiB of GPU memory
MAC_RAISED_LIMIT = 0.8  # raised GPU limit on Macs up to 36 GB; the report's 32/36 GB examples are 26000/29000 MB


def in_vram(machine, size, tag, use):
    vram = machine.get("gpu_vram_gb", 0)
    if not vram or size > vram - 3:
        return False
    return use != "coding" or size + tag["kv64k_gb"] <= vram


def bandwidth(machine, size, tag, use, high=False):
    if in_vram(machine, size, tag, use):
        return machine["gpu_bandwidth_gbs"]
    ram = machine["bandwidth_gbs"]
    return (max(ram) if high else min(ram)) if isinstance(ram, list) else ram


def tag_size(tag):
    # The tags page rounds GGUF sizes; MLX manifests have precise layer sizes.
    return round(tag["size_gb"], 1) if tag["format"] == "mlx" else tag["size_gb"]


def speed(model, size, bw):
    read_gb = size * (model["active"] / model["total"]) if model["active"] else size
    return 0.6 * bw / read_gb


def context_budget(tier, machine, memory, tag, size):
    """Memory for weights + context, assuming the Mac GPU limit is raised."""
    if tier.startswith("Mac"):
        return memory * MAC_RAISED_LIMIT if memory <= 36 else memory - 16
    vram = machine.get("gpu_vram_gb", 0)
    if vram and size <= vram - 3 and size + tag["kv64k_gb"] <= vram:
        return vram
    return memory - 10


def fits(tier, machine, memory, tag, size, use="general"):
    # Coding needs 64k context, so it always counts context memory. General use
    # on Macs up to 36 GB and on Dells is fit on weights; max_context() then
    # says how much context those picks have room for.
    if use == "coding" or (tier.startswith("Mac") and memory > 36):
        return size + tag["kv64k_gb"] <= context_budget(tier, machine, memory, tag, size)
    if tier.startswith("Mac"):
        return size <= memory * 0.6
    vram = machine.get("gpu_vram_gb", 0)
    return (vram and size <= vram - 3) or size <= memory - 10


def max_context(tier, machines, tag, size):
    """Largest standard num_ctx (<= 64k) whose context fits every machine."""
    if not tag["kv64k_gb"]:
        return CONTEXT
    room = min(context_budget(tier, m, mem, tag, size) - size for m, mem in machines)
    for ctx in (65536, 32768, 16384, 8192, 4096):
        if tag["kv64k_gb"] * ctx / CONTEXT <= room:
            return ctx
    return 0


def choose_tag(model, tier, machines, use):
    mac = tier.startswith("Mac")
    options = []
    for name, tag in model["tags"].items():
        if tag["format"] == "mlx" and not mac:
            continue
        size = tag_size(tag)
        if not all(fits(tier, machine, memory, tag, size, use) for machine, memory in machines):
            continue
        speeds = [speed(model, size, bandwidth(machine, size, tag, use)) for machine, _ in machines]
        if max(speeds) < 15:
            continue
        maximum = max(speed(model, size, bandwidth(machine, size, tag, use, high=True)) for machine, _ in machines)
        options.append((name, tag, size, speeds, maximum))
    if not options:
        return None
    fastest = max(options, key=lambda option: min(option[3]))
    chosen = fastest
    if mac:
        eligible = [
            option for option in options
            if option[1]["format"] == "mlx"
            and min(option[3]) >= min(fastest[3]) * 0.9
            and all(fast < 15 or preferred >= 15
                    for fast, preferred in zip(fastest[3], option[3]))
        ]
        if eligible:
            chosen = min(eligible, key=lambda option: (
                "nvfp4" not in option[0], -min(option[3])
            ))
    # A vendor's score for a particular quantized tag is not transferable.
    if use == "coding" and model["tag_tb"]:
        best_score = max(options, key=lambda option: model["tag_tb"].get(option[0], model["tb"]))
        if model["tag_tb"].get(best_score[0], model["tb"]) - model["tag_tb"].get(chosen[0], model["tb"]) > 3:
            chosen = best_score
    return chosen, min(fastest[3])


def rank(fleet, candidates, tier, use):
    machines = machines_for_tier(fleet, tier)
    if not machines:
        raise ValueError(f"No machines in {tier}")
    rows = []
    for model in candidates:
        result = choose_tag(model, tier, machines, use)
        if result is None:
            continue
        (tag, data, size, speeds, maximum), fastest_speed = result
        if use == "general" and max_context(tier, machines, data, size) < MIN_GENERAL_CONTEXT:
            continue
        score = model["gs"] if use == "general" else model["tag_tb"].get(tag, model["tb"])
        if score is None or (use == "coding" and score < 20):
            continue
        rows.append({
            "tag": tag, "score": score, "speed_min": min(speeds), "speed_max": maximum,
            "machine_speeds": speeds, "rank_speed": fastest_speed,
            "vendor": use == "coding" and (model["score_source"] == "vendor" or tag in model["tag_tb"]),
            # Tags of one model can use different parsers (e.g. an MLX tag with a parser,
            # a GGUF tag with none), so a tag-level flag overrides the model's.
            "flag": use == "coding" and model.get("tag_flag", {}).get(tag, model["flag"]),
            "max_context": max_context(tier, machines, data, size),
        })
    rows.sort(key=lambda row: -row["score"])
    changed = True
    while changed:
        changed = False
        for i in range(len(rows) - 1):
            a, b = rows[i:i + 2]
            if a["score"] - b["score"] <= 3 and b["rank_speed"] > a["rank_speed"]:
                rows[i:i + 2] = b, a
                changed = True
    top = rows[:5]
    if top and not any(all(s >= 15 for s in row["machine_speeds"]) for row in top):
        fallback = next((row for row in rows[5:] if all(s >= 15 for s in row["machine_speeds"])), None)
        if fallback:
            top[-1] = fallback
    return top


def formatted_speed(row):
    low, high = round(row["speed_min"]), round(row["speed_max"])
    return f"~{low}" if low == high else f"{low}-{high}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit picks as JSON")
    args = parser.parse_args()
    fleet, candidates = load_data()
    result = {
        tier: {use: rank(fleet, candidates, tier, use) for use in ("general", "coding")}
        for tier in fleet["tiers"]
    }
    if args.json:
        print(json.dumps(result, indent=2))
        return
    for tier, uses in result.items():
        for use, rows in uses.items():
            print(f"== {tier} | {use}")
            for i, row in enumerate(rows, 1):
                label = "GS" if use == "general" else "TB"
                flag = " (vendor)" if row["vendor"] else ""
                flag += " ⚠" if row["flag"] else ""
                print(f"  {i} {row['tag']:48} {label} {row['score']:.1f}{flag}  {formatted_speed(row)}")


if __name__ == "__main__":
    main()
