"""Minimal PyMQI-like API with lazy native loader."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple

from ._loader import load_mq_client


@dataclass
class QueueManager:
    name: str = ""

    def connect(self) -> None:
        load_mq_client()  # lazy load on demand

    def disconnect(self) -> None:
        load_mq_client()


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


def MQCONNX(qmgr_name: str, cd: Optional[Any]) -> Tuple[int, int]:
    load_mq_client()
    return 0, 0


def MQDISC(hconn: Optional[Any]) -> Tuple[int, int]:
    load_mq_client()
    return 0, 0


__all__ = ["QueueManager", "Queue", "MQCONNX", "MQDISC"]
