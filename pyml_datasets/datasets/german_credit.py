"""German Credit: 1000 credit applicants described by 20 attributes, good or bad credit risk."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="german_credit",
    title="German Credit",
    task="classification",
    summary=(
        "The Statlog German Credit Data classify people, described by 20 attributes, as good or "
        "bad credit risks. Each of the 1000 samples is a credit applicant described by 13 "
        "categorical and 7 numeric attributes. The source states that the dataset requires a "
        "cost matrix: classifying a bad customer as good is five times worse than classifying "
        "a good customer as bad."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data",
    doi="10.24432/C5NC77",
    creators=("Hans Hofmann",),
    citation=(
        "Hofmann, H. (1994). Statlog (German Credit Data) [Dataset]. UCI Machine Learning "
        "Repository. https://doi.org/10.24432/C5NC77"
    ),
    obtained_from=(
        "UCI Machine Learning Repository, dataset 144, downloaded with the ucimlrepo package: "
        "the original categorical/symbolic form of the data (the file german.data), all 1000 "
        "examples with 20 attributes. The numeric version of the source (german.data-numeric) "
        "is not used. The ucimlrepo version is recorded in the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. Numeric features are stored as float64 and the "
        "target as int64 labels.",
        "Categorical features are stored as integer codes, in the order of the category names "
        "listed for each feature. Every category name starts with the code of the source "
        "(for example A11), followed by the meaning that the source gives to the code.",
        "The attributes, which the source calls Attribute1 to Attribute20, have descriptive "
        "names taken from the data description of the source, in the order of the source.",
        "The target is 0 for a good and 1 for a bad credit risk. The source codes them as 1 "
        "and 2, in the same order.",
    ),
    verified_on="2026-11-03",
    categorical={
        "checking_status": (
            "A11: < 0 DM",
            "A12: 0 <= ... < 200 DM",
            "A13: >= 200 DM / salary assignments for at least 1 year",
            "A14: no checking account",
        ),
        "credit_history": (
            "A30: no credits taken / all credits paid back duly",
            "A31: all credits at this bank paid back duly",
            "A32: existing credits paid back duly till now",
            "A33: delay in paying off in the past",
            "A34: critical account / other credits existing (not at this bank)",
        ),
        "purpose": (
            "A40: car (new)",
            "A41: car (used)",
            "A42: furniture/equipment",
            "A43: radio/television",
            "A44: domestic appliances",
            "A45: repairs",
            "A46: education",
            "A47: (vacation - does not exist?)",
            "A48: retraining",
            "A49: business",
            "A410: others",
        ),
        "savings": (
            "A61: < 100 DM",
            "A62: 100 <= ... < 500 DM",
            "A63: 500 <= ... < 1000 DM",
            "A64: >= 1000 DM",
            "A65: unknown / no savings account",
        ),
        "employment_since": (
            "A71: unemployed",
            "A72: < 1 year",
            "A73: 1 <= ... < 4 years",
            "A74: 4 <= ... < 7 years",
            "A75: >= 7 years",
        ),
        "personal_status_sex": (
            "A91: male, divorced/separated",
            "A92: female, divorced/separated/married",
            "A93: male, single",
            "A94: male, married/widowed",
            "A95: female, single",
        ),
        "other_debtors": (
            "A101: none",
            "A102: co-applicant",
            "A103: guarantor",
        ),
        "property": (
            "A121: real estate",
            "A122: if not A121: building society savings agreement / life insurance",
            "A123: if not A121/A122: car or other, not in savings",
            "A124: unknown / no property",
        ),
        "other_installment_plans": (
            "A141: bank",
            "A142: stores",
            "A143: none",
        ),
        "housing": (
            "A151: rent",
            "A152: own",
            "A153: for free",
        ),
        "job": (
            "A171: unemployed / unskilled - non-resident",
            "A172: unskilled - resident",
            "A173: skilled employee / official",
            "A174: management / self-employed / highly qualified employee / officer",
        ),
        "telephone": (
            "A191: none",
            "A192: yes, registered under the customer's name",
        ),
        "foreign_worker": (
            "A201: yes",
            "A202: no",
        ),
    },
    notes=(
        "The source requires a cost matrix. Its rows are the actual class and its columns the "
        "predicted class, and a correct decision costs 0. Classifying a bad customer as good "
        "costs 5 and classifying a good customer as bad costs 1. With the classes of this "
        "file (0 good, 1 bad) the matrix is [[0, 1], [5, 0]]. The matrix is not stored in "
        "the file, so a user has to apply it.",
        "The classes are not balanced: 700 good and 300 bad credit risks.",
        "The integer codes of a categorical feature are labels, not quantities. Some "
        "features are ordered (for example savings), but the codes are not distances, and "
        "unordered features such as purpose have no order at all.",
        "The source lists the category A47 of purpose and the category A95 of "
        "personal_status_sex, but neither occurs in the 1000 samples. They stay in the lists "
        "of categories, so the codes keep the order of the source.",
        "personal_status_sex mixes the sex and the marital status of the applicant, and age "
        "and foreign_worker describe the applicant as a person. Use these attributes with "
        "care: a model that decides about real people on such grounds can be unfair.",
    ),
)


def load_german_credit() -> Dataset:
    """Load the German Credit dataset (classification, 1000 samples, 20 features).

    Returns
    -------
    Dataset
        Dataset with credit applicants described by 20 features, 13 of them categorical
        integer codes, and two classes: a good (0) or a bad (1) credit risk.
        ``Dataset.info`` holds the license, the source, the citation and the cost matrix
        of the source in its notes.

    Examples
    --------
    >>> from pyml_datasets import load_german_credit
    >>> X, y = load_german_credit()
    >>> X.shape, y.shape
    ((1000, 20), (1000,))
    """
    return load_npz(INFO)
