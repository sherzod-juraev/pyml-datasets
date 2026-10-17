"""Facts about Wine Quality that are written down independently of the data file."""

from tests.expected import Expected

EXPECTED = Expected(
    shape=(6497, 11),
    n_classes=None,
    class_counts=None,
    first_row=(7.4, 0.7, 0.0, 1.9, 0.076, 11.0, 34.0, 0.9978, 3.51, 0.56, 9.4),
    column_means={0: 7.2153},
)
