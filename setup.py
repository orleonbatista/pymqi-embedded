import os
import shutil
from pathlib import Path
from typing import List

from setuptools import Extension, find_packages, setup

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

# ---------------------------------------------------------------------------
# Bundle MQ runtime into the wheel
# ---------------------------------------------------------------------------
vendor_mq = ROOT / "vendor" / "mq"
package_mq = SRC / "pymqi" / "mq"
package_data_files: List[str] = []
if vendor_mq.exists():
    if package_mq.exists():
        shutil.rmtree(package_mq)
    shutil.copytree(vendor_mq, package_mq)
    package_data_files = [
        str(path.relative_to(package_mq.parent))
        for path in package_mq.rglob("*")
        if path.is_file()
    ]

# ---------------------------------------------------------------------------
# Locate MQ headers and libraries
# ---------------------------------------------------------------------------
candidates = []
if "MQ_INSTALLATION_PATH" in os.environ:
    candidates.append(Path(os.environ["MQ_INSTALLATION_PATH"]))
candidates.append(vendor_mq)
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
extra_link_args: List[str] = []
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

long_description = (ROOT / "README.md").read_text(encoding="utf-8")

setup(
    name="pymqi-embedded",
    version="1.13.1+embedded.2",
    description="Embedded distribution of PyMQI bundling the IBM MQ runtime libraries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Proprietary",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    install_requires=["dataclasses; python_version < '3.7'"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"pymqi": package_data_files},
    ext_modules=[extension],
)
