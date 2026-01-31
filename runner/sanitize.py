# Runtime — New File: runner/sanitize.py
#
# Protect runtime-reserved config keys
#

RUNTIME_KEYS = {
    "_steps",
    "_trace",
}


def sanitize_config(config: dict) -> dict:
    """
    Remove or isolate runtime-reserved keys from user input.
    """
    clean = dict(config)
    for key in RUNTIME_KEYS:
        if key in clean:
            del clean[key]
    return clean
