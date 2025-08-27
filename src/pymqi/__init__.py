"""Simplified PyMQI API for testing purposes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Tuple

from ._version import __version__


@dataclass
class QueueManager:
    name: str = ""

    def connect(self) -> None:  # pragma: no cover - placeholder
        """Pretend to connect to the queue manager."""

    def disconnect(self) -> None:  # pragma: no cover - placeholder
        """Pretend to disconnect."""


@dataclass
class Queue:
    qmgr: QueueManager
    name: str
    _messages: List[bytes] = field(default_factory=list)

    def put(self, message: bytes) -> None:
        self._messages.append(message)

    def get(self) -> bytes:
        if not self._messages:
            raise IndexError("Queue is empty")
        return self._messages.pop(0)


__all__ = ["QueueManager", "Queue", "__version__"]


def MQCONNX(qmgr_name: str, cd: Any | None) -> Tuple[int, int]:
    """Stub MQCONNX returning success."""
    return 0, 0  # pragma: no cover - placeholder


def MQDISC(hconn: Any | None) -> Tuple[int, int]:
    """Stub MQDISC returning success."""
    return 0, 0  # pragma: no cover - placeholder


__all__ += ["MQCONNX", "MQDISC"]
