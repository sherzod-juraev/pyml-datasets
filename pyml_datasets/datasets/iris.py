"""Iris: measurements of 150 iris flowers from three species."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="iris",
    title="Iris",
    task="classification",
    summary=(
        "Measurements of 150 iris flowers from three species, 50 flowers each: the length "
        "and the width of the sepals and of the petals."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/53/iris",
    doi="10.24432/C56C76",
    creators=("R. A. Fisher",),
    citation=(
        "Fisher, R. (1936). Iris [Dataset]. UCI Machine Learning Repository. "
        "https://doi.org/10.24432/C56C76"
    ),
    obtained_from=(
        "scikit-learn (sklearn.datasets.load_iris), which redistributes a copy of the data. "
        "The scikit-learn version is recorded in the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. Values are stored as float64 and the species as "
        "int64 labels (0 = setosa, 1 = versicolor, 2 = virginica).",
        "Samples 35 and 38 follow Fisher's paper, as corrected in scikit-learn. The UCI page "
        "lists these two samples as differing between its file and the paper.",
        "Feature and class names follow scikit-learn.",
    ),
    verified_on="2026-10-17",
    references=(
        "Fisher, R. A. (1936). The use of multiple measurements in taxonomic problems. "
        "Annals of Eugenics, 7(2), 179-188.",
    ),
)


def load_iris() -> Dataset:
    """Load the Iris dataset (classification, 150 samples, 4 features).

    Returns
    -------
    Dataset
        Dataset with 3 classes of iris plants. ``Dataset.info`` holds the license, the
        source and the citation.

    Examples
    --------
    >>> from pyml_datasets import load_iris
    >>> X, y = load_iris()
    >>> X.shape, y.shape
    ((150, 4), (150,))
    """
    return load_npz(INFO)
