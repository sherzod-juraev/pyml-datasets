"""Facts about Airfoil Self-Noise written down independently of the data file."""

from tests.expected import Expected

# Taken from the original file airfoil_self_noise.dat of the UCI download, not from the NPZ
# file. The file has no header and six columns.
# Columns of X: frequency, angle_of_attack, chord_length, free_stream_velocity,
# suction_side_displacement_thickness.
# The target (the sixth column) has the mean 124.83594278, the smallest value 103.38, the
# largest 140.987, and the first row of the file has the value 126.201.
# The chord length and the thickness are small numbers, so the means are compared with a
# tolerance much smaller than the default.
EXPECTED = Expected(
    shape=(1503, 5),
    n_classes=None,
    class_counts=None,
    first_row=(800.0, 0.0, 0.3048, 71.3, 0.00266337),
    column_means={
        0: 2886.38057219,
        1: 6.78230206,
        2: 0.13654824,
        3: 50.86074518,
        4: 0.01113988,
    },
    mean_tolerance=1e-6,
    n_missing=0,
)
