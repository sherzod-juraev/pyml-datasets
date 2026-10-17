"""Facts about Digits that are written down independently of the data file."""

from tests.expected import Expected

EXPECTED = Expected(
    shape=(1797, 64),
    n_classes=10,
    class_counts=(178, 182, 177, 183, 181, 182, 181, 179, 174, 180),
    first_row=(0.0, 0.0, 5.0, 13.0),
    column_means={63: 0.3645},
)
