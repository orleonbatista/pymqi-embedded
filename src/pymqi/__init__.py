"""Lightweight package init exporting the public API."""

from __future__ import annotations

from ._core import MQCONNX, MQDISC, Queue, QueueManager
from ._version import __version__

__all__ = [
    "QueueManager",
    "Queue",
    "MQCONNX",
    "MQDISC",
    "__version__",
]
