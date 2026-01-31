# Runtime — New File: runner/memory.py
#
# Best-effort memory limiter (Unix only; advisory elsewhere)
#

import os
import sys

try:
    import resource
    HAS_RESOURCE = True
except ImportError:
    HAS_RESOURCE = False


def set_memory_limit_mb(max_mb: int):
    if not HAS_RESOURCE:
        return

    if sys.platform == "darwin":
        # macOS uses bytes
        limit = max_mb * 1024 * 1024
    else:
        # Linux: RLIMIT_AS in bytes
        limit = max_mb * 1024 * 1024

    resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
