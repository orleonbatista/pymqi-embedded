#!/usr/bin/env bash
set -euo pipefail

WHL="$1"
auditwheel repair "$WHL" -w dist
