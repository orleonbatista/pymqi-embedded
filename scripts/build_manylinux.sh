#!/usr/bin/env bash
set -euo pipefail

# Build manylinux wheels bundling the IBM MQ Client.
# Provide MQ_CLIENT_TAR_URL or MQ_CLIENT_TAR_PATH to supply the MQ runtime.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR_DIR="$ROOT_DIR/vendor/mq"

rm -rf "$VENDOR_DIR"
mkdir -p "$VENDOR_DIR"

if [[ -n "${MQ_CLIENT_TAR_PATH:-}" ]]; then
  tar -xzf "$MQ_CLIENT_TAR_PATH" -C "$VENDOR_DIR" --strip-components=1
elif [[ -n "${MQ_CLIENT_TAR_URL:-}" ]]; then
  curl -L "$MQ_CLIENT_TAR_URL" | tar -xz -C "$VENDOR_DIR" --strip-components=1
else
  echo "Provide MQ_CLIENT_TAR_URL or MQ_CLIENT_TAR_PATH" >&2
  exit 1
fi

"$ROOT_DIR/scripts/sync_upstream.sh"

for PYVER in cp38 cp39 cp310 cp311 cp312; do
  PYBIN="/opt/python/${PYVER}/bin"
  MQ_INSTALLATION_PATH="$VENDOR_DIR" "$PYBIN/python" -m build --wheel
  for whl in dist/pymqi_embedded-*.whl; do
    "$ROOT_DIR/scripts/repair_manylinux.sh" "$whl"
  done
  rm -rf build pymqi_embedded.egg-info dist/pymqi_embedded-*.whl
  git checkout -- src/pymqi
  "$ROOT_DIR/scripts/sync_upstream.sh"
done
