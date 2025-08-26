import os

import pytest

import pymqi


@pytest.mark.skipif("MQSERVER" not in os.environ, reason="MQSERVER not configured")
def test_smoke() -> None:
    qmgr = pymqi.QueueManager("")
    queue = pymqi.Queue(qmgr, "DEV.QUEUE")
    queue.put(b"hello")
    assert queue.get() == b"hello"
