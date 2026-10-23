"""Bank Marketing: phone-call marketing campaigns of a Portuguese bank, 45211 clients."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="bank_marketing",
    title="Bank Marketing",
    task="classification",
    summary=(
        "Direct marketing campaigns (phone calls) of a Portuguese banking institution. Each of "
        "the 45211 samples is a client described by 16 features: bank client data, the last "
        "contact of the current campaign and the outcome of the previous campaign. The goal is "
        "to predict whether the client subscribed a term deposit."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/222/bank+marketing",
    doi="10.24432/C5K306",
    creators=("S. Moro", "P. Rita", "P. Cortez"),
    citation=(
        "Moro, S., Rita, P., & Cortez, P. (2014). Bank Marketing [Dataset]. UCI Machine "
        "Learning Repository. https://doi.org/10.24432/C5K306"
    ),
    obtained_from=(
        "UCI Machine Learning Repository, dataset 222, downloaded with the ucimlrepo package: "
        "all 45211 examples with 16 inputs (the bank-full version). The ucimlrepo version is "
        "recorded in the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. Numeric features are stored as float64 and the "
        "target as int64 labels.",
        "Categorical features are stored as integer codes, in the order of the category "
        "names listed for each feature. The target is 0 for no and 1 for yes.",
        "Entries of job, education, contact and poutcome that the UCI release marks as "
        "missing are stored as the category unknown, which the data description of the "
        "source lists for these features. No NaN values are stored.",
        "The column that UCI calls day_of_week is named day, because the source describes "
        "it as the day of the month of the last contact.",
    ),
    verified_on="2026-10-23",
    references=(
        "Moro, S., Cortez, P., & Rita, P. (2014). A data-driven approach to predict the "
        "success of bank telemarketing. Decision Support Systems, 62, 22-31.",
    ),
    categorical={
        "job": (
            "admin.",
            "blue-collar",
            "entrepreneur",
            "housemaid",
            "management",
            "retired",
            "self-employed",
            "services",
            "student",
            "technician",
            "unemployed",
            "unknown",
        ),
        "marital": ("divorced", "married", "single"),
        "education": ("primary", "secondary", "tertiary", "unknown"),
        "default": ("no", "yes"),
        "housing": ("no", "yes"),
        "loan": ("no", "yes"),
        "contact": ("cellular", "telephone", "unknown"),
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
        "poutcome": ("failure", "other", "success", "unknown"),
    },
    notes=(
        "The duration of the last call is only known after the call, and the call ends "
        "with the answer. The source advises to use duration for benchmarks only and to "
        "drop it for a realistic predictive model.",
        "pdays is -1 for clients who were not contacted in a previous campaign. The value is "
        "kept as it is in the source.",
        "The classes are not balanced: far fewer clients subscribed than not.",
    ),
)


def load_bank_marketing() -> Dataset:
    """Load the Bank Marketing dataset (classification, 45211 samples, 16 features).

    Returns
    -------
    Dataset
        Dataset with client and campaign features, 9 of them categorical integer codes,
        and two classes: the client did not (0) or did (1) subscribe a term deposit.
        ``Dataset.info`` holds the license, the source and the citation.

    Examples
    --------
    >>> from pyml_datasets import load_bank_marketing
    >>> X, y = load_bank_marketing()
    >>> X.shape, y.shape
    ((45211, 16), (45211,))
    """
    return load_npz(INFO)
