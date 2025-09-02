import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

try:
    from setuptools import Extension, find_packages, setup
    import wheel.bdist_wheel  # noqa: F401 - ensure command is registered
except ModuleNotFoundError:  # pragma: no cover - executed only in lean envs
    for path in (
        "/usr/lib/python3/dist-packages",
        "/usr/local/lib/python3/dist-packages",
    ):
        if path not in sys.path:
            sys.path.append(path)
    from setuptools import Extension, find_packages, setup  # type: ignore
    import wheel.bdist_wheel  # type: ignore # noqa: F401

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"


def sync_upstream() -> None:
    """Fetch PyMQI and IBM MQ runtime from upstream sources."""
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "sync_upstream.py")])


if {"sdist", "bdist_wheel"} & set(sys.argv):
    sync_upstream()

PYMQI_VERSION = os.environ.get("PYMQI_VERSION", "1.12.11")
EMBEDDED_SUFFIX = os.environ.get("EMBEDDED_SUFFIX", "+embedded.2")
PACKAGE_VERSION = f"{PYMQI_VERSION}{EMBEDDED_SUFFIX}"

# ---------------------------------------------------------------------------
# Bundle MQ runtime into the wheel
# ---------------------------------------------------------------------------
vendor_mq = ROOT / "vendor" / "mq"
package_mq = SRC / "pymqi" / "_mq"
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
    extra_link_args.extend(["-Wl,-rpath,$ORIGIN", "-Wl,-rpath,$ORIGIN/_mq/lib"])

c_source = SRC / "pymqi" / "pymqi.c"
if not c_source.exists():
    c_source = SRC / "pymqi" / "_pymqi.c"

extension = Extension(
    "pymqi._pymqi",
    sources=[str(c_source)],
    include_dirs=[str(include_dir)],
    library_dirs=[str(lib_dir)],
    libraries=libraries,
    extra_link_args=extra_link_args,
)

long_description = (ROOT / "README.md").read_text(encoding="utf-8")

setup(
    name="pymqi-embedded",
    version=PACKAGE_VERSION,
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
    python_requires=">=3.8",
    install_requires=[],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"pymqi": package_data_files},
    ext_modules=[extension],
)
