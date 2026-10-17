"""Wine: chemical analysis of 178 Italian wines from three cultivars."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="wine",
    title="Wine",
    task="classification",
    summary=(
        "Results of a chemical analysis of wines grown in the same region of Italy but "
        "derived from three different cultivars. 13 constituents were measured in each wine."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/109/wine",
    doi="10.24432/C5PC7J",
    creators=("Stefan Aeberhard", "M. Forina"),
    citation=(
        "Aeberhard, S. & Forina, M. (1992). Wine [Dataset]. UCI Machine Learning Repository. "
        "https://doi.org/10.24432/C5PC7J"
    ),
    obtained_from=(
        "scikit-learn (sklearn.datasets.load_wine), which redistributes a copy of the data. "
        "The scikit-learn version is recorded in the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. Values are stored as float64 and the cultivar as "
        "int64 labels.",
        "The cultivar labels are 0, 1 and 2 (the UCI file numbers them 1, 2 and 3).",
        "Feature and class names follow scikit-learn.",
    ),
    verified_on="2026-10-17",
    references=(
        "Forina, M. et al. PARVUS: an extendable package of programs for data exploration, "
        "classification and correlation. Institute of Pharmaceutical and Food Analysis and "
        "Technologies, Genoa, Italy.",
    ),
)


def load_wine() -> Dataset:
    """Load the Wine dataset (classification, 178 samples, 13 features).

    Returns
    -------
    Dataset
        Dataset with 3 classes of wine cultivars. ``Dataset.info`` holds the license, the
        source and the citation.

    Examples
    --------
    >>> from pyml_datasets import load_wine
    >>> X, y = load_wine()
    >>> X.shape, y.shape
    ((178, 13), (178,))
    """
    return load_npz(INFO)
