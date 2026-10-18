#!/usr/bin/env sh
set -eu

cd /app
export PYTHONUNBUFFERED=1

# Keep Python as PID 1 so Render receives shutdown signals and logs stream immediately.
exec python -u -m bot
