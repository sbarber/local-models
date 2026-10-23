"""Pure change-detection checks shared by the CLI and unit tests."""

import hashlib

from aa import row


def content_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def score_changes(models, candidates):
    live = {m["name"]: row(m) for m in models}
    reasons = []
    for candidate in candidates:
        name = candidate.get("aa_name")
        if not name:
            continue  # vendor-only score
        if name not in live:
            reasons.append(f"AA no longer lists {name}")
            continue
        actual = live[name]
        for field, key in (("gs", "gs"), ("tb21", "tb")):
            if key == "tb" and candidate["score_source"] == "vendor":
                continue
            if actual[field] != candidate[key]:
                reasons.append(f"AA {name} {key}: {candidate[key]} -> {actual[field]}")
    return reasons


def updated_models(library, refreshed):
    """Models updated after `refreshed`: a date (YYYY-MM-DD, whole day counted as seen)
    or a UTC time (YYYY-MM-DD HH:MM), so same-day updates after a Refresh are caught."""
    from datetime import datetime

    if len(refreshed) > 10:
        since, key = datetime.strptime(refreshed.replace(" UTC", ""), "%Y-%m-%d %H:%M"), lambda u: u
    else:
        since, key = datetime.strptime(refreshed, "%Y-%m-%d").date(), lambda u: u.date()
    changed = []
    for model in library:
        if not model["updated"]:
            continue
        updated = datetime.strptime(model["updated"].replace(" UTC", ""), "%b %d, %Y %I:%M %p")
        # A cloud badge doesn't imply cloud-only (e.g. Gemma has local tags).
        if key(updated) > since:
            changed.append(model["name"])
    return changed
