:mod:`samplespace.pyyaml_support` - YAML serialization support
==============================================================

.. module:: samplespace.pyyaml_support
    :synopsis: Add YAML serialization support to :mod:`samplespace`.

----------


When enabled, this module provides YAML serialization support for
classes in :mod:`samplespace.repeatablerandom`,
:mod:`samplespace.distributions`, and :mod:`samplespace.algorithms`.

The ``yaml`` module provided by
`PyYaml <https://pypi.org/project/PyYAML/>`_ is required to use this
module, and an exception will be thrown if it is not available.

.. tip::
    Once the module is imported, :func:`enable_yaml_support` must be
    called to enable YAML support.


-------

.. autofunction:: enable_yaml_support


Examples
--------

Repeatable random sequence:

    >>> import yaml
    >>> from samplespace import RepeatableRandomSequence
    >>> import samplespace.pyyaml_support
    >>> samplespace.pyyaml_support.enable_yaml_support()
    >>>
    >>> rrs = RepeatableRandomSequence(seed=678)
    >>> [rrs.randrange(10) for _ in range(5)]
    [7, 7, 0, 8, 3]
    >>>
    >>> # Serialize the sequence as YAML
    ...
    >>> as_yaml = yaml.dump(rrs)
    >>> as_yaml
    '!samplespace.rrs\nhash_input: s1enBV+SSXk=\nindex: 5\nseed: 678\n'
    >>>
    >>> # Generate some random values to compare against later
    ...
    >>> [rrs.randrange(10) for _ in range(5)]
    [0, 5, 1, 3, 9]
    >>> [rrs.randrange(10) for _ in range(5)]
    [7, 1, 1, 0, 5]
    >>> [rrs.randrange(10) for _ in range(5)]
    [2, 9, 1, 4, 8]
    >>>
    >>> # Restore the saved sequence
    ...
    >>> rrs2 = yaml.load(as_yaml, Loader=yaml.FullLoader)
    >>>
    >>> # Verify that values match those at time of serialization
    ...
    >>> [rrs2.randrange(10) for _ in range(5)]
    [0, 5, 1, 3, 9]
    >>> [rrs2.randrange(10) for _ in range(5)]
    [7, 1, 1, 0, 5]
    >>> [rrs2.randrange(10) for _ in range(5)]
    [2, 9, 1, 4, 8]

Distributions:

    >>> import yaml
    >>> from samplespace import distributions
    >>> import samplespace.pyyaml_support
    >>> samplespace.pyyaml_support.enable_yaml_support()
    >>>
    >>> gamma = distributions.Gamma(5.0, 3.0)
    >>> gamma_as_yaml = yaml.dump(gamma)
    >>> print(gamma_as_yaml)
    !samplespace.distribution
    alpha: 5.0
    beta: 3.0
    distribution: gamma
    >>> assert yaml.load(gamma_as_yaml, Loader=yaml.FullLoader) == gamma
    >>>
    >>> zipf = distributions.Zipf(0.9, 10)
    >>> zipf_as_yaml = yaml.dump(zipf)
    >>> print(zipf_as_yaml)
    !samplespace.distribution
    distribution: zipf
    n: 10
    s: 0.9
    >>> assert yaml.load(zipf_as_yaml, Loader=yaml.FullLoader) == zipf
    >>>
    >>> wcat = distributions.WeightedCategorical(
    ...     population='abcde',
    ...     cum_weights=[0.1, 0.4, 0.6, 0.7, 1.1])
    >>> wcat_as_yaml = yaml.dump(wcat)
    >>> print(wcat_as_yaml)
    !samplespace.distribution
    distribution: weightedcategorical
    items:
    - - a
      - 0.1
    - - b
      - 0.30000000000000004
    - - c
      - 0.19999999999999996
    - - d
      - 0.09999999999999998
    - - e
      - 0.40000000000000013
    >>> assert yaml.load(wcat_as_yaml, Loader=yaml.FullLoader) == wcat

Algorithms:

    >>> import yaml
    >>> from samplespace.algorithms import AliasTable
    >>> import samplespace.pyyaml_support
    >>> samplespace.pyyaml_support.enable_yaml_support()
    >>>
    >>> at = AliasTable.from_weights([0.1, 0.3, 0.5, 0.2, 0.6, 0.7])
    >>> at.alias
    [4, 5, 0, 5, 2, 4]
    >>> at.probability
    [0.25, 0.7499999999999998, 1.0, 0.5, 0.7499999999999991, 0.9999999999999996]
    >>>
    >>> at_as_yaml = yaml.dump(at)
    >>> print(at_as_yaml)
    !samplespace.aliastable
    alias:
    - 4
    - 5
    - 0
    - 5
    - 2
    - 4
    probability:
    - 0.25
    - 0.7499999999999998
    - 1.0
    - 0.5
    - 0.7499999999999991
    - 0.9999999999999996
    >>> at2 = yaml.load(at_as_yaml, Loader=yaml.FullLoader)
    >>> assert at2.alias == at.alias
    >>> assert at2.probability == at.probability

