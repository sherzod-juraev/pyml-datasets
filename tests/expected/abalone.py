"""Facts about Abalone that are written down independently of the data file."""

from tests.expected import Expected

# The first row is the first line of the original file abalone.data of the UCI download, with
# the sex M stored as its code 2 (F, I, M are 0, 1, 2). The means are from the table "Statistics
# for numeric domains" of the file abalone.names. They have three decimals, so they are compared
# with a tolerance of half a unit of the last decimal.
# Columns of X: sex, length, diameter, height, whole_weight, shucked_weight, viscera_weight,
# shell_weight.
EXPECTED = Expected(
    shape=(4177, 8),
    n_classes=None,
    class_counts=None,
    first_row=(2.0, 0.455, 0.365, 0.095, 0.514, 0.2245, 0.101, 0.15),
    column_means={
        1: 0.524,
        2: 0.408,
        3: 0.140,
        4: 0.829,
        5: 0.359,
        6: 0.181,
        7: 0.239,
    },
    mean_tolerance=0.0005,
    n_missing=0,
)
