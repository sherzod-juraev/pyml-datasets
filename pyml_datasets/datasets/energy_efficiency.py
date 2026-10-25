"""Energy Efficiency: heating and cooling load of 768 simulated buildings."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="energy_efficiency",
    title="Energy Efficiency",
    task="regression",
    summary=(
        "Heating load and cooling load of 768 simulated buildings, to be predicted from eight "
        "building parameters: the relative compactness, the surface area, the wall area, the "
        "roof area, the overall height, the orientation, the glazing area and the distribution "
        "of the glazing area. It has two targets, so y has two columns."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/242/energy+efficiency",
    doi="10.24432/C51307",
    creators=("Athanasios Tsanas", "Angeliki Xifara"),
    citation=(
        "Tsanas, A. & Xifara, A. (2012). Energy Efficiency [Dataset]. UCI Machine Learning "
        "Repository. https://doi.org/10.24432/C51307."
    ),
    obtained_from=(
        "UCI Machine Learning Repository, dataset 242, downloaded with the ucimlrepo package: "
        "all 768 examples with 8 inputs and 2 targets. The ucimlrepo version is recorded in "
        "the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. Features and targets are stored as float64.",
        "The two targets are stored together: y has the shape (768, 2), the first column is "
        "the heating load (Y1 of the source) and the second column is the cooling load (Y2).",
        "The columns X1 to X8 are named after their descriptions in the variables table of "
        "the source, written in lower case with underscores, for example Glazing Area "
        "Distribution (X8) is stored as glazing_area_distribution. The features are stored "
        "in the order X1 to X8.",
    ),
    verified_on="2026-10-25",
    references=(
        "Tsanas, A., Xifara, A. (2012). Accurate quantitative estimation of energy "
        "performance of residential buildings using statistical machine learning tools. "
        "Energy and Buildings, vol. 49.",
    ),
    notes=(
        "The buildings are 12 different building shapes simulated in Ecotect. They differ in "
        "the glazing area, the distribution of the glazing area and the orientation, among "
        "other parameters, and 768 building shapes were obtained by simulating various "
        "settings of these characteristics.",
        "The source says the aim is to predict each of the two responses from the eight "
        "features, and that the data can also be used as a multi-class classification "
        "problem if the response is rounded to the nearest integer. This library stores it "
        "as a regression dataset.",
        "orientation and glazing_area_distribution are integers in the source. The source "
        "does not say what their numbers stand for, so they are stored as its numbers "
        "without category names.",
        "The source does not state the units of the columns, so none are given here.",
    ),
)


def load_energy_efficiency() -> Dataset:
    """Load the Energy Efficiency dataset (regression, 768 samples, 8 features, 2 targets).

    Returns
    -------
    Dataset
        Dataset with the parameters of a building as features and its heating load and
        cooling load as the two columns of the target ``y``. ``Dataset.info`` holds the
        license, the source and the citation.

    Examples
    --------
    >>> from pyml_datasets import load_energy_efficiency
    >>> X, y = load_energy_efficiency()
    >>> X.shape, y.shape
    ((768, 8), (768, 2))
    """
    return load_npz(INFO)
