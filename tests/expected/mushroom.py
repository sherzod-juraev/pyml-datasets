"""Facts about Mushroom that are written down independently of the data file."""

from tests.expected import Expected

# Taken from agaricus-lepiota.data and agaricus-lepiota.names of the UCI download, not from the
# NPZ file. The file has 8124 rows of 23 comma separated values, the class first (e or p) and
# the 22 features after it. The names file agrees: 8124 instances, 4208 edible and 3916
# poisonous, and 2480 missing values, all of them (written ?) in stalk-root. Every feature is a
# category, stored as the position of its one-letter code among the codes that occur in the
# file, in alphabetical order, see INFO. The first row of the file is p,x,s,n,t,p,f,c,n,k,e,e,
# s,s,w,w,p,w,o,p,k,s,u, so the first sample is poisonous (class 1) and its features are
# x,s,n,t,p,f,c,n,k,e,e,s,s,w,w,p,w,o,p,k,s,u. Every mean is the mean of the codes of a column
# that follows from the number of rows of each code in the file (stalk_root without its
# missing entries). The class counts are in the order of the class codes: edible, poisonous.
EXPECTED = Expected(
    shape=(8124, 22),
    n_classes=2,
    class_counts=(4208, 3916),
    first_row=(
        5.0,
        2.0,
        4.0,
        1.0,
        6.0,
        1.0,
        0.0,
        1.0,
        4.0,
        0.0,
        2.0,
        2.0,
        2.0,
        7.0,
        7.0,
        0.0,
        2.0,
        1.0,
        4.0,
        2.0,
        3.0,
        5.0,
    ),
    column_means={
        0: 3.3481,
        1: 1.8277,
        2: 4.5047,
        3: 0.4156,
        4: 4.1448,
        5: 0.9742,
        6: 0.1615,
        7: 0.3092,
        8: 4.8107,
        9: 0.5672,
        10: 0.5974,
        11: 1.5751,
        12: 1.6036,
        13: 5.8163,
        14: 5.7947,
        15: 0.0,
        16: 1.9655,
        17: 1.0694,
        18: 2.292,
        19: 3.5968,
        20: 3.644,
        21: 1.5086,
    },
    n_missing=2480,
)
