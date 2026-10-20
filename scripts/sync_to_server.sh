#!/usr/bin/env bash
# Push data/ and applications/ from local Mac to Oracle Cloud server
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
REMOTE_HOST="oracle-server"
REMOTE_PATH="/opt/karriere-pipeline"

echo "=== Pushing to ${REMOTE_HOST}:${REMOTE_PATH} ==="

echo "--> Pushing data/..."
rsync -avzP \
  "${PROJECT_ROOT}/data/" \
  "${REMOTE_HOST}:${REMOTE_PATH}/data/"

echo "--> Pushing applications/..."
rsync -avzP \
  "${PROJECT_ROOT}/applications/" \
  "${REMOTE_HOST}:${REMOTE_PATH}/applications/"

echo "=== Push completed successfully ==="
