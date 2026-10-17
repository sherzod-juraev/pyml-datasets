"""Facts about Wine that are written down independently of the data file."""

from tests.expected import Expected

EXPECTED = Expected(
    shape=(178, 13),
    n_classes=3,
    class_counts=(59, 71, 48),
    first_row=(14.23, 1.71, 2.43, 15.6),
    column_means={0: 13.0006, 12: 746.8933},
)
