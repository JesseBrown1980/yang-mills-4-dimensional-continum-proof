# Class-sign bands on SU(2) at sides of at least 2, exact rationals. Integers only. json=0.
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep import *
import su2_lib as Q


# ---- SU(2): class signs from real-part bands, on the side-1 slices, against exact rational configurations. Each pattern is a sign of the real part on a union of bands.
def sign_on_real(q, cuts):
    """+1 or -1 by how many cuts (numerator, denominator) sit at or below the real part a/den. None exactly on a cut."""
    a, den = q[0], q[4]
    count = 0
    for cn, cd in cuts:
        left, right = a * cd, cn * den
        if left == right:
            return 0
        if left > right:
            count += 1
    return -1 if count % 2 else 1


patterns = [[(0, 1)], [(1, 2)], [(-1, 2)], [(3, 4)], [(-3, 4)], [(9, 10)], [(-9, 10)], [(-1, 2), (1, 2)], [(1, 4), (3, 4)], [(-3, 4), (-1, 4)], [(-9, 10), (9, 10)], [(-1, 2), (0, 1), (1, 2)], [(-3, 4), (-1, 2), (-1, 4), (1, 4), (1, 2), (3, 4)], [(99, 100)], [(-99, 100)]]
for dims, seed in (((2, 2), 801), ((2, 3), 802), ((3, 3), 803), ((2, 2, 2), 804), ((2, 2, 3), 805)):
    lat = Lat(*dims)
    rng = RNG(seed)
    both = 0
    for cuts in patterns:
        vals = {}
        draws = 0
        while len(vals) < 2 and draws < 30000:
            draws += 1
            cfg = [Q.random_unit(rng) for _ in lat.links]
            s = 1
            for w in lat.words:
                s *= sign_on_real(Q.word_value(cfg, w), cuts)
                if s == 0:
                    break
            if s:
                vals[s] = 1
        both += 1 if len(vals) == 2 else 0
    print("IND_SU2_BANDS_SIDES_2|lattice=%s|real_part_band_patterns=%d|patterns_showing_both_values_of_S=%d|json=0" % ("x".join(map(str, dims)), len(patterns), both))
    sys.stdout.flush()
print("IND_BANDS2_DONE|json=0")
