#!/usr/bin/env bash
set -euxo pipefail

# This script is intended to run inside a manylinux Docker container.
# It downloads the IBM MQ client and builds wheels for multiple Python versions.

MQ_URL="https://example.com/ibm-mq-client.tar.gz"  # Placeholder URL

for PYVER in cp38 cp39 cp310 cp311 cp312; do
    PYBIN="/opt/python/${PYVER}/bin"
    "${PYBIN}/python" -m pip install --upgrade pip setuptools wheel
    "${PYBIN}/python" -m pip wheel . -w /tmp/wheels
    for whl in /tmp/wheels/pymqi_embedded-*.whl; do
        auditwheel repair "$whl" -w dist
    done
    rm -rf /tmp/wheels
done
