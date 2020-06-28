from itertools import accumulate

from samplespace import algorithms


def test_roulette():
    """Test the roulette wheel algorithm by sweeping over "random" values."""
    steps = 100

    # Make sure each normalized weight cleanly divides steps
    weights = [1, 2, 3, 4]
    cum_weights = list(accumulate(weights))
    total = cum_weights[-1]

    expected = []
    for i, weight in enumerate(weights):
        expected.extend([i] * int(weight * steps / total))

    # Ramp up result from 0 to 1 in order, which should produce the above
    actual = []
    for ramp in range(steps):
        actual.append(algorithms.sample_discrete_roulette(
            lambda: ramp / steps,
            cum_weights
        ))

    assert actual == expected


def test_alias_table_equality():
    prob = [1.0, 2.0, 3.0, 4.0]
    alias = [0, 1, 2, 3]

    at1 = algorithms.AliasTable(probability=prob, alias=alias)
    at2 = algorithms.AliasTable(probability=prob, alias=alias)

    assert at1 == at2
    assert at1 != algorithms.AliasTable([], [])
    assert at1 != object()
