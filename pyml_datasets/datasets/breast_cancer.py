"""Breast Cancer Wisconsin (Diagnostic): features of 569 breast mass images."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="breast_cancer",
    title="Breast Cancer Wisconsin (Diagnostic)",
    task="classification",
    summary=(
        "Features computed from digitized images of fine needle aspirates of breast masses. "
        "They describe the cell nuclei in each image, and the task is to tell malignant "
        "masses from benign ones."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic",
    doi="10.24432/C5DW2B",
    creators=("William Wolberg", "Olvi Mangasarian", "Nick Street", "W. Street"),
    citation=(
        "Wolberg, W., Mangasarian, O., Street, N., & Street, W. (1993). Breast Cancer "
        "Wisconsin (Diagnostic) [Dataset]. UCI Machine Learning Repository. "
        "https://doi.org/10.24432/C5DW2B"
    ),
    obtained_from=(
        "scikit-learn (sklearn.datasets.load_breast_cancer), which redistributes a copy of "
        "the data. The scikit-learn version is recorded in the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. Values are stored as float64 and the diagnosis "
        "as int64 labels (0 = malignant, 1 = benign).",
        "The diagnosis is a number instead of the letters used in the UCI file, and the "
        "sample identifier column is not included.",
        "Feature and class names follow scikit-learn.",
    ),
    verified_on="2026-10-17",
    references=(
        "W. N. Street, W. H. Wolberg and O. L. Mangasarian. Nuclear feature extraction for "
        "breast tumor diagnosis. IS&T/SPIE 1993 International Symposium on Electronic "
        "Imaging: Science and Technology, volume 1905, pages 861-870, San Jose, CA, 1993.",
        "O. L. Mangasarian, W. N. Street and W. H. Wolberg. Breast cancer diagnosis and "
        "prognosis via linear programming. Operations Research, 43(4), pages 570-577, "
        "July-August 1995.",
        "W. H. Wolberg, W. N. Street, and O. L. Mangasarian. Machine learning techniques to "
        "diagnose breast cancer from fine-needle aspirates. Cancer Letters 77 (1994) 163-171.",
    ),
    notes=(
        "This dataset is for learning about machine learning methods. It is not a medical "
        "tool and must not be used to diagnose anything.",
    ),
)


def load_breast_cancer() -> Dataset:
    """Load the Breast Cancer Wisconsin (Diagnostic) dataset.

    Binary classification with 569 samples and 30 features.

    Returns
    -------
    Dataset
        Dataset with malignant (0) and benign (1) classes. ``Dataset.info`` holds the
        license, the source and the citation.

    Examples
    --------
    >>> from pyml_datasets import load_breast_cancer
    >>> X, y = load_breast_cancer()
    >>> X.shape, y.shape
    ((569, 30), (569,))
    """
    return load_npz(INFO)
