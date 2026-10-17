"""Public types of the package: ``Dataset`` and ``DatasetInfo``."""

import re
from collections.abc import Iterator, Mapping
from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any, Final, Literal, get_args

import numpy as np
from numpy.typing import NDArray

LicenseId = Literal["CC0-1.0", "CC-BY-4.0"]
Task = Literal["classification", "regression"]

LICENSE_IDS: Final[tuple[str, ...]] = get_args(LicenseId)
TASKS: Final[tuple[str, ...]] = get_args(Task)

_NAME_PATTERN: Final = re.compile(r"[a-z][a-z0-9_]*")
_DOI_PATTERN: Final = re.compile(r"10\.\d{4,9}/\S+")


def _plain(value: Any) -> Any:
    """Convert tuples and mappings into JSON-friendly lists and dicts.

    Parameters
    ----------
    value : object
        A value produced by ``dataclasses.asdict``.

    Returns
    -------
    object
        The same value with tuples replaced by lists, recursively.
    """
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [_plain(item) for item in value]
    return value


@dataclass(frozen=True, kw_only=True)
class DatasetInfo:
    """Provenance and license of a dataset.

    Every bundled dataset has exactly one ``DatasetInfo``. Everything that talks about
    a dataset's origin (the description stored in its file, the ``NOTICE.md`` file, the
    tables of the README and of the documentation) is generated from it, so a fact is
    written down only once. Invalid values are rejected when the object is created.

    Attributes
    ----------
    name : str
        Short identifier, lowercase letters, digits and underscores. It is also the name
        of the data file (``<name>.npz``) and of the loader (``load_<name>``).
    title : str
        Human readable name of the dataset.
    task : {"classification", "regression"}
        Kind of the prediction problem. It decides the dtype of ``y``.
    summary : str
        One or two sentences about what the dataset contains.
    license : {"CC0-1.0", "CC-BY-4.0"}
        SPDX identifier of the license the data is redistributed under. Only licenses
        that allow redistribution with at most an attribution duty are accepted.
    license_url : str
        Address of the license text.
    source : str
        Name of the original publisher of the data.
    source_url : str
        Page of the original publisher that describes the dataset and its license.
    doi : str or None
        DOI of the dataset or of the release that was used, without the resolver prefix.
    creators : tuple of str
        The people or institutions that created the dataset, as the source names them.
    citation : str
        The citation the source asks users to give, copied as the source writes it.
    obtained_from : str
        Where the bytes in this repository really came from. It can differ from
        ``source`` when a copy of the dataset was used.
    changes : tuple of str
        Every change made to the data, as the attribution duty of the license requires.
    verified_on : str
        ISO date (``YYYY-MM-DD``) on which the license was last checked at the source.
    references : tuple of str, default=()
        Papers and records that describe the dataset or that the source asks to cite.
    categorical : mapping of str to tuple of str, default={}
        Categorical features. Each key is a feature name, each value the category names
        in the order of the integer codes stored in ``X`` (code ``0`` is the first name).
    has_missing : bool, default=False
        Whether ``X`` contains missing values. They are stored as ``NaN``.
    notes : tuple of str, default=()
        Warnings and remarks that users of the dataset should see.
    """

    name: str
    title: str
    task: Task
    summary: str
    license: LicenseId
    license_url: str
    source: str
    source_url: str
    doi: str | None
    creators: tuple[str, ...]
    citation: str
    obtained_from: str
    changes: tuple[str, ...]
    verified_on: str
    references: tuple[str, ...] = ()
    categorical: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    has_missing: bool = False
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Reject values that would make the provenance of the dataset unclear.

        Raises
        ------
        ValueError
            If the name, the task, the license, a URL, the DOI or the verification date
            is malformed, or if the creators, the citation or the changes are empty.
        """
        name = self.name
        if not _NAME_PATTERN.fullmatch(name):
            raise ValueError(f"{name!r} is not a valid dataset name.")
        if self.task not in TASKS:
            raise ValueError(f"{name}: task must be one of {TASKS}, got {self.task!r}.")
        if self.license not in LICENSE_IDS:
            raise ValueError(f"{name}: license must be one of {LICENSE_IDS}, got {self.license!r}.")
        for label, url in (("license_url", self.license_url), ("source_url", self.source_url)):
            if not url.startswith("https://"):
                raise ValueError(f"{name}: {label} must be an https URL, got {url!r}.")
        if self.doi is not None and not _DOI_PATTERN.fullmatch(self.doi):
            raise ValueError(f"{name}: {self.doi!r} is not a valid DOI.")
        if not self.creators:
            raise ValueError(f"{name}: at least one creator is required.")
        if not self.citation.strip():
            raise ValueError(f"{name}: the citation must not be empty.")
        if not self.changes:
            raise ValueError(f"{name}: list the changes made to the data.")
        try:
            date.fromisoformat(self.verified_on)
        except ValueError as error:
            message = f"{name}: verified_on must be an ISO date, got {self.verified_on!r}."
            raise ValueError(message) from error
        for feature, categories in self.categorical.items():
            if not categories:
                raise ValueError(f"{name}: categorical feature {feature!r} has no categories.")

    def to_dict(self) -> dict[str, Any]:
        """Return the information as a dict of plain Python values.

        Returns
        -------
        dict of str to object
            Strings, lists, dicts, booleans and ``None`` only, so the result can be
            written as JSON.
        """
        return dict(_plain(asdict(self)))


@dataclass(frozen=True, eq=False)
class Dataset:
    """Dataset with its data matrix, targets and metadata.

    Iterating over a ``Dataset`` yields ``X`` and ``y``, so
    ``X, y = load_iris()`` works as well as ``data = load_iris()``.

    Attributes
    ----------
    X : ndarray of shape (n_samples, n_features)
        Data matrix. Missing values, if the dataset has any, are ``NaN``.
    y : ndarray of shape (n_samples,) or (n_samples, n_targets)
        Target values.
    feature_names : tuple of str
        Names of the columns of ``X``.
    target_names : tuple of str or None
        Class names for classification or target names for multi-output
        regression, ``None`` if the source does not provide them.
    description : str
        Description of the dataset: what it is, where it comes from, how to cite it, which
        license applies and which changes were made.
    info : DatasetInfo
        The structured form of the provenance and license information.
    """

    X: NDArray[np.float64]
    y: NDArray[Any]
    feature_names: tuple[str, ...]
    target_names: tuple[str, ...] | None
    description: str
    info: DatasetInfo

    def __iter__(self) -> Iterator[NDArray[Any]]:
        """Yield ``X`` and ``y`` in this order."""
        yield self.X
        yield self.y

    @property
    def has_missing(self) -> bool:
        """Whether ``X`` contains at least one missing value (``NaN``)."""
        return bool(np.isnan(self.X).any())

    @property
    def categorical_features(self) -> tuple[int, ...]:
        """Column indices of the categorical features, stored as integer codes.

        The category names of a column are in ``info.categorical`` under the feature name.
        """
        return tuple(
            index for index, name in enumerate(self.feature_names) if name in self.info.categorical
        )
