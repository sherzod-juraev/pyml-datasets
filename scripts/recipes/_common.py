"""Types shared by the dataset recipes."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from numpy.typing import ArrayLike


@dataclass(frozen=True)
class Built:
    """Raw result of a dataset recipe, before it is converted and saved.

    Everything about the origin of the data (license, citation, changes) is **not** here:
    it lives in the ``INFO`` of the dataset module, and the build script combines both.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        Data matrix, converted to ``float64`` when saved. Missing values must be ``NaN``,
        and categorical features must already be integer codes.
    y : array-like of shape (n_samples,) or (n_samples, n_targets)
        Targets, converted to ``int64`` for classification and ``float64`` for regression.
        Targets must never be missing.
    feature_names : sequence of str
        Names of the columns of ``X``.
    target_names : sequence of str or None, default=None
        Class names or target names, ``None`` if the source does not provide them.
    extras : mapping of str to str, default={}
        Informational strings saved in the file, for example the version of the library the
        data came from or the digest of the downloaded file. The loader ignores them.
    """

    X: ArrayLike
    y: ArrayLike
    feature_names: Sequence[str]
    target_names: Sequence[str] | None = None
    extras: Mapping[str, str] = field(default_factory=dict)
