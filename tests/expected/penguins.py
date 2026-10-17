"""Facts about Palmer Penguins that are written down independently of the data file."""

from tests.expected import Expected

EXPECTED = Expected(
    shape=(344, 7),
    n_classes=3,
    class_counts=(152, 68, 124),
    first_row=(2.0, 39.1, 18.7, 181.0, 3750.0, 1.0, 2007.0),
    column_means={1: 43.9219, 2: 17.1512, 3: 200.9152, 4: 4201.7544},
    n_missing=19,
)
