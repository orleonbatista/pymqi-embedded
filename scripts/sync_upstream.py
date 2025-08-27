#!/usr/bin/env python3
"""Synchronize PyMQI sources and IBM MQ Client runtime from upstream."""

import os
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

def main() -> None:
    root_dir = Path(__file__).resolve().parent.parent
    build_dir = root_dir / ".build"
    src_dir = build_dir / "pymqi-src"
    root_pymqi = root_dir / "src" / "pymqi"
    vendor_dir = root_dir / "vendor" / "mq"
    mq_build_dir = build_dir / "mq-src"

    build_dir.mkdir(parents=True, exist_ok=True)

    pymqi_version = os.environ.get("PYMQI_VERSION", "1.13.1")
    embedded_suffix = os.environ.get("EMBEDDED_SUFFIX", "+embedded.2")
    sdist_path = Path(
        os.environ.get("PYMQI_SDIST_PATH", build_dir / f"pymqi-{pymqi_version}.tar.gz")
    )

    if src_dir.exists():
        shutil.rmtree(src_dir)
    src_dir.mkdir(parents=True)

    if not sdist_path.exists():
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "download",
                "--no-binary",
                ":all:",
                f"pymqi=={pymqi_version}",
                "-d",
                str(build_dir),
            ]
        )
        sdist_path = build_dir / f"pymqi-{pymqi_version}.tar.gz"

    with tarfile.open(sdist_path, "r:gz") as tf:
        tf.extractall(src_dir)
    extracted_root = next(src_dir.iterdir())

    if root_pymqi.exists():
        shutil.rmtree(root_pymqi)
    shutil.copytree(extracted_root / "pymqi", root_pymqi)

    version_file = root_pymqi / "_version.py"
    version_file.write_text(
        "__all__ = [\"__version__\"]\n\n__version__ = \"%s%s\"\n" % (pymqi_version, embedded_suffix),
        encoding="utf-8",
    )

    shutil.copy(extracted_root / "LICENSE", root_dir / "LICENSE-THIRD-PARTY")

    mq_client_tar_url = os.environ.get(
        "MQ_CLIENT_TAR_URL",
        "https://public.dhe.ibm.com/ibmdl/export/pub/software/websphere/messaging/mqdev/redist/9.3.5.0-IBM-MQC-Redist-LinuxX64.tar.gz",
    )
    mq_client_tar_path = Path(
        os.environ.get("MQ_CLIENT_TAR_PATH", build_dir / "mq-client.tar.gz")
    )

    if mq_client_tar_url or os.environ.get("MQ_CLIENT_TAR_PATH"):
        if vendor_dir.exists():
            shutil.rmtree(vendor_dir)
        if mq_build_dir.exists():
            shutil.rmtree(mq_build_dir)
        vendor_dir.mkdir(parents=True, exist_ok=True)
        mq_build_dir.mkdir(parents=True, exist_ok=True)

        if mq_client_tar_url and not mq_client_tar_path.exists():
            urllib.request.urlretrieve(mq_client_tar_url, mq_client_tar_path)

        with tarfile.open(mq_client_tar_path, "r:gz") as tf:
            tf.extractall(mq_build_dir)
        mq_src_dir = next(d for d in mq_build_dir.iterdir() if d.is_dir())

        license_script = mq_src_dir / "mqlicense.sh"
        if license_script.exists():
            subprocess.check_call([str(license_script), "-accept"])

        subprocess.check_call([str(mq_src_dir / "genmqpkg.sh"), "-b", str(vendor_dir)])

        inc_dir = vendor_dir / "inc"
        if inc_dir.exists():
            inc_dir.rename(vendor_dir / "include")

if __name__ == "__main__":
    main()
