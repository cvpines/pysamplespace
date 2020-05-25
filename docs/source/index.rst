SampleSpace: Cross-Platform Tools for Generating Random Numbers
===============================================================

.. image:: img/header.png
    :width: 100%
    :align: center
    :alt: SampleSpace banner

SampleSpace is a cross-platform library for describing and sampling from
random distributions.

While SampleSpace is primarily intended for creating
procedurally-generated content, it is also useful for Monte-Carlo
simulations, unit testing, and anywhere that flexible, repeatable random
numbers are required.

Installation is simple::

    $ pip install samplespace

SampleSpace's only dependency is
`xxHash <https://pypi.org/project/xxhash/>`_, though it optionally
offers additional functionality if
`PyYAML <https://pypi.org/project/PyYAML/>`_ is installed.

SampleSpace was created by Coriander V. Pines and is available under
the BSD 3-Clause License.

The source is available on
`GitLab <https://gitlab.com/cvpines/pysamplespace/>`_.


.. toctree::
    :maxdepth: 1
    :caption: Submodules

    repeatablerandom
    distributions
    algorithms
    pyyaml_support


.. toctree::
    :maxdepth: 1
    :caption: Info

    rrs_quality

