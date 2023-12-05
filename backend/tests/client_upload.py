import os

from zeno_client import ZenoClient


def test_initialize_client():
    API_KEY = os.environ.get("HUB_API_KEY")
    assert API_KEY is not None
    client = ZenoClient(API_KEY, endpoint="http://localhost:8000")
    assert client is not None
