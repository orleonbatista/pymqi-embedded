from __future__ import annotations

import os

import pymqi


def main() -> None:
    qmgr_name = os.environ.get("QMGR", "")
    qmgr = pymqi.QueueManager(qmgr_name)
    queue = pymqi.Queue(qmgr, "DEV.QUEUE")
    queue.put(b"ping")
    msg = queue.get()
    print(msg)


if __name__ == "__main__":
    if "MQSERVER" not in os.environ:
        raise SystemExit("MQSERVER not configured; skipping smoke test")
    main()
