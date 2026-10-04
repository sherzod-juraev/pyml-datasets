"""Types shared by the dataset recipes."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Literal

from numpy.typing import ArrayLike


@dataclass(frozen=True)
class Built:
    """Raw result of a dataset recipe, before it is converted and saved.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        Data matrix, converted to ``float64`` when saved.
    y : array-like of shape (n_samples,) or (n_samples, n_targets)
        Targets, converted to ``int64`` for classification and ``float64`` for regression.
    feature_names : sequence of str
        Names of the columns of ``X``.
    target_names : sequence of str or None
        Class names or target names, ``None`` if the source does not provide them.
    description : str
        Description of the dataset. It should contain the source, the citation and the license,
        because it is stored in the file and shown by ``Dataset.description``.
    task : {"classification", "regression"}
        Decides the dtype of ``y``.
    extras : mapping of str to str
        Extra informational strings saved next to the arrays, for example the version of the
        library the data came from. The loader ignores them.
    """

    X: ArrayLike
    y: ArrayLike
    feature_names: Sequence[str]
    target_names: Sequence[str] | None
    description: str
    task: Literal["classification", "regression"]
    extras: Mapping[str, str] = field(default_factory=dict)
