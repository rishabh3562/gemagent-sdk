# sdk/stream.py
import asyncio, re
from types import SimpleNamespace

class STREAM_SIM:
    def __init__(self, full_text):
        self._tokens = re.findall(r'\w+|[^\w\s]|\s+', full_text)

    async def stream_events(self):
        for token in self._tokens:
            await asyncio.sleep(0.04)
            yield SimpleNamespace(type="delta", data=SimpleNamespace(delta=token))
