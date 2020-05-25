:mod:`samplespace.distributions` - Serializable Probability Distributions
=========================================================================

.. module:: samplespace.distributions
    :synopsis: Represent and sample from various probability distributions.

----------

This module implements a number of useful probability distributions.

Each distribution can be sampled using any random number generator
providing at least the same functionality as the :mod:`random` module;
this includes :class:`samplespace.repeatablerandom.RepeatableRandomSequence`.

The classes in this module are primarily intended for storing information
on random distributions in configuration files using
``Distribution.as_dict()``/:func:`distribution_from_dict` or
``Distribution.as_list()``/:func:`distribution_from_list`.
See the :ref:`examples-label` section for examples on how to do this.



Integer distributions
----------------------

.. autoclass:: DiscreteUniform
    :members:
    :inherited-members:

.. autoclass:: Geometric
    :members:
    :inherited-members:

.. autoclass:: FiniteGeometric
    :members:
    :inherited-members:

.. autoclass:: ZipfMandelbrot
    :members:
    :inherited-members:

.. autoclass:: Bernoulli
    :members:
    :inherited-members:

Categorical distributions
-------------------------

.. autoclass:: WeightedCategorical
    :members:
    :inherited-members:

.. autoclass:: UniformCategorical
    :members:
    :inherited-members:

.. autoclass:: FiniteGeometricCategorical
    :members:
    :inherited-members:

.. autoclass:: ZipfMandelbrotCategorical
    :members:
    :inherited-members:

Continuous distributions
------------------------

.. autoclass:: Constant
    :members:
    :inherited-members:

.. autoclass:: Uniform
    :members:
    :inherited-members:

.. autoclass:: Gamma
    :members:
    :inherited-members:

.. autoclass:: Triangular
    :members:
    :inherited-members:

.. autoclass:: LogNormal
    :members:
    :inherited-members:

.. autoclass:: Exponential
    :members:
    :inherited-members:

.. autoclass:: VonMises
    :members:
    :inherited-members:

.. autoclass:: Beta
    :members:
    :inherited-members:

.. autoclass:: Pareto
    :members:
    :inherited-members:

.. autoclass:: Weibull
    :members:
    :inherited-members:

.. autoclass:: Gaussian
    :members:
    :inherited-members:

Serialization functions
-----------------------

.. autofunction:: distribution_from_list

.. autofunction:: distribution_from_dict

.. classmethod:: samplespace.distribution.Distribution.from_list

    An alias for :func:`distribution_from_list`.

.. classmethod:: samplespace.distribution.Distribution.from_dict

    An alias for :func:`distribution_from_dict`.

.. _examples-label:

Examples
--------

Sampling from a distribution::

    import random
    import statistics

    from samplespace.distributions import Gaussian, FiniteGeometric

    gauss = Gaussian(15.0, 2.0)
    samples = [gauss.sample(random) for _ in range(100)]
    print('Mean:', statistics.mean(samples))
    print('Standard deviation:', statistics.stdev(samples))

    geo = FiniteGeometric(['one', 'two', 'three', 'four', 'five'], 0.7)
    samples = [geo.sample(random) for _ in range(10)]
    print(' '.join(samples))

Using other random generators::

    from samplespace import distributions, RepeatableRandomSequence

    exponential = distributions.Exponential(0.8)

    rrs = RepeatableRandomSequence(seed=12345)
    print([exponential.sample(rrs) for _ in range(5)])
    # Will always print:
    # [1.1959827296976795, 0.6056492468915003, 0.9155454941988664, 0.5653478889068511, 0.6500080335986231]

Representations of distributions::

    from samplespace.distributions import Pareto, DiscreteUniform, UniformCategorical

    pareto = Pareto(2.5)
    print('Pareto as dict:', pareto.as_dict())  # {'distribution': 'pareto', 'alpha': 2.5}
    print('Pareto as list:', pareto.as_list())  # ['pareto', 2.5]

    discrete = DiscreteUniform(3, 8)
    print('Discrete uniform as dict:', discrete.as_dict())  # {'distribution': 'discreteuniform', 'min_val': 3, 'max_val': 8}
    print('Discrete uniform as list:', discrete.as_list())  # ['discreteuniform', 3, 8]

    cat = UniformCategorical(['string', 4, {'a':'dict'}])
    print('Uniform categorical as dict:', cat.as_dict())  # {'distribution': 'uniformcategorical', 'population': ['string', 4, {'a': 'dict'}]}
    print('Uniform categorical as list:', cat.as_list())  # ['uniformcategorical', ['string', 4, {'a': 'dict'}]]

Storing distributions as in config files as lists::

    import random
    from samplespace import distributions

    ...

    skeleton_config = {
        'name': 'Skeleton',
        'starting_hp': ['gaussian', 50.0, 5.0],
        'coins_dropped': ['geometric', 0.8, True],
    }

    ...

    class Skeleton(object):
        def __init__(self, name, starting_hp, coins_dropped_dist):
            self.name = name
            self.starting_hp = starting_hp
            self.coins_dropped_dist = coins_dropped_dist

        def drop_coins(self):
            return self.coins_dropped_dist.sample(random)

    ...

    class SkeletonFactory(object):

        def __init__(self, config):
            self.name = config['name']
            self.starting_hp_dist = distributions.distribution_from_list(config['starting_hp'])
            self.coins_dropped_dist = distributions.distribution_from_list(config['coins_dropped'])

        def make_skeleton(self):
            return Skeleton(
                self.name,
                int(self.starting_hp_dist.sample(random)),
                self.coins_dropped_dist)

Storing distributions in config files as dictionaries::

    from samplespace import distributions, RepeatableRandomSequence

    city_config = {
        "building_distribution": {
            "distribution": "weightedcategorical",
            "items": [
                ["house", 0.2],
                ["store", 0.4],
                ["tree", 0.8],
                ["ground", 5.0]
            ]
        }
    }

    rrs = RepeatableRandomSequence()
    building_dist = distributions.distribution_from_dict(city_config['building_distribution'])

    buildings = [[building_dist.sample(rrs) for col in range(20)] for row in range(5)]

    for row in buildings:
        for building_type in row:
            if building_type == 'house':
                print('H', end='')
            elif building_type == 'store':
                print('S', end='')
            elif building_type == 'tree':
                print('T', end='')
            else:
                print('.', end='')
        print()

