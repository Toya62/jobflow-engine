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

if [ -d "${PROJECT_ROOT}/dashboard/app" ]; then
  echo "--> Pushing dashboard/app/..."
  rsync -avzP \
    "${PROJECT_ROOT}/dashboard/app/" \
    "${REMOTE_HOST}:${REMOTE_PATH}/dashboard/app/"

  echo "--> Updating container dashboard/app..."
  ssh "${REMOTE_HOST}" "docker cp ${REMOTE_PATH}/dashboard/app karriere-dashboard:/app/dashboard/ 2>/dev/null || true"
fi

echo "=== Push completed successfully ==="
