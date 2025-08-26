from __future__ import annotations

import os
import sys
from pathlib import Path

from setuptools import Extension, setup

# Detect MQ installation
if os.name == "nt":
    DEFAULT_MQ_PATH = Path("C:/Program Files/IBM/MQ")
else:
    DEFAULT_MQ_PATH = Path("/opt/mqm")

MQ_INSTALLATION_PATH = Path(os.environ.get("MQ_INSTALLATION_PATH", DEFAULT_MQ_PATH))
INCLUDE_DIR = MQ_INSTALLATION_PATH / "inc"
LIB_DIR = MQ_INSTALLATION_PATH / ("lib64" if os.name != "nt" else "lib64")

if not (INCLUDE_DIR / "cmqc.h").exists():
    raise RuntimeError(
        "IBM MQ header files not found. Set MQ_INSTALLATION_PATH to IBM MQ Client installation."
    )

libraries = ["mqic_r" if os.name != "nt" else "mqic"]

extension = Extension(
    "pymqi._pymqi",
    sources=["src/pymqi/_pymqi.c"],
    include_dirs=[str(INCLUDE_DIR)],
    library_dirs=[str(LIB_DIR)],
    libraries=libraries,
)

setup(
    name="pymqi-embedded",
    version="1.13.1+embedded.1",
    package_dir={"": "src"},
    ext_modules=[extension],
)
