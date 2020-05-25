:mod:`samplespace.algorithms` - General Sampling Algorithms
===========================================================

.. module:: samplespace.algorithms
    :synopsis: Provides general-purpose sampling algorithms.

--------

This module implements several general-purpose sampling algorithms.

--------

.. autofunction:: sample_discrete_roulette

.. autoclass:: AliasTable
    :members:


Examples
--------

Sampling from a discrete categorical distribution using the
Roulette Wheel Selection algorithm::

    import random
    import itertools
    from samplespace import algorithms


    population = 'abcde'
    weights = [0.1, 0.4, 0.2, 0.3, 0.5]

    cum_weights = list(itertools.accumulate(weights))
    indices = [algorithms.sample_discrete_roulette(random.random, cum_weights)
               for _ in range(25)]  # [0, 4, 4, ...]
    samples = [population[index] for index in indices]  # ['a', 'e', 'e', ...]


Sampling from a discrete categorical distribution using the Alias Table
algorithm and a repeatable sequence::

    from samplespace import algorithms, RepeatableRandomSequence

    population = 'abcde'
    weights = [0.1, 0.4, 0.2, 0.3, 0.5]

    rrs = RepeatableRandomSequence(seed=12345)
    at = algorithms.AliasTable.from_weights(weights)
    indices = [at.sample(rrs.randrange, rrs.chance) for _ in range(25)]
    samples = [population[index] for index in indices]  # ['e', 'e', 'c', ...]

    # Note that rrs.index == 50 at this point, since two random values
    # were required for each sample.

    # It is also possible to use AliasTable within a cascade:
    rrs.reset()
    indices = [0] * 25
    for i in range(len(indices)):
        with rrs.cascade():
            indices[i] = at.sample(rrs.randrange, rrs.chance)
    samples = [population[index] for index in indices]  # ['e', 'd', 'b', ...]

    # Because cascades were used, rrs.index == 25.
    # Note that the values produced are different than the previous
    # attempt, because a different number of logical samples were made.

