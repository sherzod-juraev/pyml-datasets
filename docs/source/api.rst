API reference
=============

Dataset
-------

.. autoclass:: pyml_datasets.Dataset
    :members:
    :show-inheritance:
    :exclude-members: X, y, feature_names, target_names, description

Iterating over a ``Dataset`` yields ``X`` and then ``y``.

Loaders
-------

.. autofunction:: pyml_datasets.load_iris

.. autofunction:: pyml_datasets.load_wine

.. autofunction:: pyml_datasets.load_breast_cancer

.. autofunction:: pyml_datasets.load_diabetes

.. autofunction:: pyml_datasets.load_linnerud

.. autofunction:: pyml_datasets.load_california_housing
