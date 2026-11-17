"""Facts about the bundled data files that are read without loading the arrays."""

import zipfile
from importlib.resources import files
from importlib.resources.abc import Traversable
from typing import Final

from numpy.lib import format as npy_format

_PACKAGE: Final = "pyml_datasets"
_DATA_DIR: Final = "data"
_FEATURES: Final = "X.npy"


def _data_file(name: str) -> Traversable:
    """Return the bundled ``<name>.npz`` file.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    importlib.resources.abc.Traversable
        The data file of the dataset.

    Raises
    ------
    FileNotFoundError
        If the file is not part of the installed package.
    """
    resource = files(_PACKAGE) / _DATA_DIR / f"{name}.npz"
    if not resource.is_file():
        raise FileNotFoundError(f"Dataset file '{name}.npz' is missing from the package.")
    return resource


def read_shape(name: str) -> tuple[int, int]:
    """Read the shape of ``X`` from the header of its array, without loading the data.

    An NPZ file is a ZIP archive of ``.npy`` files, and every ``.npy`` file starts with a
    header that holds the shape.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    tuple of int
        Number of samples and number of features.

    Raises
    ------
    FileNotFoundError
        If the data file is missing from the package.
    ValueError
        If ``X`` is not a matrix or its header has a format this module does not read.
    """
    with (
        _data_file(name).open("rb") as file,
        zipfile.ZipFile(file) as archive,
        archive.open(_FEATURES) as member,
    ):
        version = npy_format.read_magic(member)
        if version == (1, 0):
            shape, _, _ = npy_format.read_array_header_1_0(member)
        elif version == (2, 0):
            shape, _, _ = npy_format.read_array_header_2_0(member)
        else:
            raise ValueError(f"Dataset '{name}': unsupported array format {version}.")
    if len(shape) != 2:
        raise ValueError(f"Dataset '{name}': X has shape {shape}, expected a matrix.")
    return shape[0], shape[1]


def read_size(name: str) -> int:
    """Return the size of the data file in bytes.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    int
        Size of ``<name>.npz`` in bytes.

    Raises
    ------
    FileNotFoundError
        If the data file is missing from the package.
    """
    with _data_file(name).open("rb") as file:
        return file.seek(0, 2)
