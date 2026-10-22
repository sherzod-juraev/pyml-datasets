"""Facts about Default of Credit Card Clients, independent of the data file."""

from tests.expected import Expected

EXPECTED = Expected(
    shape=(30000, 23),
    n_classes=2,
    # 6636 clients with a default payment (22.12 percent), 23364 without.
    class_counts=(23364, 6636),
    # LIMIT_BAL, SEX, EDUCATION, MARRIAGE, AGE of the first client in the original file.
    first_row=(20000.0, 2.0, 2.0, 1.0, 24.0),
    n_missing=0,
)
