"""Concrete Compressive Strength: strength in MPa of 1030 concrete mixtures."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="concrete_strength",
    title="Concrete Compressive Strength",
    task="regression",
    summary=(
        "Compressive strength in MPa of 1030 concrete samples, to be predicted from eight "
        "features: the amounts of seven ingredients of the mixture (cement, blast furnace slag, "
        "fly ash, water, superplasticizer, coarse aggregate and fine aggregate, in kg per cubic "
        "metre) and the age of the concrete in days."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength",
    doi="10.24432/C5PK67",
    creators=("I-Cheng Yeh",),
    citation=(
        "Yeh, I. (1998). Concrete Compressive Strength [Dataset]. UCI Machine Learning "
        "Repository. https://doi.org/10.24432/C5PK67"
    ),
    obtained_from=(
        "UCI Machine Learning Repository, dataset 165, downloaded with the ucimlrepo package: "
        "all 1030 examples with 8 inputs. The ucimlrepo version is recorded in the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. Features and the target are stored as float64.",
        "The names of the columns are written in lower case with underscores, for example "
        "Blast Furnace Slag is stored as blast_furnace_slag. The features are stored in the "
        "order of the data description of the source, the target is the concrete compressive "
        "strength.",
    ),
    verified_on="2026-10-24",
    references=(
        "Yeh, I. (1998). Modeling of strength of high-performance concrete using artificial "
        "neural networks. Cement and Concrete Research, Vol. 28, No. 12.",
    ),
    notes=(
        "The seven ingredients are given in kg in a m3 mixture, the age in days (1 to 365) "
        "and the compressive strength in MPa.",
        "The source describes the compressive strength of concrete as a highly nonlinear "
        "function of age and ingredients.",
        "The data file that UCI offers for download (Concrete_Data.xls) has more decimals than "
        "the table that ucimlrepo returns and that is stored here: the amounts of the "
        "ingredients differ by at most 0.05 and the strength by less than 0.005.",
    ),
)


def load_concrete_strength() -> Dataset:
    """Load the Concrete Compressive Strength dataset (regression, 1030 samples, 8 features).

    Returns
    -------
    Dataset
        Dataset with the amounts of the ingredients and the age of the concrete as features
        and its compressive strength in MPa as target. ``Dataset.info`` holds the license,
        the source and the citation.

    Examples
    --------
    >>> from pyml_datasets import load_concrete_strength
    >>> X, y = load_concrete_strength()
    >>> X.shape, y.shape
    ((1030, 8), (1030,))
    """
    return load_npz(INFO)
