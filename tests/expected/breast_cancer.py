"""Facts about Breast Cancer Wisconsin (Diagnostic), independent of the data file."""

from tests.expected import Expected

EXPECTED = Expected(
    shape=(569, 30),
    n_classes=2,
    class_counts=(212, 357),
    first_row=(17.99, 10.38, 122.8, 1001.0),
    column_means={0: 14.1273},
)
