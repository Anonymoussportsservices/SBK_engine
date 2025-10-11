#!/usr/bin/env bash
# start.sh - entrypoint for Render (or use uvicorn directly in Render start command)
PORT=${PORT:-10000}
exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1