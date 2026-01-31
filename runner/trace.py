# Runtime — New File: runner/trace.py
#
# Lightweight execution trace channel (events, notes, markers)
#

import multiprocessing as mp


class Trace:
    def __init__(self):
        self._events = mp.Manager().list()

    def emit(self, event: str, **data):
        self._events.append({
            "event": event,
            "data": data,
        })

    def dump(self):
        return list(self._events)
