import re

PATTERN = re.compile(r'^([0-9]+)([smhdwy])$')
SUFFIX_MAP = {
    's': 1,
    'm': 60,
    'h': 3600,
    'd': 86400,
    'w': 604800,
    'y': 31536000,
}


def parse_duration(string):
    match = re.match(PATTERN, string)
    if not match:
        raise ValueError('Invalid duration: {}'.format(string))

    suffix = match.group(2)
    if suffix not in SUFFIX_MAP:
        raise ValueError('Invalid duration suffix: {}'.format(string))

    return int(match.group(1)) * SUFFIX_MAP[suffix]
