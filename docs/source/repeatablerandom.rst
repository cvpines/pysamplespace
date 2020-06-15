:mod:`samplespace.repeatablerandom` - Repeatable Random Sequences
=================================================================

.. module:: samplespace.repeatablerandom
    :synopsis: Generate repeatable, deterministic random sequences.

----------

:class:`RepeatableRandomSequence` allows for generating repeatable,
deterministic random sequences. It is compatible with the built-in
:mod:`random` module as a drop-in replacement.

A key feature of :class:`RepeatableRandomSequence` is its ability to
get, serialize, and restore internal state. This is especially useful
when generating procedural content from a fixed seed.

A :class:`RepeatableRandomSequence` can also be used for unit testing
by replacing the built-in :mod:`random` module. Because each random
sequence is deterministic and repeatable for a given seed, expected
values can be recorded and compared against within unit tests.

:class:`RepeatableRandomSequence` produces high-quality pseudo-random
values. See :ref:`random-quality-label` for results from randomness tests.

----------

.. autoclass:: RepeatableRandomSequence

.. autoattribute:: RepeatableRandomSequence.BLOCK_SIZE_BITS

.. autoattribute:: RepeatableRandomSequence.BLOCK_MASK

Bookkeeping functions
---------------------

.. automethod:: RepeatableRandomSequence.seed

.. automethod:: RepeatableRandomSequence.getseed

.. automethod:: RepeatableRandomSequence.getstate

.. automethod:: RepeatableRandomSequence.setstate

.. automethod:: RepeatableRandomSequence.reset

.. autoattribute:: RepeatableRandomSequence.index

.. automethod:: RepeatableRandomSequence.getnextblock

.. automethod:: RepeatableRandomSequence.getrandbits

.. automethod:: RepeatableRandomSequence.cascade

.. autoclass:: RepeatableRandomSequenceState
    :members:

Integer distributions
---------------------

.. automethod:: RepeatableRandomSequence.randrange

.. automethod:: RepeatableRandomSequence.randint

.. automethod:: RepeatableRandomSequence.randbytes

.. automethod:: RepeatableRandomSequence.geometric

.. automethod:: RepeatableRandomSequence.finitegeometric

.. automethod:: RepeatableRandomSequence.zipfmandelbrot

Categorical distributions
-------------------------

.. automethod:: RepeatableRandomSequence.choice

.. automethod:: RepeatableRandomSequence.choices

.. automethod:: RepeatableRandomSequence.shuffle

.. automethod:: RepeatableRandomSequence.sample

.. automethod:: RepeatableRandomSequence.chance

Continuous distributions
------------------------

.. automethod:: RepeatableRandomSequence.random

.. automethod:: RepeatableRandomSequence.uniform

.. automethod:: RepeatableRandomSequence.triangular

.. automethod:: RepeatableRandomSequence.gauss

.. automethod:: RepeatableRandomSequence.gausspair

.. automethod:: RepeatableRandomSequence.lognormvariate

.. automethod:: RepeatableRandomSequence.expovariate

.. automethod:: RepeatableRandomSequence.vonmisesvariate

.. automethod:: RepeatableRandomSequence.gammavariate

.. automethod:: RepeatableRandomSequence.betavariate

.. automethod:: RepeatableRandomSequence.paretovariate

.. automethod:: RepeatableRandomSequence.weibullvariate

.. automethod:: RepeatableRandomSequence.normalvariate

Examples
--------

Generating random values::

    import samplespace

    rrs = samplespace.RepeatableRandomSequence(seed=1234)

    samples = [rrs.randrange(30) for _ in range(10)]
    print(samples)
    # Will always print:
    # [21, 13, 28, 19, 16, 29, 28, 24, 29, 25]

Distinct seeds produce unique results::

    import samplespace

    # Each seed will generate a unique sequence of values
    for seed in range(5):
        rrs = samplespace.RepeatableRandomSequence(seed=seed)
        samples = [rrs.random() for _ in range(5)]
        print('Seed: {0}\tResults: {1}'.format(
            seed,
            ' '.join('{:.3f}'.format(x) for x in samples)))

Results depend only on number of previous calls, not their type::

    import samplespace

    rrs = samplespace.RepeatableRandomSequence(seed=1234)

    dummy = rrs.random()
    x1 = rrs.random()

    rrs.reset()
    dummy = rrs.gauss(6.0, 2.0)
    x2 = rrs.random()
    assert x2 == x1

    rrs.reset()
    dummy = rrs.randrange(50)
    x3 = rrs.random()
    assert x3 == x1

    rrs.reset()
    dummy = list('abcdefg')
    rrs.shuffle(dummy)
    x4 = rrs.random()
    assert x4 == x1

    rrs.reset()
    with rrs.cascade():
        dummy = [rrs.random() for _ in range(10)]
    x5 = rrs.random()
    assert x5 == x1

Replay random sequences using :meth:`RepeatableRandomSequence.reset`::

    import samplespace

    rrs = samplespace.RepeatableRandomSequence(seed=1234)

    samples = [rrs.random() for _ in range(10)]
    print(' '.join(samples))

    # Using reset() returns the sequence to its initial state
    rrs.reset()
    samples2 = [rrs.random() for _ in range(10)]
    print(' '.join(samples2))
    assert samples == sample2

Replay random sequences using :meth:`RepeatableRandomSequence.getstate`/
:meth:`RepeatableRandomSequence.setstate`::

    import samplespace

    rrs = samplespace.RepeatableRandomSequence(seed=12345)

    # Generate some random values to advance the state
    [rrs.random() for _ in range(100)]

    # Save the state for later recall
    state = rrs.getstate()
    print(rrs.random())
    # Will print 0.2736967629462168

    # Generate some more values
    [rrs.random() for _ in range(100)]

    # Return the sequence to the saved state. The next value will match
    # the value following when the state was saved.
    rrs.setstate(state)
    print(rrs.random())
    # Will also print 0.2736967629462168

Replay random sequences using :meth:`RepeatableRandomSequence.index`::

    import samplespace

    rrs = samplespace.RepeatableRandomSequence(seed=5)

    # Generate a sequence of values
    samples = [rrs.randrange(10) for _ in range(15)]
    print(samples)
    # Will print
    # [0, 2, 2, 7, 9, 4, 1, 5, 5, 6, 7, 1, 7, 6, 8]

    # Rewind the sequence by 5
    rrs.index -= 5

    # Generate a new sequence, will overlap by 5 elements
    samples = [rrs.randrange(10) for _ in range(15)]
    print(samples)
    # Will print
    # [7, 1, 7, 6, 8, 6, 6, 6, 3, 7, 6, 9, 5, 2, 7]

Serialize sequence state as simple data types::

    import samplespace
    import samplespace.repeatablerandom
    import json

    rrs = samplespace.RepeatableRandomSequence(seed=12345)

    # Generate some random values to advance the state
    [rrs.random() for _ in range(100)]

    # Save the state for later recall
    # State can be serialzied to a dict and serialized as JSON
    state = rrs.getstate()
    state_as_dict = state.as_dict()
    state_as_json = json.dumps(state_as_dict)
    print(state_as_json)
    # Prints {"seed": 12345, "hash_input": "gxzNfDj4Ypc=", "index": 100}

    print(rrs.random())
    # Will print 0.2736967629462168

    # Generate some more values
    [rrs.random() for _ in range(100)]

    # Return the sequence to the saved state. The next value will match
    # the value following when the state was saved.
    new_state_as_dict = json.loads(state_as_json)
    new_state = samplespace.repeatablerandom.RepeatableRandomSequenceState.from_dict(new_state_as_dict)
    rrs.setstate(new_state)
    print(rrs.random())
    # Will also print 0.2736967629462168

