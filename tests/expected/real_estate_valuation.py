"""Facts about Real Estate Valuation written down independently of the data file."""

from tests.expected import Expected

# Taken from the original file "Real estate valuation data set.xlsx" of the UCI download, not
# from the NPZ file. The only sheet has a header row and 8 columns: No, X1 transaction date,
# X2 house age, X3 distance to the nearest MRT station, X4 number of convenience stores,
# X5 latitude, X6 longitude and Y house price of unit area. The 414 data rows have the numbers
# 1 to 414 in No, so X is the six columns after No. The file has no missing values.
# The file has the transaction date with seven decimals (the first row: 2012.9166667), while
# ucimlrepo, where the NPZ file comes from, gives it rounded to three decimals (2012.917).
# That is why the first row has the rounded date and the tolerance of the means is larger
# than the default.
EXPECTED = Expected(
    shape=(414, 6),
    n_classes=None,
    class_counts=None,
    first_row=(2012.917, 32.0, 84.87882, 10.0, 24.98298, 121.54024),
    # Means of the six columns of X, computed from the xlsx file of the source.
    column_means={0: 2013.1490, 1: 17.7126, 2: 1083.8857, 3: 4.0942, 4: 24.9690, 5: 121.5334},
    mean_tolerance=1e-3,
    n_missing=0,
)
