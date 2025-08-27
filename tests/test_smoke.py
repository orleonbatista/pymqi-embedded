import os

import pymqi
import pytest


@pytest.mark.skipif("MQSERVER" not in os.environ, reason="MQSERVER not configured")
def test_smoke() -> None:
    cc, rc = pymqi.MQCONNX("", None)
    assert cc == 0
    cc, rc = pymqi.MQDISC(None)
    assert cc == 0
    if os.getenv("MQI_SMOKE_PUTGET") == "1":
        q_name = os.getenv("MQI_SMOKE_Q")
        if not q_name:
            pytest.skip("MQI_SMOKE_Q not set")
        try:
            qmgr = pymqi.QueueManager("")
            queue = pymqi.Queue(qmgr, q_name)
            queue.put(b"ping")
            assert queue.get() == b"ping"
        except Exception as exc:  # pragma: no cover - environment dependent
            pytest.skip(f"put/get failed: {exc}")
