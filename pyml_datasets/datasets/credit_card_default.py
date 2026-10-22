"""Default of Credit Card Clients: payment records of credit card holders in Taiwan."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="credit_card_default",
    title="Default of Credit Card Clients",
    task="classification",
    summary=(
        "Data on 30,000 credit card clients in Taiwan, measured from April to "
        "September 2005, with 23 features covering credit limit, demographics, repayment "
        "status, bill amounts and previous payments. The task is to predict whether the "
        "client will default on the next month's payment (binary target Y)."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients",
    doi="10.24432/C55S3H",
    creators=("I-Cheng Yeh",),
    citation=(
        "Yeh, I. (2009). Default of Credit Card Clients [Dataset]. "
        "UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H."
    ),
    obtained_from=(
        "UCI dataset 350, read with the ucimlrepo package "
        "(version stored in extras['ucimlrepo_version'])."
    ),
    changes=(
        "Converted to the NumPy NPZ format.",
        "The row identifier column ID of the source is not included.",
        "Column names X1..X23 were replaced with the feature names from the UCI "
        "variable descriptions; the values themselves were not modified.",
        "Features were converted to float64.",
        "Target Y was kept as integer 0/1 codes, and the class names were set from the "
        "Yes/No meaning in the source description.",
    ),
    notes=(
        "SEX uses the codes 1 (male) and 2 (female) as documented by the source, so the "
        "category codes do not start at 0.",
        "EDUCATION is documented as 1 = graduate school, 2 = university, 3 = high school, "
        "4 = others. The data also contains the undocumented values 0, 5 and 6.",
        "MARRIAGE is documented as 1 = married, 2 = single, 3 = others. The data also "
        "contains the undocumented value 0.",
        "The repayment status columns PAY_0, PAY_2, PAY_3, PAY_4, PAY_5 and PAY_6 are "
        "documented with the scale -1 = pay duly, 1 to 9 = payment delay in months. The "
        "data also contains the undocumented values -2 and 0 in all six columns, and the "
        "value 9 does not occur. The value 1 does not occur in PAY_5 and PAY_6. There is no "
        "column PAY_1: PAY_0 is the repayment status of September 2005, as in the source.",
        "All raw values are kept as they are in the source; no recoding, cleaning or "
        "removal of rows was applied.",
    ),
    verified_on="2026-10-22",
)


def load_credit_card_default() -> Dataset:
    """Load the Default of Credit Card Clients dataset.

    Binary classification with 30000 samples and 23 features: credit limit, demographics,
    six months of repayment status, bill amounts and previous payments.

    Returns
    -------
    Dataset
        ``X`` has shape ``(30000, 23)``. ``y`` has shape ``(30000,)`` and holds the codes
        0 (no default payment next month) and 1 (default payment next month), in the order
        of ``target_names``. ``Dataset.info`` holds the license, the source and the
        citation.

    Examples
    --------
    >>> from pyml_datasets import load_credit_card_default
    >>> X, y = load_credit_card_default()
    >>> X.shape, y.shape
    ((30000, 23), (30000,))
    """
    return load_npz(INFO)
