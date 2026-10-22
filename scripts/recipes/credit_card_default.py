"""Recipe for the Default of Credit Card Clients dataset from UCI."""

from importlib.metadata import version
from typing import Final

import numpy as np
from ucimlrepo import fetch_ucirepo

from scripts.recipes._common import Built

_UCI_ID: Final = 350
_EXPECTED_SHAPE: Final = (30_000, 23)


def build() -> Built:
    """Download Default of Credit Card Clients from UCI and return it as a ``Built`` object.

    The shape, the feature dtypes, the target values and the feature descriptions are
    checked, so a silent change of the data on the UCI side is noticed instead of being
    saved: the features must be exactly ``(30000, 23)`` with integer dtypes, the target
    ``Y`` must contain exactly the values ``{0, 1}`` (binary classification), and every
    feature must have a non-empty, unique description in the UCI metadata.

    Returns
    -------
    Built
        Features as a ``(30000, 23)`` matrix and the ``Y`` binary classification target.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape, feature dtypes, target
        values or feature descriptions, or if the UCI metadata is missing.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("credit_card_default: UCI returns no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"credit_card_default: expected features of shape {_EXPECTED_SHAPE},"
            f" got {features.shape}."
        )
    non_integer = {
        str(col): str(dtype) for col, dtype in features.dtypes.items() if dtype.kind not in "iu"
    }
    if non_integer:
        raise ValueError(
            f"credit_card_default: expected all feature columns to be integer, "
            f"got non-integer dtypes: {non_integer}."
        )
    X = features.to_numpy(dtype=np.float64)
    if list(targets.columns) != ["Y"] or len(targets) != len(features):
        raise ValueError("credit_card_default: expected a single 'Y' target, one value per row.")
    y_raw = targets["Y"].to_numpy()
    unique = np.unique(y_raw)
    if not np.array_equal(unique, np.array([0, 1])):
        raise ValueError(
            f"credit_card_default: Y must contain exactly the values {{0, 1}},"
            f" got {unique.tolist()}."
        )
    y = y_raw.astype(np.int64)

    variables = dataset.variables
    if variables is None:
        raise ValueError("credit_card_default: UCI returns no variables metadata.")

    feature_vars = variables[variables["role"] == "Feature"]
    if len(feature_vars) != len(features.columns):
        raise ValueError(
            f"credit_card_default: expected {len(features.columns)} feature variables, "
            f"got {len(feature_vars)}."
        )
    raw_descriptions = dict(zip(feature_vars["name"], feature_vars["description"], strict=True))
    for name, desc in raw_descriptions.items():
        if not isinstance(desc, str) or desc.strip() == "":
            raise ValueError(
                f"credit_card_default: feature '{name}' has a missing or empty description."
            )

    if len(set(raw_descriptions.values())) != len(raw_descriptions):
        raise ValueError("credit_card_default: duplicated feature descriptions.")

    if set(raw_descriptions) != set(features.columns):
        raise ValueError(
            "credit_card_default: feature names in variables do not match features.columns."
        )
    feature_names = [str(raw_descriptions[name]) for name in features.columns]

    return Built(
        X=X,
        y=y,
        feature_names=feature_names,
        target_names=("No default payment", "Default payment"),
        extras={
            "source": f"UCI Machine Learning Repository, dataset {_UCI_ID}",
            "ucimlrepo_version": version("ucimlrepo"),
        },
    )
