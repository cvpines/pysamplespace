![SampleSpace banner](docs/source/img/header.png "SampleSpace")

# SampleSpace: Cross-Platform Tools for Generating Random Numbers

[![pipeline status](https://gitlab.com/cvpines/pysamplespace/badges/master/pipeline.svg)](https://gitlab.com/cvpines/pysamplespace/-/commits/master)
[![coverage report](https://gitlab.com/cvpines/pysamplespace/badges/master/coverage.svg)](https://gitlab.com/cvpines/pysamplespace/-/commits/master)
[![PyPI](https://img.shields.io/pypi/v/pysamplespace)](https://pypi.org/project/pysamplespace/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysamplespace)]((https://pypi.org/project/pysamplespace/))
[![PyPI - License](https://img.shields.io/pypi/l/pysamplespace)](https://gitlab.com/cvpines/pysamplespace/-/blob/master/LICENSE)

SampleSpace is a cross-platform library for describing and sampling from
random distributions.

While SampleSpace is primarily intended for creating
procedurally-generated content, it is also useful for Monte-Carlo
simulations, unit testing, and anywhere that flexible, repeatable random
numbers are required.

## Platforms

SampleSpace supports the following platforms:

* Python &mdash; [pysamplespace](https://pypi.org/project/pysamplespace/)
* C++ &mdash; In development
* C# &mdash; In development

SampleSpace guarantees that the value of random sequences is consistent
and serialized states are compatible across each platform implementation.

## Installation

Installation is simple using `pip`:

> `$ pip install pysamplespace`

SampleSpace's only dependency is
[xxHash](https://pypi.org/project/xxhash/), though it optionally
offers additional functionality if
[PyYAML](https://pypi.org/project/PyYAML/) is installed.

## [Usage](https://pysamplespace.readthedocs.io/en/latest/)

All documentation is available at on [Read the Docs](https://pysamplespace.readthedocs.io/en/latest/). 

SampleSpace provides the following submodules:

* [samplespace.repeatablerandom](https://pysamplespace.readthedocs.io/en/latest/repeatablerandom.html) &mdash;  Repeatable Random Sequences
* [samplespace.distributions](https://pysamplespace.readthedocs.io/en/latest/distributions.html) &mdash;  Serializable Probability Distributions
* [samplespace.algorithms](https://pysamplespace.readthedocs.io/en/latest/algorithms.html) &mdash;  General Sampling Algorithms
* [samplespace.pyyaml_support](https://pysamplespace.readthedocs.io/en/latest/pyyaml_support.html) &mdash;  YAML serialization support
 
### Repeatable Random Sequences

`samplespace.repeatablerandom` allows for generating repeatable, 
deterministic random sequences. It is compatible with the built-in
[random](https://docs.python.org/3/library/random.html) module as a
drop-in replacement.

A key feature of `RepeatableRandomSequence` is its ability to get, serialize, and restore internal
state. This is especially useful when generating procedural content from a fixed seed.

A `RepeatableRandomSequence` can also be used for unit testing by replacing the built-in random module.
Because each random sequence is deterministic and repeatable for a given seed, expected values can be 
recorded and compared against within unit tests.

`RepeatableRandomSequence` produces high-quality pseudo-random values. See 
[Randomness Test Results](https://pysamplespace.readthedocs.io/en/latest/rrs_quality.html) for 
results from randomness tests.

```python
import samplespace

rrs = samplespace.RepeatableRandomSequence(seed=1234)

samples = [rrs.randrange(30) for _ in range(10)]
print(samples)
# Will always print:
# [21, 13, 28, 19, 16, 29, 28, 24, 29, 25]

# Generate some random values to advance the state
[rrs.random() for _ in range(90)]

# Save the state for later recall
# State can be serialzied to a dict and serialized as JSON
state = rrs.getstate()
state_as_dict = state.as_dict()
state_as_json = json.dumps(state_as_dict)
print(state_as_json)
# Prints {"seed": 12345, "hash_input": "gxzNfDj4Ypc=", "index": 100}

print(rrs.random())
# Will print 0.5940559149714152

# Generate some more values
[rrs.random() for _ in range(100)]

# Return the sequence to the saved state. The next value will match
# the value following when the state was saved.
new_state_as_dict = json.loads(state_as_json)
new_state = samplespace.repeatablerandom.RepeatableRandomSequenceState.from_dict(new_state_as_dict)
rrs.setstate(new_state)
print(rrs.random())
# Will also print 0.5940559149714152
```

### Distributions

`samplespace.distributions` implements a number of useful probability distributions.

Each distribution can be sampled using any random number generator providing at least the same
functionality as the random module; this includes `samplespace.repeatablerandom`.

The classes in this module are primarily intended for storing information on random distributions
in configuration files using `Distribution.as_dict()`/`distribution_from_dict()`
or `Distribution.as_list()`/`distribution_from_list()`.

Distributions can be serialized to strings:
```python
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
``` 

Distributions can be specified in configuration files:
```python
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
```

### Algorithms

`samplespace.algorithms` implements several general-purpose sampling algorithms
such as binary roulette wheel sampling and alias tables.


### PyYAML Support

SampleSpace provides optional support for [PyYAML](https://pypi.org/project/PyYAML/),
which can be enabled via the `samplespace.pyyaml_support` submodule.

Repeatable Random Sequences:

```python
import yaml
from samplespace import RepeatableRandomSequence
import samplespace.pyyaml_support
samplespace.pyyaml_support.enable_yaml_support()

rrs = RepeatableRandomSequence(seed=678)
[rrs.randrange(10) for _ in range(5)]

# Serialize the sequence as YAML
as_yaml = yaml.dump(rrs) # '!samplespace.rrs\nhash_input: s1enBV+SSXk=\nindex: 5\nseed: 678\n'

rrs_from_yaml = yaml.load(as_yaml, Loader=yaml.FullLoader)
``` 

Distributions:

```python
import yaml
from samplespace import distributions
import samplespace.pyyaml_support
samplespace.pyyaml_support.enable_yaml_support()

gamma = distributions.Gamma(5.0, 3.0)
gamma_as_yaml = yaml.dump(gamma) # '!samplespace.distribution\nalpha: 5.0\nbeta: 3.0\ndistribution: gamma\n'

dist_from_yaml = yaml.load(gamma_as_yaml, Loader=yaml.FullLoader)
```


## Copyright and License 

SampleSpace was created by [Coriander V. Pines](http://corianderpines.org)
and is available under the
[BSD 3-Clause License](https://gitlab.com/cvpines/pysamplespace/-/blob/master/LICENSE).

The source is available on [GitLab](https://gitlab.com/cvpines/pysamplespace/).
