API reference
=============

Dataset
-------

.. autoclass:: pyml_datasets.Dataset
    :members:
    :exclude-members: X, y, feature_names, target_names, description, info

Iterating over a ``Dataset`` yields ``X`` and then ``y``.

DatasetInfo
-----------

.. autoclass:: pyml_datasets.DatasetInfo
    :members: to_dict

Finding datasets
----------------

.. autofunction:: pyml_datasets.list_datasets

.. autofunction:: pyml_datasets.get_info

.. autofunction:: pyml_datasets.load_dataset

Loaders
-------

.. include:: /_generated/api_loaders.inc
