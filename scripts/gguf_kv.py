#!/usr/bin/env python3
"""KV-cache size of an Ollama GGUF tag at a context length, from the model file's header.

Reads only the header (ranged GETs), never the weights.
Usage: scripts/gguf_kv.py <model:tag> ...   # prints GB at 64k and 128k context
"""
import json
import struct
import sys
import urllib.request

REGISTRY = "https://registry.ollama.ai/v2/library"
CONTEXT = 65536
# llama.cpp's per-architecture value when the GGUF omits full_attention_interval
# (src/models/qwen3next.cpp: full_attn_interval = 4).
DEFAULT_FULL_ATTENTION_INTERVAL = {"qwen3next": 4}
SCALARS = {0: "B", 1: "b", 2: "H", 3: "h", 4: "I", 5: "i", 6: "f", 7: "?", 10: "Q", 11: "q", 12: "d"}


def manifest(tag):
    model, name = tag.split(":")
    request = urllib.request.Request(f"{REGISTRY}/{model}/manifests/{name}",
                                     headers={"Accept": "application/vnd.docker.distribution.manifest.v2+json"})
    return model, json.loads(urllib.request.urlopen(request, timeout=60).read())


class Reader:
    def __init__(self, url):
        self.url, self.buffer, self.position = url, b"", 0

    def read(self, size):
        while self.position + size > len(self.buffer):
            start = len(self.buffer)
            request = urllib.request.Request(self.url, headers={"Range": f"bytes={start}-{start + max(size, 8 << 20) - 1}"})
            self.buffer += urllib.request.urlopen(request, timeout=120).read()
        data = self.buffer[self.position:self.position + size]
        self.position += size
        return data

    def unpack(self, fmt):
        return struct.unpack("<" + fmt, self.read(struct.calcsize(fmt)))[0]

    def string(self):
        return self.read(self.unpack("Q")).decode("utf-8", "replace")


def value(reader, kind, keep):
    if kind in SCALARS:
        return reader.unpack(SCALARS[kind])
    if kind == 8:
        return reader.string()
    if kind == 9:
        item, count = reader.unpack("I"), reader.unpack("Q")
        if not keep and item in SCALARS:
            reader.read(struct.calcsize(SCALARS[item]) * count)
            return None
        return [value(reader, item, keep) for _ in range(count)]
    raise ValueError(f"Unknown GGUF value type {kind}")


def header(tag):
    model, data = manifest(tag)
    layer = next(item for item in data["layers"] if item["mediaType"].endswith(".model"))
    reader = Reader(f"{REGISTRY}/{model}/blobs/{layer['digest']}")
    if reader.read(4) != b"GGUF":
        raise ValueError(f"{tag} is not a GGUF model")
    reader.unpack("I")
    reader.unpack("Q")
    metadata = {}
    for _ in range(reader.unpack("Q")):
        key, kind = reader.string(), reader.unpack("I")
        keep = not key.startswith("tokenizer.")  # vocabularies are large and unused here
        result = value(reader, kind, keep)
        if keep:
            metadata[key] = result
    return metadata


def kv_gb(metadata, context=CONTEXT):
    """f16 K+V for attention layers only; sliding-window layers hold just the window."""
    arch = metadata["general.architecture"]
    get = lambda key: metadata.get(f"{arch}.{key}")
    layers = get("block_count")
    heads = get("attention.head_count_kv")
    heads = heads if isinstance(heads, list) else [heads] * layers
    head_count = get("attention.head_count")
    key_length = get("attention.key_length") or get("embedding_length") // (
        max(head_count) if isinstance(head_count, list) else head_count)
    value_length = get("attention.value_length") or key_length
    interval = get("full_attention_interval") or DEFAULT_FULL_ATTENTION_INTERVAL.get(arch)
    window, pattern = get("attention.sliding_window"), get("attention.sliding_window_pattern")
    total = 0
    for layer in range(layers):
        if not heads[layer] or (interval and (layer + 1) % interval):
            continue  # recurrent / linear-attention layer
        tokens = context
        if window:
            sliding = pattern[layer] if isinstance(pattern, list) else bool(pattern and (layer + 1) % pattern)
            if sliding:
                tokens = min(context, window)
        total += heads[layer] * (key_length + value_length) * 2 * tokens
    return total / 1e9


if __name__ == "__main__":
    for tag in sys.argv[1:]:
        meta = header(tag)
        print(f"{tag}\tkv64k={kv_gb(meta):.2f}GB\tkv128k={kv_gb(meta, 131072):.2f}GB")
