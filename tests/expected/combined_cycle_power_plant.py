"""Facts about Combined Cycle Power Plant written down independently of the data file."""

from tests.expected import Expected

# Taken from the original file Folds5x2_pp.xlsx of the UCI download, not from the NPZ file.
# The file has five sheets, the data shuffled five times. The first row below is the first row
# of Sheet1, which is also the first row of the table that ucimlrepo returns. The means are the
# same in all five sheets.
# Columns of X: temperature (AT), exhaust_vacuum (V), ambient_pressure (AP), relative_humidity
# (RH). The target PE has the mean 454.3650, the smallest value 420.26 and the largest 495.76,
# and the first row of Sheet1 has PE 463.26.
EXPECTED = Expected(
    shape=(9568, 4),
    n_classes=None,
    class_counts=None,
    first_row=(14.96, 41.76, 1024.07, 73.17),
    column_means={
        0: 19.6512,
        1: 54.3058,
        2: 1013.2591,
        3: 73.3090,
    },
    n_missing=0,
)
