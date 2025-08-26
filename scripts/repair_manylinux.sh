#!/usr/bin/env bash
set -euxo pipefail

WHL="$1"
auditwheel repair "$WHL" -w dist
