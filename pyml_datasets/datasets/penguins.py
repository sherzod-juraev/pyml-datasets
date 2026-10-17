"""Penguins: body measurements of 344 penguins from the Palmer Archipelago."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="penguins",
    title="Palmer Penguins",
    task="classification",
    summary=(
        "Body measurements of 344 penguins of three species (Adelie, Chinstrap and Gentoo) "
        "observed on three islands of the Palmer Archipelago, Antarctica, between 2007 and "
        "2009. Some values are missing."
    ),
    license="CC0-1.0",
    license_url="https://creativecommons.org/publicdomain/zero/1.0/",
    source="palmerpenguins data package (Palmer Station Antarctica LTER and K. Gorman)",
    source_url="https://allisonhorst.github.io/palmerpenguins/",
    doi="10.5281/zenodo.3960218",
    creators=("Kristen B. Gorman", "Palmer Station Antarctica LTER"),
    citation=(
        "Horst AM, Hill AP, Gorman KB (2020). palmerpenguins: Palmer Archipelago "
        "(Antarctica) penguin data. R package version 0.1.0. "
        "https://allisonhorst.github.io/palmerpenguins/. doi:10.5281/zenodo.3960218."
    ),
    obtained_from=(
        "The file inst/extdata/penguins.csv of the GitHub repository "
        "allisonhorst/palmerpenguins. Its SHA-256 digest is pinned in the build recipe."
    ),
    changes=(
        "Converted to the NumPy NPZ format. Measurements are stored as float64 and the "
        "species as int64 labels (0 = Adelie, 1 = Chinstrap, 2 = Gentoo).",
        "The columns island and sex are stored as integer codes, see the categorical "
        "features. The missing values (NA in the CSV file) are stored as NaN.",
        "All columns except the species are features. No row and no column was removed.",
    ),
    verified_on="2026-10-17",
    references=(
        "Gorman KB, Williams TD, Fraser WR (2014). Ecological sexual dimorphism and "
        "environmental variability within a community of Antarctic penguins (genus "
        "Pygoscelis). PLoS ONE 9(3):e90081. https://doi.org/10.1371/journal.pone.0090081",
        "Adelie data record: https://doi.org/10.6073/pasta/98b16d7d563f265cb52372c8ca99e60f",
        "Gentoo data record: https://doi.org/10.6073/pasta/7fca67fb28d56ee2ffa3d9370ebda689",
        "Chinstrap data record: https://doi.org/10.6073/pasta/c14dfcfada8ea13a17536e73eb6fbe9e",
    ),
    categorical={
        "island": ("Biscoe", "Dream", "Torgersen"),
        "sex": ("female", "male"),
    },
    has_missing=True,
    notes=(
        "The data are released under CC0. The package page also asks anyone who wants to "
        "publish with the data to contact its creator about the analysis and final products, "
        "and expects users to follow the US LTER Network Data Access Policy.",
    ),
)


def load_penguins() -> Dataset:
    """Load the Palmer Penguins dataset (classification, 344 samples, 7 features).

    The dataset has missing values, stored as ``NaN``, and two categorical features,
    stored as integer codes.

    Returns
    -------
    Dataset
        Dataset with 3 penguin species as classes. ``Dataset.info`` holds the license, the
        source, the citation and the names of the categories.

    Examples
    --------
    >>> from pyml_datasets import load_penguins
    >>> data = load_penguins()
    >>> data.X.shape, data.y.shape
    ((344, 7), (344,))
    >>> data.has_missing
    True
    """
    return load_npz(INFO)
