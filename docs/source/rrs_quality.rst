.. _random-quality-label:

Random Generator Quality
========================

:class:`RepeatableRandomSequence` produces high-quality psuedo-random data
regardless of seed or cascade size.

The script ``tests/generate_random_bytes.py`` can be used to generate
files filled with random bytes for testing with external testing programs,
or ``tests/stream_random_bytes.py [seed]`` can be used to stream an
unlimited number of random bytes to stdout.

Randomness Test Results
-----------------------

Results from  `ENT <http://fourmilab.ch/random/>`_::

    $ python stream_random_bytes.py | head -c 8388608 | ent
    Entropy = 7.999979 bits per byte.

    Optimum compression would reduce the size
    of this 8388608 byte file by 0 percent.

    Chi square distribution for 8388608 samples is 244.76, and randomly
    would exceed this value 66.64 percent of the times.

    Arithmetic mean value of data bytes is 127.4945 (127.5 = random).
    Monte Carlo value for Pi is 3.141415391 (error 0.01 percent).
    Serial correlation coefficient is 0.000034 (totally uncorrelated = 0.0).

Results from `Dieharder <https://webhome.phy.duke.edu/~rgb/General/dieharder.php>`_::

    #=============================================================================#
    #            dieharder version 3.31.1 Copyright 2003 Robert G. Brown          #
    #=============================================================================#
            test_name   |ntup| tsamples |psamples|  p-value |Assessment
    #=============================================================================#
       diehard_birthdays|   0|       100|     100|0.46260921|  PASSED
          diehard_operm5|   0|   1000000|     100|0.30499458|  PASSED
      diehard_rank_32x32|   0|     40000|     100|0.84557704|  PASSED
        diehard_rank_6x8|   0|    100000|     100|0.75986634|  PASSED
       diehard_bitstream|   0|   2097152|     100|0.26336497|  PASSED
            diehard_opso|   0|   2097152|     100|0.09991336|  PASSED
            diehard_oqso|   0|   2097152|     100|0.47106073|  PASSED
             diehard_dna|   0|   2097152|     100|0.09032458|  PASSED
    diehard_count_1s_str|   0|    256000|     100|0.93473326|  PASSED
    diehard_count_1s_byt|   0|    256000|     100|0.84493493|  PASSED
     diehard_parking_lot|   0|     12000|     100|0.33164281|  PASSED
        diehard_2dsphere|   2|      8000|     100|0.90268828|  PASSED
        diehard_3dsphere|   3|      4000|     100|0.87557333|  PASSED
         diehard_squeeze|   0|    100000|     100|0.75415145|  PASSED
            diehard_sums|   0|       100|     100|0.15694874|  PASSED
            diehard_runs|   0|    100000|     100|0.19158234|  PASSED
            diehard_runs|   0|    100000|     100|0.27969502|  PASSED
           diehard_craps|   0|    200000|     100|0.99326664|  PASSED
           diehard_craps|   0|    200000|     100|0.37802538|  PASSED
     marsaglia_tsang_gcd|   0|     40000|     100|0.44158442|  PASSED
     marsaglia_tsang_gcd|   0|     40000|     100|0.38455344|  PASSED
             sts_monobit|   1|    100000|     100|0.90249899|  PASSED
                sts_runs|   2|    100000|     100|0.77696296|  PASSED
              sts_serial|   1|    100000|     100|0.90249899|  PASSED
              sts_serial|   2|    100000|     100|0.59050254|  PASSED
              sts_serial|   3|    100000|     100|0.90871975|  PASSED
              sts_serial|   3|    100000|     100|0.99336098|  PASSED
              sts_serial|   4|    100000|     100|0.34637953|  PASSED
              sts_serial|   4|    100000|     100|0.23240191|  PASSED
              sts_serial|   5|    100000|     100|0.65698384|  PASSED
              sts_serial|   5|    100000|     100|0.20441284|  PASSED
              sts_serial|   6|    100000|     100|0.11455355|  PASSED
              sts_serial|   6|    100000|     100|0.10947486|  PASSED
              sts_serial|   7|    100000|     100|0.33236940|  PASSED
              sts_serial|   7|    100000|     100|0.90065107|  PASSED
              sts_serial|   8|    100000|     100|0.71691528|  PASSED
              sts_serial|   8|    100000|     100|0.72658614|  PASSED
              sts_serial|   9|    100000|     100|0.05947803|  PASSED
              sts_serial|   9|    100000|     100|0.35266839|  PASSED
              sts_serial|  10|    100000|     100|0.25645609|  PASSED
              sts_serial|  10|    100000|     100|0.96328452|  PASSED
              sts_serial|  11|    100000|     100|0.26614777|  PASSED
              sts_serial|  11|    100000|     100|0.75690153|  PASSED
              sts_serial|  12|    100000|     100|0.72460595|  PASSED
              sts_serial|  12|    100000|     100|0.59228401|  PASSED
              sts_serial|  13|    100000|     100|0.43108810|  PASSED
              sts_serial|  13|    100000|     100|0.39814551|  PASSED
              sts_serial|  14|    100000|     100|0.93222323|  PASSED
              sts_serial|  14|    100000|     100|0.10847133|  PASSED
              sts_serial|  15|    100000|     100|0.97030212|  PASSED
              sts_serial|  15|    100000|     100|0.74232610|  PASSED
              sts_serial|  16|    100000|     100|0.30293298|  PASSED
              sts_serial|  16|    100000|     100|0.74289769|  PASSED
             rgb_bitdist|   1|    100000|     100|0.52609114|  PASSED
             rgb_bitdist|   2|    100000|     100|0.35992730|  PASSED
             rgb_bitdist|   3|    100000|     100|0.80654719|  PASSED
             rgb_bitdist|   4|    100000|     100|0.84084274|  PASSED
             rgb_bitdist|   5|    100000|     100|0.54266728|  PASSED
             rgb_bitdist|   6|    100000|     100|0.04443687|  PASSED
             rgb_bitdist|   7|    100000|     100|0.22723549|  PASSED
    rgb_minimum_distance|   4|     10000|    1000|0.23472614|  PASSED
        rgb_permutations|   5|    100000|     100|0.68681017|  PASSED
          rgb_lagged_sum|   0|   1000000|     100|0.57837513|  PASSED
         rgb_kstest_test|   0|     10000|    1000|0.52944830|  PASSED


Distribution Validity Tests
---------------------------

The scripts ``tests/scripts/calculate_*_metrics.py`` can be used to
check that Repeatable Random Sequences produce values with the correct
probability distributions.

Bear in mind that as limited samples are taken from each distribution,
some false negatives may occur. If anomalous results are present, try
re-running the scripts.
