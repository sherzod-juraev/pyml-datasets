"""Facts about German Credit that are written down independently of the data file."""

from tests.expected import Expected

EXPECTED = Expected(
    shape=(1000, 20),
    n_classes=2,
    class_counts=(700, 300),
    # The first applicant of german.data: A11, 6, A34, A43, 1169, A65, A75, 4, A93, A101, 4,
    # A121, 67, A143, A152, 2, A173, 1, A192, A201, class 1 (good). Categories are integer
    # codes in the order of INFO.categorical, so A11 is 0, A34 is 4, A43 is 3 and so on.
    first_row=(
        0.0,
        6.0,
        4.0,
        3.0,
        1169.0,
        4.0,
        4.0,
        4.0,
        2.0,
        0.0,
        4.0,
        0.0,
        67.0,
        2.0,
        1.0,
        2.0,
        2.0,
        1.0,
        1.0,
        0.0,
    ),
    # Means of the seven numeric columns, computed from german.data of the source.
    column_means={
        1: 20.9030,
        4: 3271.2580,
        7: 2.9730,
        10: 2.8450,
        12: 35.5460,
        15: 1.4070,
        17: 1.1550,
    },
    n_missing=0,
)
