"""Airfoil Self-Noise: scaled sound pressure level of NACA 0012 airfoil blade sections."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="airfoil_self_noise",
    title="Airfoil Self-Noise",
    task="regression",
    summary=(
        "Scaled sound pressure level in decibels of NACA 0012 airfoil blade sections, to be "
        "predicted from five inputs: the frequency, the angle of attack, the chord length, "
        "the free-stream velocity and the suction side displacement thickness. The 1503 "
        "examples are a NASA data set, obtained from a series of aerodynamic and acoustic "
        "tests of two and three-dimensional airfoil blade sections conducted in an anechoic "
        "wind tunnel."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/291/airfoil+self+noise",
    doi="10.24432/C5VW2C",
    creators=("Thomas Brooks", "D. Pope", "Michael Marcolini"),
    citation=(
        "Brooks, T., Pope, D., & Marcolini, M. (1989). Airfoil Self-Noise [Dataset]. UCI "
        "Machine Learning Repository. https://doi.org/10.24432/C5VW2C."
    ),
    obtained_from=(
        "UCI Machine Learning Repository, dataset 291, downloaded with the ucimlrepo package: "
        "all 1503 examples with 5 inputs. The ucimlrepo version is recorded in the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. Features and the target are stored as float64.",
        "The columns are named after their descriptions in the variables table of the source, "
        "written in lower case with underscores: attack-angle is stored as angle_of_attack, "
        "chord-length as chord_length, free-stream-velocity as free_stream_velocity, "
        "suction-side-displacement-thickness as suction_side_displacement_thickness, and the "
        "target scaled-sound-pressure as scaled_sound_pressure_level. frequency keeps its "
        "name. The features are stored in the order of the variables table.",
    ),
    verified_on="2026-10-29",
    notes=(
        "The NASA data set comprises different size NACA 0012 airfoils at various wind "
        "tunnel speeds and angles of attack. The span of the airfoil and the observer "
        "position were the same in all of the experiments.",
        "Units: the frequency is in Hz, the angle of attack in degrees, the chord length in "
        "meters, the free-stream velocity in meters per second, the suction side displacement "
        "thickness in meters and the scaled sound pressure level in decibels.",
        "In the data file of the source the frequency takes whole numbers from 200 to 20000 "
        "(21 different values), the angle of attack takes 27 different values from 0 to 22.2, "
        "the chord length takes 6 different values from 0.0254 to 0.3048 and the free-stream "
        "velocity takes 4 different values: 31.7, 39.6, 55.5 and 71.3.",
        "The variables table of UCI lists the angle of attack as binary, but the data file "
        "has 27 different values for it, as written above. It is stored as the number the "
        "source gives.",
    ),
)


def load_airfoil_self_noise() -> Dataset:
    """Load the Airfoil Self-Noise dataset (regression, 1503 samples, 5 features).

    Returns
    -------
    Dataset
        Dataset with the frequency, the angle of attack, the chord length, the free-stream
        velocity and the suction side displacement thickness as features, and the scaled
        sound pressure level in decibels as target. ``Dataset.info`` holds the license, the
        source and the citation.

    Examples
    --------
    >>> from pyml_datasets import load_airfoil_self_noise
    >>> X, y = load_airfoil_self_noise()
    >>> X.shape, y.shape
    ((1503, 5), (1503,))
    """
    return load_npz(INFO)
