"""Facts about Concrete Compressive Strength written down independently of the data file."""

from tests.expected import Expected

# Taken from the original file Concrete_Data.xls of the UCI download, not from the NPZ file.
# Columns of X: cement, blast_furnace_slag, fly_ash, water, superplasticizer, coarse_aggregate,
# fine_aggregate, age.
# That file has more decimals than the table of ucimlrepo, which the NPZ file stores: the
# amounts differ by at most 0.05, so the means differ by less than 0.0025. The means are
# therefore compared with a larger tolerance. See the notes of the dataset.
EXPECTED = Expected(
    shape=(1030, 8),
    n_classes=None,
    class_counts=None,
    first_row=(540.0, 0.0, 0.0, 162.0, 2.5, 1040.0, 676.0, 28.0),
    column_means={
        0: 281.1656,
        1: 73.8955,
        2: 54.1871,
        3: 181.5664,
        4: 6.2031,
        5: 972.9186,
        6: 773.5789,
        7: 45.6621,
    },
    mean_tolerance=0.005,
    n_missing=0,
)
