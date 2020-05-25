# Generates an endless stream of random bytes using 1024 byte long cascades

import sys
import os

from samplespace import RepeatableRandomSequence


if __name__ == '__main__':
    f = os.fdopen(os.sys.stdout.fileno(), 'wb')
    seed = sys.argv[1] if len(sys.argv) >= 2 else 0
    rrs = RepeatableRandomSequence(seed=seed)
    while True:
        try:
            f.write(rrs.randbytes(1048576))
            f.flush()
        except (BrokenPipeError, KeyboardInterrupt):
            break

    try:
        f.close()
    except BrokenPipeError:
        pass
