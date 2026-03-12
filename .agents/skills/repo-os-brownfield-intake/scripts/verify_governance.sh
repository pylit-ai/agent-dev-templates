#!/usr/bin/env bash
# Run governance checks if present.
set -e
ROOT="${1:-.}"
if [[ -f "$ROOT/scripts/check-governance" ]]; then
  "$ROOT/scripts/check-governance"
elif [[ -f "$ROOT/../scripts/check-governance" ]]; then
  "$ROOT/../scripts/check-governance"
else
  echo "No check-governance script found; skipping."
fi
