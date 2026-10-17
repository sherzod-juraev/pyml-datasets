"""Wine Quality: physicochemical tests and tasting scores of 6497 vinho verde wines."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="wine_quality",
    title="Wine Quality",
    task="regression",
    summary=(
        "Physicochemical measurements of 6497 red and white vinho verde wines from the "
        "north of Portugal, and the quality of each wine as a score between 0 and 10 given "
        "by wine tasters. The quality scores are ordered and not balanced, so the dataset "
        "can be used for regression as well as for classification."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/186/wine+quality",
    doi="10.24432/C56S3T",
    creators=("Paulo Cortez", "A. Cerdeira", "F. Almeida", "T. Matos", "J. Reis"),
    citation=(
        "Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Wine Quality "
        "[Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56S3T"
    ),
    obtained_from=(
        "UCI Machine Learning Repository, dataset 186, downloaded with the ucimlrepo "
        "package. The ucimlrepo version is recorded in the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. Features and the quality score are stored as float64.",
        "The red wines (1599) and the white wines (4898) are stored together. As in the UCI "
        "release, the colour of the wine is not a feature.",
    ),
    verified_on="2026-10-17",
    references=(
        "Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Modeling wine "
        "preferences by data mining from physicochemical properties. Decision Support "
        "Systems, 47(4), 547-553.",
    ),
)


def load_wine_quality() -> Dataset:
    """Load the Wine Quality dataset (regression, 6497 samples, 11 features).

    Returns
    -------
    Dataset
        Dataset with physicochemical features and the sensory quality score as target.
        ``Dataset.info`` holds the license, the source and the citation.

    Examples
    --------
    >>> from pyml_datasets import load_wine_quality
    >>> X, y = load_wine_quality()
    >>> X.shape, y.shape
    ((6497, 11), (6497,))
    """
    return load_npz(INFO)
