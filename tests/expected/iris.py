"""Facts about Iris that are written down independently of the data file."""

from tests.expected import Expected

EXPECTED = Expected(
    shape=(150, 4),
    n_classes=3,
    class_counts=(50, 50, 50),
    first_row=(5.1, 3.5, 1.4, 0.2),
    column_means={0: 5.8433, 1: 3.0573, 2: 3.758, 3: 1.1993},
)
