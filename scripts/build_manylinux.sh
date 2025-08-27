#!/usr/bin/env bash
set -euo pipefail

# Build manylinux wheels bundling the IBM MQ Client.
# Downloads the MQ runtime if not supplied via MQ_CLIENT_TAR_URL or MQ_CLIENT_TAR_PATH.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR_DIR="$ROOT_DIR/vendor/mq"

rm -rf "$VENDOR_DIR"

MQ_CLIENT_TAR_URL="${MQ_CLIENT_TAR_URL:-https://public.dhe.ibm.com/ibmdl/export/pub/software/websphere/messaging/mqdev/redist/9.3.5.0-IBM-MQC-Redist-LinuxX64.tar.gz}"

"$ROOT_DIR/scripts/sync_upstream.sh"

unset MQ_CLIENT_TAR_URL MQ_CLIENT_TAR_PATH

for PYVER in cp36 cp37 cp38 cp39 cp310 cp311 cp312; do
  PYBIN="/opt/python/${PYVER}/bin"
  MQ_INSTALLATION_PATH="$VENDOR_DIR" "$PYBIN/python" -m build --wheel
  for whl in dist/pymqi_embedded-*.whl; do
    "$ROOT_DIR/scripts/repair_manylinux.sh" "$whl"
  done
  rm -rf build pymqi_embedded.egg-info dist/pymqi_embedded-*.whl
  git checkout -- src/pymqi
  "$ROOT_DIR/scripts/sync_upstream.sh"
done
