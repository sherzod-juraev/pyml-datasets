"""Facts about Adult that are written down independently of the data file."""

from tests.expected import Expected

EXPECTED = Expected(
    shape=(48842, 14),
    n_classes=2,
    class_counts=(37155, 11687),
    # The first person of adult.data: 39, State-gov, 77516, Bachelors, 13, Never-married,
    # Adm-clerical, Not-in-family, White, Male, 2174, 0, 40, United-States. Categories are
    # integer codes, see INFO. The counts and the means come from adult.data and adult.test
    # of the UCI download (rows of both files, the labels without their trailing dot).
    # adult.names agrees: 48842 instances (train 32561, test 16281), 23.93 percent above 50K
    # and 45222 instances without unknown values, which is 48842 minus 3620 rows with a "?".
    first_row=(39.0, 6.0, 77516.0, 12.0, 13.0, 4.0, 0.0, 1.0, 4.0, 1.0, 2174.0, 0.0, 40.0, 38.0),
    column_means={0: 38.6436, 2: 189664.1346, 4: 10.0781, 10: 1079.0676, 11: 87.5023, 12: 40.4224},
    n_missing=6465,
)
