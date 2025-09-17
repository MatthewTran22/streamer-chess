#!/usr/bin/env bash
set -euo pipefail

# Config
LISTEN_PORT="${LISTEN_PORT:-1936}"
RTMP_APP_PATH="${RTMP_APP_PATH:-/s/in}"
# Default to host.docker.internal so container can reach host's RTMP server on macOS/Windows
RTMP_FORWARD_URL="${RTMP_FORWARD_URL:-rtmp://host.docker.internal:1935/s/streamKey}"
FFMPEG_MODE="${FFMPEG_MODE:-copy}" # copy|transcode|off

echo "[startup] LISTEN_PORT=${LISTEN_PORT} RTMP_APP_PATH=${RTMP_APP_PATH}"
echo "[startup] Forwarding to ${RTMP_FORWARD_URL} (mode=${FFMPEG_MODE})"

start_ffmpeg_listener() {
  local input="rtmp://0.0.0.0:${LISTEN_PORT}${RTMP_APP_PATH}"
  if [[ "${FFMPEG_MODE}" == "off" ]]; then
    echo "[startup] FFMPEG_MODE=off → skipping listener"
    return 0
  fi

  if [[ "${FFMPEG_MODE}" == "copy" ]]; then
    echo "[ffmpeg] starting pass-through listener: ${input} → ${RTMP_FORWARD_URL}"
    ffmpeg -loglevel info -listen 1 -i "${input}" \
      -c copy -f flv "${RTMP_FORWARD_URL}" &
  else
    echo "[ffmpeg] starting transcode listener: ${input} → ${RTMP_FORWARD_URL}"
    ffmpeg -loglevel error -listen 1 -i "${input}" \
      -c:v libx264 -preset veryfast -tune zerolatency -g 30 -sc_threshold 0 \
      -c:a aac -ar 44100 -b:a 128k \
      -f flv "${RTMP_FORWARD_URL}" &
  fi
}

start_ffmpeg_listener

echo "[startup] launching backend"
exec python main.py


