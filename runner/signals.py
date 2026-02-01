# Runtime — New File: runner/signals.py
#
# Graceful interrupt + hard kill handling
#

import signal
from runner.errors import LimitExceeded


def install_signal_handlers():
    def _handle_timeout(signum, frame):
        raise LimitExceeded("Execution interrupted by signal")

    signal.signal(signal.SIGALRM, _handle_timeout)
    signal.signal(signal.SIGINT, _handle_timeout)
    signal.signal(signal.SIGTERM, _handle_timeout)
