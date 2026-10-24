"""Facts about Auto MPG that are written down independently of the data file."""

from tests.expected import Expected

# Taken from the original file auto-mpg.data of the UCI download, not from the NPZ file.
# Columns of X: cylinders, displacement, horsepower, weight, acceleration, model_year, origin.
EXPECTED = Expected(
    shape=(398, 7),
    n_classes=None,
    class_counts=None,
    first_row=(8.0, 307.0, 130.0, 3504.0, 12.0, 70.0, 1.0),
    column_means={
        0: 5.4548,
        1: 193.4259,
        2: 104.4694,
        3: 2970.4246,
        4: 15.5681,
        5: 76.0101,
        6: 1.5729,
    },
    n_missing=6,
)
