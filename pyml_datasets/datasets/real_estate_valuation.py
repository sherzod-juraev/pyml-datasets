"""Real Estate Valuation: 414 house sales in Taiwan, price of unit area from 6 features."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="real_estate_valuation",
    title="Real Estate Valuation",
    task="regression",
    summary=(
        "Market historical data of real estate valuation, collected from the Sindian District "
        "of New Taipei City, Taiwan. Each of the 414 samples is a house sale described by 6 "
        "features: the transaction date, the house age, the distance to the nearest MRT "
        "station, the number of convenience stores in the living circle on foot and the "
        "latitude and the longitude. The goal is to predict the house price of unit area."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/477/real+estate+valuation+data+set",
    doi="10.24432/C5J30W",
    creators=("I-Cheng Yeh",),
    citation=(
        "Yeh, I. (2018). Real Estate Valuation [Dataset]. UCI Machine Learning Repository. "
        "https://doi.org/10.24432/C5J30W"
    ),
    obtained_from=(
        "UCI Machine Learning Repository, dataset 477, downloaded with the ucimlrepo package: "
        "all 414 examples with 6 inputs and the target. The ucimlrepo version is recorded in "
        "the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. The features and the target are stored as float64.",
        "The identifier column No, the numbers 1 to 414, is not stored, because it is not a "
        "feature.",
        "The column names are written in lowercase with underscores, and the prefixes X1 to X6 "
        "and Y are dropped, for example X3 distance to the nearest MRT station becomes "
        "distance_to_nearest_mrt_station.",
    ),
    verified_on="2026-11-09",
    references=(
        "Yeh, I., & Hsu, T.-K. (2018). Building real estate valuation models with comparative "
        "approach through case-based reasoning. Applied Soft Computing.",
    ),
    notes=(
        "The source says that the data set was randomly split into a training part (2/3 of the "
        "samples) and a testing part (1/3), but its file has no column that tells which sample "
        "belongs to which part. All 414 samples are stored and the split is not provided.",
        "The transaction date is a number: 2013.250 is March 2013 and 2013.500 is June 2013, "
        "as the source describes. Only 12 different dates occur, from 2012.667 to 2013.583. "
        "ucimlrepo gives the dates rounded to three decimals, while the xlsx file of the UCI "
        "page has seven (the first sale: 2012.9166667), so the stored dates differ from that "
        "file by 0.0004 at most.",
        "The target is the house price of unit area in 10000 New Taiwan Dollar per Ping, where "
        "a Ping is a local unit of area, 1 Ping = 3.3 square meters, as the source gives.",
    ),
)


def load_real_estate_valuation() -> Dataset:
    """Load the Real Estate Valuation dataset (regression, 414 samples, 6 features).

    Returns
    -------
    Dataset
        Dataset with the transaction date, the age and the surroundings of a house, and the
        house price of unit area (10000 New Taiwan Dollar per Ping) as the target.
        ``Dataset.info`` holds the license, the source and the citation.

    Examples
    --------
    >>> from pyml_datasets import load_real_estate_valuation
    >>> X, y = load_real_estate_valuation()
    >>> X.shape, y.shape
    ((414, 6), (414,))
    """
    return load_npz(INFO)
