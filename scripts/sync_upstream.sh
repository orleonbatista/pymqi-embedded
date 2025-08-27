#!/usr/bin/env bash
set -euo pipefail

# Synchronise PyMQI upstream into src/pymqi/
# Usage: PYMQI_VERSION=1.13.1 scripts/sync_upstream.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="$ROOT_DIR/.build"
SRC_DIR="$BUILD_DIR/pymqi-src"

PYMQI_VERSION="${PYMQI_VERSION:-1.13.1}"
SDIST_URL="https://files.pythonhosted.org/packages/source/p/pymqi/pymqi-${PYMQI_VERSION}.tar.gz"
SDIST_PATH="${PYMQI_SDIST_PATH:-$BUILD_DIR/pymqi-${PYMQI_VERSION}.tar.gz}"

rm -rf "$SRC_DIR"
mkdir -p "$SRC_DIR"
mkdir -p "$ROOT_DIR/src/pymqi"

if [ ! -f "$SDIST_PATH" ]; then
  curl -L "$SDIST_URL" -o "$SDIST_PATH"
fi

tar -xzf "$SDIST_PATH" -C "$SRC_DIR" --strip-components=1
rsync -a --delete "$SRC_DIR/pymqi/" "$ROOT_DIR/src/pymqi/"

# Preserve upstream license
LICENSE_DST="$ROOT_DIR/LICENSE-THIRD-PARTY"
cp "$SRC_DIR/LICENSE" "$LICENSE_DST"
