"""Forest Fires: 517 forest fires in northeast Portugal, burned area from weather and indices."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="forest_fires",
    title="Forest Fires",
    task="regression",
    summary=(
        "Forest fires in the northeast region of Portugal. Each of the 517 samples is a fire "
        "described by its place on the map of the Montesinho park, the month and the day of "
        "the week, four indices of the Fire Weather Index system and four weather "
        "observations. The goal is to predict the burned area in hectares. The source calls "
        "it a difficult regression task."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/162/forest+fires",
    doi="10.24432/C5D88D",
    creators=("Paulo Cortez", "Anbal Morais"),
    citation=(
        "Cortez, P. & Morais, A. (2007). Forest Fires [Dataset]. UCI Machine Learning "
        "Repository. https://doi.org/10.24432/C5D88D"
    ),
    obtained_from=(
        "UCI Machine Learning Repository, dataset 162, downloaded with the ucimlrepo package: "
        "all 517 examples with 12 inputs and the target area. The ucimlrepo version is "
        "recorded in the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. The features and the target are stored as float64.",
        "The categorical features month and day are stored as integer codes, in the order of "
        "the category names listed for each feature: the months from jan to dec and the days "
        "of the week from mon to sun.",
    ),
    verified_on="2026-11-04",
    categorical={
        "month": (
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "jun",
            "jul",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
        ),
        "day": ("mon", "tue", "wed", "thu", "fri", "sat", "sun"),
    },
    notes=(
        "The target area is very skewed towards 0.0. The source page says that it may make "
        "sense to model it with the logarithm transform, and the paper of the source used "
        "ln(x+1). The values are stored as released, without any transform.",
        "X and Y are the coordinates of a grid on the map of the Montesinho park, stored as "
        "whole numbers.",
        "The variables table of UCI lists DMC, rain and area as integers, although the ranges "
        "that it gives for them have decimals. The values are stored as real numbers.",
    ),
)


def load_forest_fires() -> Dataset:
    """Load the Forest Fires dataset (regression, 517 samples, 12 features).

    Returns
    -------
    Dataset
        Dataset with the place, the time and the weather of a fire, two of the features
        (month and day) categorical integer codes, and the burned area in hectares as the
        target. ``Dataset.info`` holds the license, the source and the citation.

    Examples
    --------
    >>> from pyml_datasets import load_forest_fires
    >>> X, y = load_forest_fires()
    >>> X.shape, y.shape
    ((517, 12), (517,))
    """
    return load_npz(INFO)
