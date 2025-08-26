import pymqi


def test_import() -> None:
    assert pymqi.QueueManager is not None
    assert pymqi.Queue is not None
