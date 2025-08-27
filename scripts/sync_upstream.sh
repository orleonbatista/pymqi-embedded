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

# ---------------------------------------------------------------------------
# Optionally download and prepare the IBM MQ runtime
# ---------------------------------------------------------------------------
VENDOR_DIR="$ROOT_DIR/vendor/mq"
MQ_BUILD_DIR="$BUILD_DIR/mq-src"

if [[ -n "${MQ_CLIENT_TAR_PATH:-}" || -n "${MQ_CLIENT_TAR_URL:-}" ]]; then
  rm -rf "$VENDOR_DIR" "$MQ_BUILD_DIR"
  mkdir -p "$VENDOR_DIR" "$MQ_BUILD_DIR"

  MQ_CLIENT_TAR_PATH="${MQ_CLIENT_TAR_PATH:-$BUILD_DIR/mq-client.tar.gz}"
  if [[ -n "${MQ_CLIENT_TAR_URL:-}" && ! -f "$MQ_CLIENT_TAR_PATH" ]]; then
    curl -L "$MQ_CLIENT_TAR_URL" -o "$MQ_CLIENT_TAR_PATH"
  fi

  tar -xzf "$MQ_CLIENT_TAR_PATH" -C "$MQ_BUILD_DIR"
  MQ_SRC_DIR="$(find "$MQ_BUILD_DIR" -mindepth 1 -maxdepth 1 -type d | head -n1)"

  if [[ -x "$MQ_SRC_DIR/mqlicense.sh" ]]; then
    "$MQ_SRC_DIR/mqlicense.sh" -accept
  fi

  "$MQ_SRC_DIR/genmqpkg.sh" -b "$VENDOR_DIR"

  if [[ -d "$VENDOR_DIR/inc" ]]; then
    mv "$VENDOR_DIR/inc" "$VENDOR_DIR/include"
  fi
fi
