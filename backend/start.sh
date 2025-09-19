#!/usr/bin/env bash
set -euo pipefail

echo "[startup] Streamer Chess Backend - FastAPI only"
echo "[startup] MediaMTX handles all streaming (RTMP->RTSP conversion)"
echo "[startup] Backend connects to MediaMTX RTSP stream for video analysis"

echo "[startup] launching FastAPI backend"
exec python main.py


