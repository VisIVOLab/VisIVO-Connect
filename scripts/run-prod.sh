#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

: "${VISIVO_HOST:=0.0.0.0}"
: "${VISIVO_PORT:=8080}"
: "${VISIVO_LOG_LEVEL:=INFO}"

if [[ ! -x .venv/bin/python ]]; then
  echo "Missing virtualenv at .venv/bin/python" >&2
  exit 1
fi

exec .venv/bin/python -m uvicorn backend.main:app \
  --host "$VISIVO_HOST" \
  --port "$VISIVO_PORT" \
  --loop asyncio \
  --log-level "${VISIVO_LOG_LEVEL,,}"
