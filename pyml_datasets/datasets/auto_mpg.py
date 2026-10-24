"""Auto MPG: city-cycle fuel consumption in miles per gallon of 398 cars."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="auto_mpg",
    title="Auto MPG",
    task="regression",
    summary=(
        "City-cycle fuel consumption in miles per gallon of 398 cars, to be predicted from "
        "seven features: the number of cylinders, the displacement, the horsepower, the "
        "weight, the acceleration, the model year and the origin of the car. Some "
        "horsepower values are missing."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/9/auto+mpg",
    doi="10.24432/C5859H",
    creators=("R. Quinlan",),
    citation=(
        "Quinlan, R. (1993). Auto MPG [Dataset]. UCI Machine Learning Repository. "
        "https://doi.org/10.24432/C5859H"
    ),
    obtained_from=(
        "UCI Machine Learning Repository, dataset 9, downloaded with the ucimlrepo package: "
        "all 398 examples of the revised version, in which the source already removed 8 "
        "examples of the StatLib original because their mpg was unknown. The ucimlrepo "
        "version is recorded in the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. Features and the target mpg are stored as float64.",
        "The 6 missing values of horsepower are stored as NaN.",
        "The column car_name, which UCI marks as an identifier and describes as a string "
        "that is unique for each instance, is not stored, because X holds numbers only. "
        "The other columns are stored in the order of the data description of the source.",
    ),
    verified_on="2026-10-24",
    references=(
        "Quinlan, R. (1993). Combining Instance-Based and Model-Based Learning. In "
        "Proceedings on the Tenth International Conference of Machine Learning, 236-243, "
        "University of Massachusetts, Amherst. Morgan Kaufmann.",
    ),
    has_missing=True,
    notes=(
        "The source took the data from the StatLib library at Carnegie Mellon University, "
        "where it was used in the 1983 American Statistical Association Exposition, and calls "
        "it a slightly modified version of that dataset.",
        "6 values of horsepower are missing and stored as NaN. Impute them or drop the rows "
        "before fitting a model that cannot handle NaN.",
        "cylinders, model_year and origin are multi-valued discrete features in the source and "
        "are stored as its numbers. The source does not say what the numbers of origin stand "
        "for, so origin has no category names.",
        "mpg is fuel consumption in miles per gallon, so a higher value means a more "
        "economical car.",
    ),
)


def load_auto_mpg() -> Dataset:
    """Load the Auto MPG dataset (regression, 398 samples, 7 features).

    The dataset has 6 missing values in ``horsepower``, stored as ``NaN``.

    Returns
    -------
    Dataset
        Dataset with the characteristics of a car as features and its fuel consumption in
        miles per gallon as target. ``Dataset.info`` holds the license, the source and the
        citation.

    Examples
    --------
    >>> from pyml_datasets import load_auto_mpg
    >>> X, y = load_auto_mpg()
    >>> X.shape, y.shape
    ((398, 7), (398,))
    """
    return load_npz(INFO)
