"""Adult: census records of 48842 people, predict whether the income is above 50K a year."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="adult",
    title="Adult",
    task="classification",
    summary=(
        "Records extracted from the 1994 Census database. Each of the 48842 samples is a "
        "person described by 14 features, for example age, education, occupation, marital "
        "status, race, sex, capital gain and loss, working hours and native country. The "
        "goal is to predict whether the yearly income of the person is above 50000 dollars."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/2/adult",
    doi="10.24432/C5XW20",
    creators=("Barry Becker", "Ronny Kohavi"),
    citation=(
        "Becker, B. & Kohavi, R. (1996). Adult [Dataset]. UCI Machine Learning Repository. "
        "https://doi.org/10.24432/C5XW20"
    ),
    obtained_from=(
        "UCI Machine Learning Repository, dataset 2, downloaded with the ucimlrepo package: "
        "all 48842 examples with 14 inputs, the training part of the source (adult.data, "
        "32561 rows) followed by its test part (adult.test, 16281 rows). The ucimlrepo "
        "version is recorded in the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. Numeric features are stored as float64 and the "
        "target as int64 labels.",
        "Categorical features are stored as integer codes, in the order of the category "
        "names listed for each feature. The categories are in alphabetical order, except "
        "those of education, which are in the order of the education level, so its code is "
        "education_num minus one. The target is 0 for <=50K and 1 for >50K.",
        "The training part and the test part of the source are stored together, the training "
        "part first. The test part writes the target with a trailing dot (<=50K. and >50K.). "
        "The dot is dropped, so both parts use the same two classes.",
        "Entries of workclass, occupation and native_country that the source marks as missing "
        "are stored as NaN. UCI delivers some of them as the text ? and some as empty cells, "
        "both become NaN.",
        "The hyphens in the column names are replaced with underscores, for example "
        "marital-status becomes marital_status.",
    ),
    verified_on="2026-11-08",
    references=(
        "Kohavi, R. (1996). Scaling Up the Accuracy of Naive-Bayes Classifiers: a "
        "Decision-Tree Hybrid. Proceedings of the Second International Conference on "
        "Knowledge Discovery and Data Mining.",
    ),
    categorical={
        "workclass": (
            "Federal-gov",
            "Local-gov",
            "Never-worked",
            "Private",
            "Self-emp-inc",
            "Self-emp-not-inc",
            "State-gov",
            "Without-pay",
        ),
        "education": (
            "Preschool",
            "1st-4th",
            "5th-6th",
            "7th-8th",
            "9th",
            "10th",
            "11th",
            "12th",
            "HS-grad",
            "Some-college",
            "Assoc-voc",
            "Assoc-acdm",
            "Bachelors",
            "Masters",
            "Prof-school",
            "Doctorate",
        ),
        "marital_status": (
            "Divorced",
            "Married-AF-spouse",
            "Married-civ-spouse",
            "Married-spouse-absent",
            "Never-married",
            "Separated",
            "Widowed",
        ),
        "occupation": (
            "Adm-clerical",
            "Armed-Forces",
            "Craft-repair",
            "Exec-managerial",
            "Farming-fishing",
            "Handlers-cleaners",
            "Machine-op-inspct",
            "Other-service",
            "Priv-house-serv",
            "Prof-specialty",
            "Protective-serv",
            "Sales",
            "Tech-support",
            "Transport-moving",
        ),
        "relationship": (
            "Husband",
            "Not-in-family",
            "Other-relative",
            "Own-child",
            "Unmarried",
            "Wife",
        ),
        "race": ("Amer-Indian-Eskimo", "Asian-Pac-Islander", "Black", "Other", "White"),
        "sex": ("Female", "Male"),
        "native_country": (
            "Cambodia",
            "Canada",
            "China",
            "Columbia",
            "Cuba",
            "Dominican-Republic",
            "Ecuador",
            "El-Salvador",
            "England",
            "France",
            "Germany",
            "Greece",
            "Guatemala",
            "Haiti",
            "Holand-Netherlands",
            "Honduras",
            "Hong",
            "Hungary",
            "India",
            "Iran",
            "Ireland",
            "Italy",
            "Jamaica",
            "Japan",
            "Laos",
            "Mexico",
            "Nicaragua",
            "Outlying-US(Guam-USVI-etc)",
            "Peru",
            "Philippines",
            "Poland",
            "Portugal",
            "Puerto-Rico",
            "Scotland",
            "South",
            "Taiwan",
            "Thailand",
            "Trinadad&Tobago",
            "United-States",
            "Vietnam",
            "Yugoslavia",
        ),
    },
    has_missing=True,
    notes=(
        "Missing entries, the text ? in the source, occur in workclass, occupation and "
        "native_country: 6465 values in 3620 rows, which leaves 45222 complete rows, the "
        "number that the source documentation gives. The missing entries are NaN, so fill or "
        "drop them before fitting a model that cannot handle NaN.",
        "The first 32561 rows are the training part of the source and the last 16281 rows are "
        "its test part, so slicing the rows gives back the split of the source.",
        "The classes are not balanced: 11687 of the 48842 people, 23.93 percent, are in the "
        "class above 50K, as the source documentation states.",
        "education_num is the education level as a number. It holds the same information as "
        "education, because every education has exactly one education_num in the source.",
        "Rows that repeat an earlier row are kept as they are in the source.",
        "race and sex are features of the dataset, and the UCI variables table marks them as "
        "demographic variables. A model that uses them can reproduce social bias, so check "
        "its fairness before it is used for decisions about people.",
    ),
)


def load_adult() -> Dataset:
    """Load the Adult dataset (classification, 48842 samples, 14 features).

    Returns
    -------
    Dataset
        Dataset with person features, 8 of them categorical integer codes, and two classes:
        the yearly income is at most 50K (0) or above 50K (1). Missing entries of three
        features are ``NaN``. ``Dataset.info`` holds the license, the source and the
        citation.

    Examples
    --------
    >>> from pyml_datasets import load_adult
    >>> X, y = load_adult()
    >>> X.shape, y.shape
    ((48842, 14), (48842,))
    """
    return load_npz(INFO)
