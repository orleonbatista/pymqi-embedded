from __future__ import annotations

import os
from pathlib import Path

from setuptools import Extension, find_packages, setup

ROOT = Path(__file__).resolve().parent

candidates = []
if "MQ_INSTALLATION_PATH" in os.environ:
    candidates.append(Path(os.environ["MQ_INSTALLATION_PATH"]))
candidates.append(ROOT / "vendor" / "mq")
if os.name == "nt":
    candidates.append(Path(r"C:/Program Files/IBM/MQ"))
else:
    candidates.append(Path("/opt/mqm"))

include_dir = lib_dir = None
for base in candidates:
    inc = base / "include"
    lib = base / ("lib64" if (base / "lib64").exists() else "lib")
    if (inc / "cmqc.h").exists():
        include_dir = inc
        lib_dir = lib
        break

if include_dir is None or lib_dir is None:
    msg = (
        "IBM MQ Client headers or libraries not found. "
        "Set MQ_INSTALLATION_PATH, place files under vendor/mq, "
        "or install the client to the system default path."
    )
    raise RuntimeError(msg)

libraries = ["mqic_r"]
extra_link_args = []
if os.name != "nt":
    extra_link_args.append("-Wl,-rpath,$ORIGIN")

extension = Extension(
    "pymqi._pymqi",
    sources=["src/pymqi/_pymqi.c"],
    include_dirs=[str(include_dir)],
    library_dirs=[str(lib_dir)],
    libraries=libraries,
    extra_link_args=extra_link_args,
)

setup(
    name="pymqi-embedded",
    version="1.13.1+embedded.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=[extension],
)
