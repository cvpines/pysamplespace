import random

import pytest

from samplespace import distributions, RepeatableRandomSequence

# noinspection PyProtectedMember
dist_lookup = distributions._distribution_lookup

dist_args = [
    ('constant', {'value': 2.3}),
    ('uniform', {'min_val': 4.5, 'max_val': 6.7}),
    ('discreteuniform', {'min_val': 2, 'max_val': 8}),
    ('geometric', {'mean': 1.6, 'include_zero': True}),
    ('geometric', {'mean': 1.6, 'include_zero': False}),
    ('finitegeometric', {'s': 0.7, 'n': 10}),
    ('zipfmandelbrot', {'s': 1.5, 'q': 0.5, 'n': 10}),
    ('gamma', {'alpha': 3.4, 'beta': 4.5}),
    ('triangular', {'low': 2.4, 'high': 4.6, 'mode': 3.5}),
    ('triangular', {'low': 2.4, 'high': 4.6}),
    ('uniformproduct', {'n': 4}),
    ('lognormal', {'mu': -1.3, 'sigma': 3.1}),
    ('exponential', {'lambd': 2.3}),
    ('vonmises', {'mu': 3.4, 'kappa': 23.1}),
    ('beta', {'alpha': 1.2, 'beta': 3.4}),
    ('pareto', {'alpha': 5.6}),
    ('weibull', {'alpha': 7.8, 'beta': 9.1}),
    ('gaussian', {'mu': 2.3, 'sigma': 4.5}),
    ('bernoulli', {'p': 0.47}),
    ('weightedcategorical', {'population': ['hello', 'world', '!']}),
    ('weightedcategorical', {
        'population': 'abcd',
        'weights': [1.0, 2.0, 3.0, 1.0]}),
    ('weightedcategorical', {
        'population': ['abc', 1, 2.1, 3, {'a': 'dict'}, None],
        'cum_weights': [1.2, 3.3, 5.7, 7.8, 9.1, 10.3]}),
    ('uniformcategorical', {'population': [2, 6.4, 'hi', None, {'b': 'dict'}]}),
    ('finitegeometriccategorical', {'population': ['one', 'two', 'three'], 's': 0.7}),
    ('zipfmandelbrotcategorical', {'population': ['one', 'two', 'three'], 's': 1.5, 'q': 0.5})
]
assert sorted(list(set(name for name, args in dist_args))) == sorted(list(dist_lookup.keys())), \
    'Inadequate coverage over distribution types!'


def test_to_from_list():
    """Verifies that ``as_list``/``from_list`` serialize
    distributions correctly.

    Checks that ``from_list(as_list(y)) == y``."""
    for name, args in dist_args:
        cls = dist_lookup[name]
        dist: distributions.Distribution = cls(**args)
        assert distributions.Distribution.from_list(dist.as_list()) == dist


def test_to_from_dict():
    """Verifies that ``as_dict``/``from_dict`` serialize
    distributions correctly.

    Checks that ``from_dict(as_dict(y)) == y``."""

    for name, args in dist_args:
        cls = dist_lookup[name]
        dist: distributions.Distribution = cls(**args)
        assert distributions.Distribution.from_dict(dist.as_dict()) == dist


def test_properties():
    """Verifies that properties are exposed correctly."""

    for name, args in dist_args:
        cls = dist_lookup[name]
        dist: distributions.Distribution = cls(**args)
        as_dict = dist.as_dict()
        del as_dict['distribution']
        for key, val in as_dict.items():
            # Special case for item-list serialization
            if key == 'items':
                val = [tuple(x) for x in val]
            assert getattr(dist, key) == val


def test_sample_no_throw():
    """Verify that samples can be taken from each distribution type
    without exceptions being thrown. Uses both the random module and a
    RepeatableRandomSequence."""
    rrs = RepeatableRandomSequence(seed=1234)
    for name, args in dist_args:
        cls = dist_lookup[name]
        dist: distributions.Distribution = cls(**args)
        dist.sample(random)
        dist.sample(rrs)
        if hasattr(dist, 'samples'):
            dist.samples(random, 10)
            dist.samples(rrs, 10)
        if hasattr(dist, 'samples_unique'):
            dist.samples_unique(random, 3)
            dist.samples_unique(rrs, 3)


def test_geometric_dynamic_impl():
    # noinspection PyUnusedLocal
    def override_impl(*args):
        return 'CALLED_IMPL'

    dist = distributions.Geometric(1.0)
    dist._impl = override_impl

    # random module doesn't supply geometric(), so the replaced
    # impl method should be called.
    assert dist.sample(random) == 'CALLED_IMPL'

    # RRS does supply geometric(), so the replaced impl method
    # should not be called.
    rrs = RepeatableRandomSequence(seed=2)
    assert dist.sample(rrs) != 'CALLED_IMPL'


# noinspection PyProtectedMember
def test_geometric_impl():
    with pytest.raises(ValueError):
        distributions.Geometric(-1.0, False).sample(random)

    with pytest.raises(ValueError):
        distributions.Geometric(-1.0, True).sample(random)

    rrs = RepeatableRandomSequence(seed=1234)
    for mean in (1.0, 2.5, 100.0):
        dist = distributions.Geometric(mean)
        for _ in range(10):
            state = rrs.getstate()
            expected = rrs.geometric(mean)
            rrs.setstate(state)
            actual = dist._impl(rrs, mean, False)
            assert actual == expected


def test_uniformproduct_dynamic_impl():
    # noinspection PyUnusedLocal
    def override_impl(*args):
        return 'CALLED_IMPL'

    dist = distributions.UniformProduct(5)
    dist._impl = override_impl

    # random module doesn't supply uniformproduct(), so the replaced
    # impl method should be called.
    assert dist.sample(random) == 'CALLED_IMPL'

    # RRS does supply uniformproduct(), so the replaced impl method
    # should not be called.
    rrs = RepeatableRandomSequence(seed=2)
    assert dist.sample(rrs) != 'CALLED_IMPL'


# noinspection PyProtectedMember
def test_uniformproduct_impl():
    with pytest.raises(ValueError):
        distributions.UniformProduct(-1).sample(random)

    rrs = RepeatableRandomSequence(seed=1234)
    for n in (1, 2, 5, 10):
        dist = distributions.UniformProduct(n)
        for _ in range(10):
            state = rrs.getstate()
            expected = rrs.uniformproduct(n)
            rrs.setstate(state)
            with rrs.cascade():
                actual = dist._impl(rrs, n)
            assert actual == expected


def test_base_is_virtual():
    with pytest.raises(NotImplementedError):
        distributions.Distribution().sample(None)

    with pytest.raises(NotImplementedError):
        distributions.Distribution().as_list()

    with pytest.raises(NotImplementedError):
        distributions.Distribution().as_dict()


def test_repr():
    for name, args in dist_args:
        cls = dist_lookup[name]
        dist: distributions.Distribution = cls(**args)
        assert eval('distributions.' + repr(dist)) == dist


def test_equality():
    for name, args in dist_args:
        cls = dist_lookup[name]
        dist1 = cls(**args)
        dist2 = cls(**args)
        assert dist1 == dist2
        assert str(dist1) == str(dist2)
        assert repr(dist1) == repr(dist2)
        assert dist1 != distributions.Distribution()
