import re
import datetime

PATTERN = re.compile(r'^([0-9]+)([smhdwy])$')
SUFFIX_MAP = {
    's': 1,
    'm': 60,
    'h': 3600,
    'd': 86400,
    'w': 604800,
    'y': 31536000,
}


def duration(value) -> datetime.timedelta:
    """Convert duration to `timedelta`."""
    if isinstance(value, datetime.timedelta):
        return value

    if isinstance(value, str):
        match = re.match(PATTERN, value)
        if not match:
            raise ValueError('Invalid duration: {}'.format(value))

        suffix = match.group(2)
        if suffix not in SUFFIX_MAP:
            raise ValueError('Invalid duration suffix: {}'.format(value))

        value = int(match.group(1)) * SUFFIX_MAP[suffix]

    return datetime.timedelta(seconds=value)
