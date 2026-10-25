"""Facts about Energy Efficiency written down independently of the data file."""

from tests.expected import Expected

# Taken from the original file ENB2012_data.xlsx of the UCI download, not from the NPZ file.
# Columns of X: relative_compactness, surface_area, wall_area, roof_area, overall_height,
# orientation, glazing_area, glazing_area_distribution (X1 to X8 of the source).
# y has two columns: the heating load (Y1) and the cooling load (Y2). In the source file their
# means are 22.3072 and 24.5878, the smallest values are 6.01 and 10.9, and the first row has
# 15.55 and 21.33.
EXPECTED = Expected(
    shape=(768, 8),
    n_classes=None,
    class_counts=None,
    first_row=(0.98, 514.5, 294.0, 110.25, 7.0, 2.0, 0.0, 0.0),
    column_means={
        0: 0.7642,
        1: 671.7083,
        2: 318.5,
        3: 176.6042,
        4: 5.25,
        5: 3.5,
        6: 0.2344,
        7: 2.8125,
    },
    n_missing=0,
    n_targets=2,
)
