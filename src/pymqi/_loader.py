"""Native IBM MQ client loader with no side effects on import."""

from __future__ import annotations

import ctypes
import sys
from pathlib import Path
from typing import List


def _mq_lib_paths() -> List[str]:
    base = Path(__file__).parent / "_mq"
    candidates: List[str] = []
    if sys.platform.startswith("win"):
        candidates += [str(base / "bin"), str(base / "lib")]
        names = ["mqic_r.dll", "mqic.dll"]
    else:
        candidates += [str(base / "lib64"), str(base / "lib")]
        names = ["libmqic_r.so", "libmqic.so"]
    return [str(Path(d) / n) for d in candidates for n in names]


def load_mq_client() -> ctypes.CDLL:
    last: OSError | None = None
    for path in _mq_lib_paths():
        try:
            return ctypes.CDLL(path)
        except OSError as exc:  # pragma: no cover - depends on environment
            last = exc
    names = (
        ["mqic_r.dll", "mqic.dll"]
        if sys.platform.startswith("win")
        else [
            "libmqic_r.so",
            "libmqic.so",
        ]
    )
    for name in names:
        try:
            return ctypes.CDLL(name)
        except OSError as exc:  # pragma: no cover - depends on environment
            last = exc
    msg = "IBM MQ client not found in packaged libs or system"
    if last:
        msg += f": {last}"
    raise OSError(msg)
