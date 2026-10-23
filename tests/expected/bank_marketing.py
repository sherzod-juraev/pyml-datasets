"""Facts about Bank Marketing that are written down independently of the data file."""

from tests.expected import Expected

EXPECTED = Expected(
    shape=(45211, 16),
    n_classes=2,
    class_counts=(39922, 5289),
    # The first client of the source file: 58, management, married, tertiary, no, 2143, yes,
    # no, unknown, 5, may, 261, 1, -1, 0, unknown. Categories are integer codes, see INFO.
    first_row=(
        58.0,
        4.0,
        1.0,
        2.0,
        0.0,
        2143.0,
        1.0,
        0.0,
        2.0,
        5.0,
        4.0,
        261.0,
        1.0,
        -1.0,
        0.0,
        3.0,
    ),
    column_means={0: 40.9362, 5: 1362.2721, 11: 258.1631, 12: 2.7638, 13: 40.1978, 14: 0.5803},
    n_missing=0,
)
