"""Facts about Forest Fires written down independently of the data file."""

from tests.expected import Expected

# Taken from the original file forestfires.csv of the UCI download, not from the NPZ file. The
# file has a header line and 13 columns: X, Y, month, day, FFMC, DMC, DC, ISI, temp, RH, wind,
# rain and area. The columns of X are the first twelve, month and day are integer codes in the
# order of INFO.categorical: the first fire of the file is on a Friday in March, so its month
# is 2 (mar) and its day is 4 (fri).
# The target (the area) has the mean 12.847292, the smallest value 0, the largest 1090.84, and
# 247 of the 517 fires have the area 0. The first row of the file has the area 0.
EXPECTED = Expected(
    shape=(517, 12),
    n_classes=None,
    class_counts=None,
    first_row=(7.0, 5.0, 2.0, 4.0, 86.2, 26.2, 94.3, 5.1, 8.2, 51.0, 6.7, 0.0),
    # Means of the ten numeric columns, computed from forestfires.csv of the source.
    column_means={
        0: 4.669246,
        1: 4.299807,
        4: 90.644681,
        5: 110.872340,
        6: 547.940039,
        7: 9.021663,
        8: 18.889168,
        9: 44.288201,
        10: 4.017602,
        11: 0.021663,
    },
    n_missing=0,
)
