#!/usr/bin/env bash
# Keep the documented CLI and exit codes; testable logic lives in check_changes.py.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/check_changes.py
