# Generates files filled with random bytes for use with randomness
# testing programs.

import os
import time

from samplespace import RepeatableRandomSequence

OUTPUT_DIRECTORY = '../random_output'
FILENAME_FORMAT = 'random-s{seed}-n{length}-c{chunk}.bytes'

PARAMS = [
    {'seed': 0, 'length': 1048576, 'chunk': 1},
    {'seed': 0, 'length': 1048576, 'chunk': 8},
    {'seed': 0, 'length': 1048576, 'chunk': 1048576},
    {'seed': 1, 'length': 1048576, 'chunk': 1},
    {'seed': 1, 'length': 1048576, 'chunk': 8},
    {'seed': 1, 'length': 1048576, 'chunk': 1048576},
    {'seed': 1234, 'length': 1048576, 'chunk': 1},
    {'seed': 1234, 'length': 1048576, 'chunk': 8},
    {'seed': 1234, 'length': 1048576, 'chunk': 1048576},
    {'seed': 0, 'length': 256*1024*1024, 'chunk': 1048576},
]

if __name__ == '__main__':
    for test_config in PARAMS:
        seed = test_config['seed']
        length = test_config['length']
        chunk_size = test_config['chunk']

        filename = os.path.join(
            os.path.abspath(OUTPUT_DIRECTORY),
            FILENAME_FORMAT.format(
                seed=seed,
                length=length,
                chunk=chunk_size))
        print('Generating random data into file \"{}\"...'.format(filename), end='')

        rrs = RepeatableRandomSequence(seed=seed)

        with open(filename, 'wb') as f:
            remaining_bytes = length
            start_time = time.time()
            while remaining_bytes:
                f.write(bytearray(rrs.randbytes(min(chunk_size, remaining_bytes))))
                remaining_bytes -= chunk_size
            f.flush()
            end_time = time.time()
            print('DONE ({:.3f} seconds)'.format(end_time-start_time))
