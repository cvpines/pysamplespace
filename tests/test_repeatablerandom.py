import json

import pytest

import samplespace

DATA_FILE = 'data.json'

with open(DATA_FILE, 'r') as f:
    test_data = json.load(f)


class PatchedRRS(samplespace.RepeatableRandomSequence):
    __slots__ = ('_seed', '_hash_input', '_index', '_cascading', 'index_list')

    def __init__(self, seed):
        super().__init__(seed)
        self.index_list = []

    def getnextblock(self):
        self.index_list.append(self._index)
        return super().getnextblock()


def test_data_version():
    assert test_data['version'] == samplespace.__version__


def test_expected_sequence():
    # Test raw 64 bit chunks for seed 0
    rrs = samplespace.RepeatableRandomSequence(seed=0)
    actual = [rrs.getnextblock() for _ in range(10)]
    expected = test_data['raw-seed0-index0-n10']
    assert actual == expected

    # Test raw 64 bit chunks for a different seed
    rrs = samplespace.RepeatableRandomSequence(seed=123456)
    actual = [rrs.getnextblock() for _ in range(10)]
    expected = test_data['raw-seed123456-index0-n10']
    assert actual == expected

    # Continuing the sequence, test conversion to floats
    actual = [rrs.random() for _ in range(10)]
    expected = test_data['double-seed123456-index10-n10']
    assert actual == expected

    # Continuing the sequence, test byte sequences
    actual = [rrs.randbytes(10) for _ in range(2)]
    expected = [bytes(x) for x in test_data['bytes-len10-seed123456-index20-n2']]
    assert actual == expected

    # Continuing the sequence, test double sequences
    with rrs.cascade():
        seq1 = [rrs.random() for _ in range(5)]
    with rrs.cascade():
        seq2 = [rrs.random() for _ in range(5)]
    actual = [seq1, seq2]
    expected = test_data['doubles-len5-seed123456-index22-n2']
    assert actual == expected

    # Continuing the sequence, test nil-kappa von mises dist
    actual = [rrs.vonmisesvariate(mu=0.0, kappa=0.0) for _ in range(5)]
    expected = test_data['vonmises-kappa0-mu0-seed123456-index24-n5']
    assert actual == expected

    # Continuing the sequence, test wrapped-mu von mises dist
    actual = [rrs.vonmisesvariate(mu=10.0, kappa=2.0) for _ in range(5)]
    expected = test_data['vonmises-kappa2-mu10-seed123456-index29-n5']
    assert actual == expected

    # Continuing the sequence, test large-alpha gamma dist
    actual = [rrs.gammavariate(alpha=2.0, beta=1.0) for _ in range(5)]
    expected = test_data['gamma-alpha2-beta1-seed123456-index34-n5']
    assert actual == expected

    # Continuing the sequence, test unit-alpha gamma dist
    actual = [rrs.gammavariate(alpha=1.0, beta=1.0) for _ in range(5)]
    expected = test_data['gamma-alpha1-beta1-seed123456-index39-n5']
    assert actual == expected

    # Continuing the sequence, test small-alpha gamma dist
    actual = [rrs.gammavariate(alpha=0.5, beta=1.0) for _ in range(5)]
    expected = test_data['gamma-alpha0.5-beta1-seed123456-index44-n5']
    assert actual == expected

    # Continuing the sequence, gaussian distribution
    actual = [rrs.gauss(mu=0, sigma=1) for _ in range(10)]
    expected = test_data['gauss-mu0-sigma1-seed123456-index49-n10']
    assert actual == expected


def test_no_cascading():
    rrs = samplespace.RepeatableRandomSequence(seed=1234)

    # Ensure no-cascade methods are blocked
    with pytest.raises(RuntimeError):
        with rrs.cascade():
            rrs.seed(10)

    with pytest.raises(RuntimeError):
        with rrs.cascade():
            rrs.index = 10

    with pytest.raises(RuntimeError):
        with rrs.cascade():
            _ = rrs.index

    with pytest.raises(RuntimeError):
        with rrs.cascade():
            rrs.reset()

    with pytest.raises(RuntimeError):
        with rrs.cascade():
            rrs.getstate()

    with pytest.raises(RuntimeError):
        with rrs.cascade():
            # noinspection PyTypeChecker
            rrs.setstate(None)


# noinspection PyProtectedMember
def test_cascade_indices():
    rrs = PatchedRRS(seed=1234)

    # Non-cascaded should use subsequent indices
    rrs.index_list.clear()
    start_index = rrs.index
    for _ in range(10):
        rrs.getnextblock()

    assert rrs.index_list == [start_index + i for i in range(10)]

    # Cascades should produce the same number of indices, but
    # indices should not be subsequent
    rrs.index_list.clear()
    start_index = rrs.index
    with rrs.cascade():
        for _ in range(10):
            rrs.getnextblock()

    assert len(rrs.index_list) == 10
    assert rrs.index_list[0] == start_index
    assert rrs.index_list[1:] != [start_index + i for i in range(1, 10)]

    # Indices should resume normal incrementing when a cascade ends
    rrs.index_list.clear()
    rrs.getnextblock()
    assert rrs.index_list == [start_index + 1]


def test_reset():
    rrs = samplespace.RepeatableRandomSequence(seed='abcdef')
    run1 = [rrs.getnextblock() for _ in range(256)]

    rrs.reset()
    run2 = [rrs.getnextblock() for _ in range(256)]

    assert run1 == run2


# noinspection PyProtectedMember
def test_getrandbits():
    rrs = PatchedRRS(seed=1234)

    # Assert values stay in range
    assert all(0 <= rrs.getrandbits(3) < 8 for _ in range(100))
    assert all(0 <= rrs.getrandbits(4) < 16 for _ in range(100))
    assert all(0 <= rrs.getrandbits(5) < 32 for _ in range(100))

    # Negative bits returns zero and advances the index
    start_index = rrs._index
    assert rrs.getrandbits(-1) == 0
    assert rrs._index == start_index + 1

    # Bits <= block size should advance index once
    rrs.index_list.clear()
    start_index = rrs._index
    rrs.getrandbits(5)
    assert rrs.index_list == [start_index]
    assert rrs._index == start_index + 1

    rrs.index_list.clear()
    start_index = rrs._index
    rrs.getrandbits(64)
    assert rrs.index_list == [start_index]
    assert rrs._index == start_index + 1

    # Bits > block size should advance index multiple times
    rrs.index_list.clear()
    start_index = rrs._index
    rrs.getrandbits(65)
    assert len(rrs.index_list) == 2
    assert rrs.index_list[0] == start_index
    assert rrs.index_list[1] != start_index + 1
    assert rrs._index == start_index + 1


def test_distinct_seeds():
    rrs = samplespace.RepeatableRandomSequence(seed='abcdef')
    run1 = [rrs.getnextblock() for _ in range(256)]

    rrs = samplespace.RepeatableRandomSequence(seed=98471)
    run2 = [rrs.getnextblock() for _ in range(256)]

    assert run1 != run2


def test_state():
    # Restoring state
    rrs = samplespace.RepeatableRandomSequence(seed=12345)
    for _ in range(100):
        rrs.getnextblock()

    state = rrs.getstate()
    expected = rrs.getnextblock()

    for _ in range(100):
        rrs.getnextblock()

    rrs.setstate(state)
    actual = rrs.getnextblock()
    assert actual == expected

    # Restoring state using indices
    start_index = rrs.index
    expected = rrs.getnextblock()

    for _ in range(100):
        rrs.getnextblock()

    rrs.index = start_index
    actual = rrs.getnextblock()
    assert actual == expected

    # Rewinding indices
    expected = [rrs.random() for _ in range(10)]

    for _ in range(50):
        rrs.getnextblock()

    rrs.index -= 60
    actual = [rrs.random() for _ in range(10)]
    assert actual == expected

    # Copying state
    state = rrs.getstate()
    expected = rrs.getnextblock()

    rrs2 = samplespace.RepeatableRandomSequence(seed='hello')
    rrs2.setstate(state)
    actual = rrs2.getnextblock()
    assert actual == expected


def test_serialize_rrs_state():
    """Verifies that RRS states serialize to YAML correctly."""
    rrs = samplespace.RepeatableRandomSequence(seed=12345)
    [rrs.getnextblock() for _ in range(100)]

    state = rrs.getstate()
    expected = rrs.getnextblock()

    state_as_dict = state.as_dict()
    [rrs.getnextblock() for _ in range(100)]

    new_state = samplespace.repeatablerandom.RepeatableRandomSequenceState.from_dict(state_as_dict)
    assert new_state == state

    rrs.setstate(new_state)
    actual = rrs.getnextblock()
    assert actual == expected


# noinspection PyProtectedMember
def test_shuffle():
    rrs = samplespace.RepeatableRandomSequence(seed='hello')

    initial = list(range(100))

    start_index = rrs.index

    shuffled = list(initial)
    rrs.shuffle(shuffled)

    assert set(initial) == set(shuffled)
    assert initial != shuffled
    assert rrs.index == start_index + 1


def test_randint():
    rrs = samplespace.RepeatableRandomSequence(seed='hello')

    expected = [rrs.randrange(2, 14) for _ in range(10)]

    rrs.reset()
    actual = [rrs.randint(2, 13) for _ in range(10)]
    assert actual == expected


# noinspection PyTypeChecker
def test_randrange_args():
    rrs = samplespace.RepeatableRandomSequence()

    with pytest.raises(TypeError):
        rrs.randrange(2.1)

    with pytest.raises(TypeError):
        rrs.randrange(1, 2.1)

    with pytest.raises(TypeError):
        rrs.randrange(1, 2, 0.5)

    with pytest.raises(ValueError):
        rrs.randrange(1, 2, 0)


def test_triangular_args():
    rrs = samplespace.RepeatableRandomSequence()

    with pytest.raises(ValueError):
        rrs.triangular(2.0, 1.0)

    with pytest.raises(ValueError):
        rrs.triangular(1.0, 2.0, 3.0)

    assert rrs.triangular(2.0, 2.0, 2.0) == 2.0


def test_geometric_args():
    rrs = samplespace.RepeatableRandomSequence()

    with pytest.raises(ValueError):
        rrs.geometric(0.5, False)

    with pytest.raises(ValueError):
        rrs.geometric(-0.5, True)


def test_finitegeometric_args():
    rrs = samplespace.RepeatableRandomSequence()

    with pytest.raises(ValueError):
        rrs.finitegeometric(0.5, 0)


def test_zipf_args():
    rrs = samplespace.RepeatableRandomSequence()

    with pytest.raises(ValueError):
        rrs.zipfmandelbrot(1.5, 1.0, 0)


def test_choice_args():
    rrs = samplespace.RepeatableRandomSequence()

    with pytest.raises(IndexError):
        rrs.choice([])


def test_sample_args():
    rrs = samplespace.RepeatableRandomSequence()

    assert rrs.sample([1], 0) == []

    with pytest.raises(IndexError):
        rrs.sample([], 1)

    with pytest.raises(ValueError):
        rrs.sample([1, 2, 3], 5)


def test_choices_args():
    rrs = samplespace.RepeatableRandomSequence()

    assert rrs.choices([1, 2], k=0) == []

    with pytest.raises(IndexError):
        rrs.choices([], k=1)

    with pytest.raises(TypeError):
        rrs.choices([1], weights=[1.0], cum_weights=[1.0])

    with pytest.raises(ValueError):
        rrs.choices([1], weights=[1.0, 2.0])


def test_gamma_args():
    rrs = samplespace.RepeatableRandomSequence()

    with pytest.raises(ValueError):
        rrs.gammavariate(-1.0, -1.0)


def test_pareto_args():
    rrs = samplespace.RepeatableRandomSequence()

    with pytest.raises(ValueError):
        rrs.paretovariate(0.0)


def test_weibull_args():
    rrs = samplespace.RepeatableRandomSequence()

    with pytest.raises(ValueError):
        rrs.weibullvariate(1.0, 0.0)


# noinspection PyProtectedMember,PyTypeChecker
def test_randbelow_args():
    rrs = samplespace.RepeatableRandomSequence()

    with pytest.raises(TypeError):
        rrs._randbelow(2.1)

    with pytest.raises(ValueError):
        rrs._randbelow(0)
